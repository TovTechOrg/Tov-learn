# UserPromptSubmit hook: notice when the learner sounds stuck and point Claude to the help flow.
#
# If the learner's message contains a "stuck" phrase (Hebrew or English) — not understanding
# the material, or something in an exercise/project not working — add a short note to Claude's
# context suggesting the /learn stuck module. The learner's message itself is never blocked
# or changed; Claude decides whether the help flow fits.
#
# Any unexpected error -> exit 0 with no output (the message goes through as usual).

try {
    [Console]::InputEncoding  = [System.Text.Encoding]::UTF8   # Hebrew prompts arrive as UTF-8
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8   # the note may quote Hebrew text
    $inputJson = [Console]::In.ReadToEnd()
    if (!$inputJson) { exit 0 }
    $prompt = ($inputJson | ConvertFrom-Json).prompt
    if (!$prompt -or $prompt.TrimStart().StartsWith("/")) { exit 0 }   # slash commands route themselves

    $stuckPatterns = @(
        # Hebrew — not understanding
        'לא הבנתי', 'לא מבינ(ה|ים|ות)?\b', 'לא ברור', 'לא מצליח', 'לא מצליחה', 'מבולבל', 'מבולבלת',
        # Hebrew — stuck / broken
        'נתקעתי', 'תקוע', 'תקועה', 'לא עובד', 'לא עובדת', 'לא עובדים', 'נשבר', 'שגיאה', 'באג',
        # English
        "don'?t understand", "didn'?t understand", 'confus(ed|ing)', "\bstuck\b",
        "(doesn'?t|does not|isn'?t|is not|not) work(ing)?", '\berror\b', '\bbug\b', '\bbroken\b'
    )
    $regex = '(?i)(' + ($stuckPatterns -join '|') + ')'
    if ($prompt -notmatch $regex) { exit 0 }

    # Worded as facts, not commands: the hooks docs warn that imperative "system instruction"
    # phrasing in additionalContext can trigger Claude's prompt-injection defenses.
    $context = "The learner's message contains a phrase that often means being stuck ('$($Matches[1])'). " +
               "This course's /learn skill has a help flow for learners who are stuck on the material " +
               "or on an exercise or project that doesn't work: .claude/commands/learn/stuck.md. " +
               "The note applies only if the message is actually about being stuck."
    @{ hookSpecificOutput = @{ hookEventName = "UserPromptSubmit"; additionalContext = $context } } |
        ConvertTo-Json -Compress -Depth 3
    exit 0
} catch {
    exit 0
}
