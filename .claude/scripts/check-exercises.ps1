# Stop hook: make sure a just-finished lesson didn't skip its exercises.
#
# When Claude finishes a turn, look for a lesson that was marked complete in the last few
# minutes ("Slides covered: all") but has no exercises file. If found, block the stop once
# and tell Claude to give the exercises now. Exercises are an instruction in teaching.md and
# slides.md; this hook makes sure the model can't silently skip them.
#
# Safety:
#   - Exits immediately when stop_hook_active is true (Claude is already continuing because
#     of a Stop hook), so it can't loop.
#   - Reminds at most once per lesson (marker file), so a learner who declines isn't trapped.
#   - Only looks at lessons completed in the last $WindowMinutes, so lessons finished before
#     this hook existed never trigger it.
#   - Any unexpected error -> exit 0 (never blocks the session because of a hook bug).

$WindowMinutes = 15

try {
    $inputJson = [Console]::In.ReadToEnd()
    $hookInput = if ($inputJson) { $inputJson | ConvertFrom-Json } else { $null }
    if ($hookInput -and $hookInput.stop_hook_active) { exit 0 }

    $progressDir = Join-Path $env:USERPROFILE "skill-tutor-tutorials\progress"
    if (!(Test-Path $progressDir)) { exit 0 }

    $since = (Get-Date).AddMinutes(-$WindowMinutes)
    $recent = Get-ChildItem -Path $progressDir -Filter "lesson-*.md" -File |
        Where-Object { $_.LastWriteTime -ge $since } |
        Sort-Object LastWriteTime -Descending

    foreach ($file in $recent) {
        if ($file.Name -notmatch '^lesson-(\d+\.\d+)\.md$') { continue }
        $lesson = $Matches[1]

        $content = Get-Content $file.FullName -Raw -Encoding UTF8
        if ($content -notmatch 'Slides covered:\*\*\s*all') { continue }      # lesson not finished

        $exercises = Join-Path $progressDir "exercises-lesson-$lesson.md"
        if (Test-Path $exercises) { continue }                                 # exercises done

        $marker = Join-Path $progressDir ".exercises-reminded-$lesson"
        if (Test-Path $marker) { continue }                                    # already reminded once
        New-Item -ItemType File -Path $marker -Force | Out-Null

        $reason = "Lesson $lesson was marked complete, but no exercises were saved for it " +
                  "(~/skill-tutor-tutorials/progress/exercises-lesson-$lesson.md does not exist). " +
                  "Exercises are a required part of every lesson. Before finishing, give the " +
                  "learner the exercises for lesson $lesson now, following the exercises step of " +
                  "the module in use (teaching.md Step 5, or slides.md Step 4), one at a time, and " +
                  "save each completed exercise to that file. Respond in session.language. " +
                  "If the learner explicitly declines the exercises, respect that and continue."
        @{ decision = "block"; reason = $reason } | ConvertTo-Json -Compress
        exit 0
    }
} catch {
    exit 0
}
exit 0
