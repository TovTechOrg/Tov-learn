# Auto-save progress when Claude session ends.
# Reads lesson/slide from TTS temp files and writes to skill-tutor-tutorials/progress/.
# Runs silently — no output on success.

$lessonFile = "$env:TEMP\tov_current_lesson.txt"
$slideFile  = "$env:TEMP\tov_current_slide.txt"
$progressDir = "$env:USERPROFILE\skill-tutor-tutorials\progress"

if (!(Test-Path $lessonFile)) { exit 0 }
$lessonPath = (Get-Content $lessonFile -Raw -Encoding UTF8).Trim()
if (!$lessonPath) { exit 0 }

$lessonFolder = Split-Path $lessonPath -Leaf
$lessonNum = if ($lessonFolder -match '^(\d+\.\d+)') { $Matches[1] } else { $lessonFolder }

$slide = if (Test-Path $slideFile) { (Get-Content $slideFile -Raw).Trim() } else { "1" }
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"

if (!(Test-Path $progressDir)) { New-Item -ItemType Directory -Path $progressDir -Force | Out-Null }

$progressFile = "$progressDir\lesson-$lessonNum.md"

# Read existing file to preserve quiz scores and notes
$existing = if (Test-Path $progressFile) { Get-Content $progressFile -Raw -Encoding UTF8 } else { "" }

# Replace or prepend the auto-save block
$autoSaveBlock = @"
<!-- auto-save -->
**שיעור:** $lessonNum
**שקף אחרון:** $slide
**זמן:** $timestamp
**נתיב:** $lessonPath
<!-- /auto-save -->

"@

if ($existing -match '(?s)<!-- auto-save -->.*?<!-- /auto-save -->') {
    $updated = $existing -replace '(?s)<!-- auto-save -->.*?<!-- /auto-save -->\r?\n?', $autoSaveBlock
} else {
    $updated = $autoSaveBlock + $existing
}

[System.IO.File]::WriteAllText($progressFile, $updated, (New-Object System.Text.UTF8Encoding($true)))
