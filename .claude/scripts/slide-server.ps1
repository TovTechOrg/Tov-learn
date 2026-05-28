# Tov-learn Slide Server — localhost:7823
# GET  /        → returns current slide number
# POST / {num}  → advance to slide N + speak TTS
# POST / stop   → kill current TTS only

param([int]$Port = 7823)

$slideFile   = "$env:TEMP\tov_current_slide.txt"
$lessonFile  = "$env:TEMP\tov_current_lesson.txt"
$ttsTextFile = "$env:TEMP\tov_tts_text.txt"
$ttsRunFile  = "$env:TEMP\tov_tts_run.ps1"

if (!(Test-Path $slideFile)) { "1" | Set-Content $slideFile }

$script:ttsProcess    = $null
$script:loadedLesson  = ""
$script:ttsScripts    = @{}   # [int]slideNum → [string]text

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

function Kill-TTS {
    if ($script:ttsProcess -and !$script:ttsProcess.HasExited) {
        try { $script:ttsProcess.Kill() } catch {}
        $script:ttsProcess = $null
    }
}

function Speak-Slide {
    param([int]$num)
    Kill-TTS

    # Reload lesson if changed
    if (Test-Path $lessonFile) {
        $lesson = (Get-Content $lessonFile -Raw -Encoding UTF8).Trim()
        Load-Lesson $lesson
    }

    $text = $script:ttsScripts[$num]
    if (!$text) { return }

    # Write TTS text with BOM so runner reads Hebrew correctly
    [System.IO.File]::WriteAllText($ttsTextFile, $text, (New-Object System.Text.UTF8Encoding($true)))

    # Build runner script — backtick-dollar escapes PS vars in the here-string
    $runner = @"
Add-Type -AssemblyName System.Speech
`$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
`$hv = `$s.GetInstalledVoices() | Where-Object { `$_.VoiceInfo.Culture.Name -like 'he-*' } | Select-Object -First 1
if (`$hv) { `$s.SelectVoice(`$hv.VoiceInfo.Name) }
`$t = [System.IO.File]::ReadAllText('$ttsTextFile', [System.Text.Encoding]::UTF8)
`$s.Speak(`$t)
"@
    [System.IO.File]::WriteAllText($ttsRunFile, $runner, (New-Object System.Text.UTF8Encoding($true)))
    $script:ttsProcess = Start-Process powershell -ArgumentList "-NoProfile -WindowStyle Hidden -File `"$ttsRunFile`"" -PassThru
}

# Pre-load current lesson if already set
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

        if ($ctx.Request.HttpMethod -eq "POST") {
            $reader = New-Object System.IO.StreamReader($ctx.Request.InputStream)
            $body   = $reader.ReadToEnd().Trim()

            if ($body -eq "stop") {
                Kill-TTS
            } else {
                $num = [int]$body
                "$num" | Set-Content $slideFile
                Speak-Slide $num
            }
            $buf = [System.Text.Encoding]::UTF8.GetBytes("ok")
        } else {
            $cur = if (Test-Path $slideFile) { (Get-Content $slideFile).Trim() } else { "1" }
            $buf = [System.Text.Encoding]::UTF8.GetBytes($cur)
        }

        $res.ContentLength64 = $buf.Length
        $res.OutputStream.Write($buf, 0, $buf.Length)
        $res.OutputStream.Close()
    } catch { }
}
