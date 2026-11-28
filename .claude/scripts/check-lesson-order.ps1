# PostToolUse hook (matcher: Read): runs after Claude reads a file.
#
# Lesson-order rule (.claude/commands/learn/order.md): a lesson starts only when every earlier lesson
# in the course order is complete. When the file is a lesson script (X.Y_script.txt) — which Claude
# reads whenever a lesson starts, whatever started it (/learn X.Y, slides mode, resume) — check every
# earlier lesson, and if any isn't complete, add a factual note for Claude next to the read result.
#
# An earlier lesson is complete when:
#   - its progress file, or its module's progress/module-M.md, says "**Skip quiz passed:**"; or
#   - it was learned under the current rules (progress file has "**Exercises required:** yes", written
#     when learning starts): "Slides covered: all" and its required exercises recorded (exercises.md); or
#   - it was learned before these rules (no such line): all slides covered, shown by "Slides covered: all"
#     or by a Sessions-table row whose "Sections Covered" says all ("All 15", "All sections"). Exercises
#     aren't checked for those.
# The note says "not started" only for a lesson with no progress file; any other incomplete lesson has
# started learning, and order.md offers the lesson skip quiz only for lessons not started. Likewise, a
# module skip quiz is offered only for an earlier module none of whose lessons has a progress file and
# whose module quiz was never taken (no module-M.md): one attempt only.
# Optional lessons (type רשות in COURSE.md) are skipped: they never block a later lesson.
# Fires every time such a lesson starts, in any session, until the earlier lessons are complete.
# It never fires at the end of a lesson (there's no Stop hook for this), so once per attempt.
# Any unexpected error -> exit 0 with no output (the read goes through as usual).

try {
    [Console]::InputEncoding  = [System.Text.Encoding]::UTF8
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $hookInput = [Console]::In.ReadToEnd() | ConvertFrom-Json
    $path = $hookInput.tool_input.file_path          # absolute, backslashes on Windows
    if (!$path -or $path -notmatch '(\d+\.\d+)_script\.txt$') { exit 0 }
    $lesson = $Matches[1]

    # courses/<course>/lessons/<module>/<X.Y-name>/X.Y_script.txt
    $lessonsDir = Split-Path (Split-Path (Split-Path $path -Parent) -Parent) -Parent
    $courseDir  = Split-Path $lessonsDir -Parent

    # Lesson order: the course's COURSE.md lesson table; fall back to the lesson folders on disk
    # Lessons whose type column says רשות are optional: they never block a later lesson
    $order = @()
    $optional = @()
    $courseMd = Join-Path $courseDir "COURSE.md"
    if (Test-Path $courseMd) {
        $order = @(Get-Content $courseMd -Encoding UTF8 | ForEach-Object {
            if ($_ -match '^\|\s*(\d+\.\d+)\s*\|') {
                $num = $Matches[1]
                if ($_ -match '\|\s*רשות\s*\|\s*$') { $script:optional += $num }
                $num
            } })
    }
    if ($order -notcontains $lesson) {
        $order = @(Get-ChildItem $lessonsDir -Recurse -File -Filter "*_script.txt" | ForEach-Object {
            if ($_.Name -match '^(\d+\.\d+)_script\.txt$') { $Matches[1] } } |
            Sort-Object { [version]$_ } -Unique)
    }
    $i = [array]::IndexOf($order, $lesson)
    if ($i -le 0) { exit 0 }                         # first lesson, or not found

    $progressDir = Join-Path $env:USERPROFILE "skill-tutor-tutorials\progress"
    function Read-Text($file) {
        $p = Join-Path $progressDir $file
        if (Test-Path $p) { Get-Content $p -Raw -Encoding UTF8 } else { $null }
    }

    # Older progress files (quiz.md format): a Sessions-table row whose 2nd column says all sections
    $legacyAllRow = '(?mi)^\|[^|\r\n]*\|\s*(all\b|הכל|כל )'
    $module = $lesson.Split('.')[0]
    $incomplete = @()
    $wholeModules = @()                              # earlier modules a module skip quiz can pass
    foreach ($l in $order[0..($i - 1)]) {
        if ($optional -contains $l) { continue }
        $m = $l.Split('.')[0]
        $moduleText = Read-Text "module-$m.md"
        if ($moduleText -and $moduleText -match '\*\*Skip quiz passed:\*\*') { continue }
        $text = Read-Text "lesson-$l.md"
        $state = $null
        if (!$text) {
            $state = "not started"
        } elseif ($text -match '\*\*Skip quiz passed:\*\*') {
            continue
        } elseif ($text -notmatch '\*\*Exercises required:\*\*\s*yes') {          # learned before the rules
            if ($text -notmatch 'Slides covered:\*\*\s*all' -and $text -notmatch $legacyAllRow) {
                $state = "learning started, slides not finished"
            }
        } elseif ($text -notmatch 'Slides covered:\*\*\s*all') {
            $state = "learning started, slides not finished"
        } else {
            $exercises = Read-Text "exercises-lesson-$l.md"
            if (!$exercises) {
                $state = "slides finished, no exercises started"
            } elseif ($exercises -match '\*\*נדרשים:\*\*\s*(\d+)') {   # a file without a count: can't tell
                $required = [int]$Matches[1]
                $recorded = ([regex]::Matches($exercises, '(?m)^## תרגיל')).Count
                if ($recorded -lt $required) { $state = "slides finished, $recorded of $required exercises recorded" }
            }
        }
        if ($state) {
            $incomplete += "$l ($state)"
            if ($m -ne $module -and $wholeModules -notcontains $m) { $wholeModules += $m }
        }
    }
    if ($incomplete.Count -eq 0) { exit 0 }

    # A module skip quiz is offered only once, and only before any lesson of the module was started:
    # no module-M.md (an earlier attempt) and no lesson progress file in the module
    $wholeModules = @($wholeModules | Where-Object {
        $mod = $_
        -not (Read-Text "module-$mod.md") -and
        -not ($order | Where-Object { $_.Split('.')[0] -eq $mod -and (Read-Text "lesson-$_.md") })
    })

    $note = "Lesson $lesson is starting, but earlier lessons in this course's order are not complete: " +
            ($incomplete -join "; ") + ". Under this course's lesson-order rules " +
            "(.claude/commands/learn/order.md), lesson $lesson begins only after every earlier lesson is " +
            "complete: finished (all slides and the required exercises) or passed by a skip quiz. " +
            "A lesson skip quiz applies only to lessons marked not started."
    if ($wholeModules.Count -gt 0) {
        $note += " Earlier modules with no lesson started yet and no earlier module-quiz attempt, which a module skip quiz (quiz module N) can pass " +
                 "as a whole: " + ($wholeModules -join ", ") + "."
    }
    $note += " A script read while building a module skip quiz is not a lesson start; this note does not apply to such a read."
    @{ hookSpecificOutput = @{ hookEventName = "PostToolUse"; additionalContext = $note } } |
        ConvertTo-Json -Compress -Depth 3
    exit 0
} catch {
    exit 0
}
