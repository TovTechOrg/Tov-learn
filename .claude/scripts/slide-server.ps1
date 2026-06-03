# Tov-learn Slide Server — localhost:7823
# GET  /            → returns current slide number
# POST / {num}      → speak slide N + sync viewer
# POST / queue:N-M  → speak slides N through M sequentially (auto-next)
# POST / pause      → pause TTS in place
# POST / resume     → resume from pause point
# POST / stop       → stop TTS

param([int]$Port = 7823)

$slideFile   = "$env:TEMP\tov_current_slide.txt"
$lessonFile  = "$env:TEMP\tov_current_lesson.txt"
$controlFile = "$env:TEMP\tov_tts_control.txt"
$ttsTextFile = "$env:TEMP\tov_tts_text.txt"

if (!(Test-Path $slideFile)) { "1" | Set-Content $slideFile }
[System.IO.File]::WriteAllText($controlFile, "stop")
[System.IO.File]::WriteAllText($ttsTextFile, "")

$script:loadedLesson = ""
$script:ttsScripts   = @{}

function Load-Lesson {
    param([string]$lessonPath)
    if ($lessonPath -eq $script:loadedLesson) { return }
    $script:ttsScripts = @{}
    $ttsDir = Join-Path $lessonPath "digital-course-tts-scripts"
    if (Test-Path $ttsDir) {
        Get-ChildItem "$ttsDir\slide-*.txt" | ForEach-Object {
            $num = [int]($_.BaseName -replace 'slide-', '')
            $script:ttsScripts[$num] = (Get-Content $_.FullName -Raw -Encoding UTF8).Trim()
        }
        Write-Host "Preloaded $($script:ttsScripts.Count) TTS scripts from $lessonPath"
    }
    $script:loadedLesson = $lessonPath
}

# --- Persistent TTS runspace (opened once at startup, never blocks the HTTP loop) ---
$ttsRunspace = [System.Management.Automation.Runspaces.RunspaceFactory]::CreateRunspace()
$ttsRunspace.ApartmentState = [System.Threading.ApartmentState]::STA
$ttsRunspace.Open()

$ttsPS = [System.Management.Automation.PowerShell]::Create()
$ttsPS.Runspace = $ttsRunspace

$ctrlCapture = $controlFile
$textCapture = $ttsTextFile

[void]$ttsPS.AddScript({
    param($ctrlFile, $txtFile)
    Add-Type -AssemblyName System.Speech
    $s = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $hv = $s.GetInstalledVoices() | Where-Object { $_.VoiceInfo.Culture.Name -like 'he-*' } | Select-Object -First 1
    if ($hv) { $s.SelectVoice($hv.VoiceInfo.Name) }

    while ($true) {
        $ctrl = ""
        try { $ctrl = ([System.IO.File]::ReadAllText($ctrlFile)).Trim() } catch {}

        if ($ctrl -eq "speak") {
            $text = ""
            try { $text = [System.IO.File]::ReadAllText($txtFile, [System.Text.Encoding]::UTF8).Trim() } catch {}
            if ($text) {
                [System.IO.File]::WriteAllText($ctrlFile, "speaking")
                $chunks = [System.Text.RegularExpressions.Regex]::Split($text, '(?<=[.!?])\s+|\r?\n') | Where-Object { $_.Trim() -ne '' }
                $aborted = $false
                foreach ($chunk in $chunks) {
                    if ($aborted) { break }
                    # Wait while paused; abort on stop or new speak command
                    while ($true) {
                        try { $ctrl = ([System.IO.File]::ReadAllText($ctrlFile)).Trim() } catch { $ctrl = "speaking" }
                        if ($ctrl -eq "stop")   { $aborted = $true; break }
                        if ($ctrl -eq "speak")  { $aborted = $true; break }
                        if ($ctrl -eq "pause")  { Start-Sleep -Milliseconds 200; continue }
                        if ($ctrl -eq "resume") { [System.IO.File]::WriteAllText($ctrlFile, "speaking"); break }
                        break  # "speaking" — proceed
                    }
                    if (-not $aborted) { $s.Speak($chunk) }
                }
            }
        } elseif ($ctrl -eq "exit") {
            break
        }
        Start-Sleep -Milliseconds 100
    }
    $s.Dispose()
}).AddArgument($ctrlCapture).AddArgument($textCapture)

$ttsPS.BeginInvoke() | Out-Null
Write-Host "TTS runspace ready"

# --- TTS control functions (instant file writes — never block the HTTP loop) ---

function Kill-TTS {
    [System.IO.File]::WriteAllText($controlFile, "stop")
}

function Start-TTS {
    param([string]$text)
    [System.IO.File]::WriteAllText($ttsTextFile, $text, (New-Object System.Text.UTF8Encoding $false))
    [System.IO.File]::WriteAllText($controlFile, "speak")
}

function Get-LessonLoaded {
    if (Test-Path $lessonFile) {
        $lesson = (Get-Content $lessonFile -Raw -Encoding UTF8).Trim()
        Load-Lesson $lesson
    }
}

function Speak-Slide {
    param([int]$num)
    Get-LessonLoaded
    $text = $script:ttsScripts[$num]
    if ($text) { Start-TTS $text }
}

function Speak-Queue {
    param([int]$from, [int]$to)
    Get-LessonLoaded
    $combined = ($from..$to | ForEach-Object {
        if ($script:ttsScripts[$_]) { $script:ttsScripts[$_] }
    }) -join "`n`n"
    if ($combined) { Start-TTS $combined }
}

if (Test-Path $lessonFile) {
    $lesson = (Get-Content $lessonFile -Raw -Encoding UTF8).Trim()
    Load-Lesson $lesson
}

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$Port/")
$listener.Start()
Write-Host "Slide server running on http://localhost:$Port"

while ($listener.IsListening) {
    try {
        $ctx = $listener.GetContext()
        $res = $ctx.Response
        $res.Headers.Add("Access-Control-Allow-Origin", "*")
        $res.Headers.Add("Cache-Control", "no-cache")
        $res.KeepAlive = $false

        if ($ctx.Request.HttpMethod -eq "POST") {
            $reader = New-Object System.IO.StreamReader($ctx.Request.InputStream)
            $body   = $reader.ReadToEnd().Trim()

            $buf = [System.Text.Encoding]::UTF8.GetBytes("ok")
            $res.ContentLength64 = $buf.Length
            $res.OutputStream.Write($buf, 0, $buf.Length)
            $res.OutputStream.Close()

            if ($body -eq "stop") {
                Kill-TTS
            } elseif ($body -eq "pause") {
                [System.IO.File]::WriteAllText($controlFile, "pause")
            } elseif ($body -eq "resume") {
                [System.IO.File]::WriteAllText($controlFile, "resume")
            } elseif ($body -match '^queue:(\d+)-(\d+)$') {
                Speak-Queue ([int]$Matches[1]) ([int]$Matches[2])
            } else {
                $num = [int]$body
                "$num" | Set-Content $slideFile
                Speak-Slide $num
            }
        } else {
            $cur = if (Test-Path $slideFile) { (Get-Content $slideFile).Trim() } else { "1" }
            $buf = [System.Text.Encoding]::UTF8.GetBytes($cur)
            $res.ContentLength64 = $buf.Length
            $res.OutputStream.Write($buf, 0, $buf.Length)
            $res.OutputStream.Close()
        }
    } catch { }
}

# Cleanup on exit
[System.IO.File]::WriteAllText($controlFile, "exit")
Start-Sleep -Seconds 1
$ttsPS.Dispose()
$ttsRunspace.Close()
$ttsRunspace.Dispose()
