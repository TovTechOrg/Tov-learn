#!/usr/bin/env python3
"""Structural validation for Tov-learn skill files.

Checks:
  1. Every module referenced in learn.md (route + commands tables) exists
  2. Every module listed in the CLAUDE.md modules table exists, and every
     module file in .claude/commands/learn/ is listed there
  3. Cross-references between modules (any `.claude/commands/learn/X.md`
     mentioned inside a module) are not broken
  4. Every lesson folder has both _script.txt and _exercises.md
  5. Each COURSE.md lesson table matches the lesson folders on disk
  6. Regression guards: teaching.md keeps Step 5 (End of Lesson) and the
     mandatory-exercises rule
  7. Exercise rules (exercises.md tracking format, required exercises, paid-exercise flow
     without a mentor wait), lesson order (order.md) and skip quizzes
  8. Regression guards for the manual-test fixes: save after showing, the order of a
     reply that saves, Hebrew words and no escape sequences, quiz rules, status by
     completion, exercise plan, next lesson only from COURSE.md
  9. Every script referenced by a hook in .claude/settings.json exists
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
LEARN_MD = ROOT / ".claude" / "commands" / "learn.md"
LEARN_COMMANDS = ROOT / ".claude" / "commands" / "learn"
CLAUDE_MD = ROOT / "CLAUDE.md"
COURSES = ROOT / "courses"

MODULE_REF = re.compile(r"\.claude/commands/learn/([\w-]+\.md)")

errors = []


def error(msg):
    errors.append(msg)


def read(path):
    return path.read_text(encoding="utf-8")


# 1. learn.md routing + commands tables
if not LEARN_MD.exists():
    error("Missing entry point: .claude/commands/learn.md")
else:
    routed = set(MODULE_REF.findall(read(LEARN_MD)))
    if not routed:
        error("learn.md references no modules — routing table not parsed")
    for mod in sorted(routed):
        if not (LEARN_COMMANDS / mod).exists():
            error(f"learn.md routes to missing module: .claude/commands/learn/{mod}")

# 2. CLAUDE.md modules table <-> files on disk
existing = {p.name for p in LEARN_COMMANDS.glob("*.md")}
if CLAUDE_MD.exists():
    listed = set(MODULE_REF.findall(read(CLAUDE_MD)))
    for mod in sorted(listed - existing):
        error(f"CLAUDE.md lists missing module: .claude/commands/learn/{mod}")
    for mod in sorted(existing - listed):
        error(f"Module not documented in CLAUDE.md modules table: .claude/commands/learn/{mod}")

# 3. Cross-references inside modules
for src in sorted(LEARN_COMMANDS.glob("*.md")):
    for ref in sorted(set(MODULE_REF.findall(read(src)))):
        if ref not in existing:
            error(f"{src.name} references missing file: .claude/commands/learn/{ref}")

# 4 + 5. Lesson folders and COURSE.md
LESSON_DIR = re.compile(r"^(\d+\.\d+)-")
TABLE_ROW = re.compile(r"^\|\s*(\d+\.\d+)\s*\|", re.MULTILINE)

for course_dir in sorted(COURSES.iterdir()):
    if not course_dir.is_dir():
        continue
    lessons_dir = course_dir / "lessons"
    if not lessons_dir.exists():
        continue

    on_disk = set()
    for module_dir in sorted(lessons_dir.iterdir()):
        if not module_dir.is_dir():
            continue
        for lesson_dir in sorted(module_dir.iterdir()):
            if not lesson_dir.is_dir():
                continue
            rel = lesson_dir.relative_to(ROOT)
            m = LESSON_DIR.match(lesson_dir.name)
            if m:
                on_disk.add(m.group(1))
            if not list(lesson_dir.glob("*_script.txt")):
                error(f"Missing script:    {rel}")
            if not list(lesson_dir.glob("*_exercises.md")):
                error(f"Missing exercises: {rel}")

    course_md = course_dir / "COURSE.md"
    if not course_md.exists():
        error(f"Missing COURSE.md: {course_dir.relative_to(ROOT)}")
        continue
    in_table = set(TABLE_ROW.findall(read(course_md)))
    rel_course = course_md.relative_to(ROOT)
    for num in sorted(on_disk - in_table, key=lambda s: [int(x) for x in s.split(".")]):
        error(f"{rel_course}: lesson {num} has a folder but is not in the lesson list")
    for num in sorted(in_table - on_disk, key=lambda s: [int(x) for x in s.split(".")]):
        error(f"{rel_course}: lesson {num} is listed but has no folder")

# 6. Regression guards on teaching.md
teaching_path = LEARN_COMMANDS / "teaching.md"
if teaching_path.exists():
    teaching = read(teaching_path)
    if "Step 5" not in teaching:
        error("Regression: teaching.md is missing 'Step 5 — End of Lesson'")
    if "Exercises — mandatory" not in teaching:
        error("Regression: teaching.md lost the mandatory-exercises rule")
    if "One slide per message" not in teaching:
        error("Regression: teaching.md lost the one-slide-per-message rule")

# 5. Regression guard: both lesson modes give exercises at the end of the lesson, follow the
#    shared exercises rules, and save them where check-lesson-order.ps1 looks for them
for mod in ("teaching.md", "slides.md"):
    path = LEARN_COMMANDS / mod
    if path.exists():
        text = path.read_text(encoding="utf-8")
        if "always, never skip" not in text:
            error(f"Regression: {mod} end of lesson no longer requires exercises")
        if "exercises-lesson-{lesson_number}.md" not in text:
            error(f"Regression: {mod} no longer saves exercises to progress/exercises-lesson-X.Y.md")
        if ".claude/commands/learn/exercises.md" not in text:
            error(f"Regression: {mod} no longer follows the shared exercises rules (exercises.md)")
        if "**Exercises required:** yes" not in text:
            error(f"Regression: {mod} no longer marks finished lessons with '**Exercises required:** yes' "
                  f"(check-lesson-order.ps1 tells new lessons from ones finished before the exercises rule)")
        if "Mark the lesson as taught under the exercises rule" not in text:
            error(f"Regression: {mod} no longer writes '**Exercises required:** yes' when the lesson starts "
                  f"(check-lesson-order.ps1 tells new lessons from ones learned before the rules)")
        if "Mark the lesson's slides as done" not in text:
            error(f"Regression: {mod} no longer saves 'Slides covered: all' before the exercises "
                  f"(check-lesson-order.ps1 needs it to catch exercises left unfinished)")
        if "session.failed_skip_quiz" not in text:
            error(f"Regression: {mod} no longer limits exercises after a failed skip quiz")
        if "Quiz, mini project, or neither" not in text or "only the exercises are" not in text:
            error(f"Regression: {mod} no longer says the quiz / mini project is optional")
if teaching_path.exists() and "**Skip quiz passed:**" not in teaching_path.read_text(encoding="utf-8"):
    error("Regression: teaching.md no longer records a passed skip quiz ('**Skip quiz passed:**')")
if teaching_path.exists():
    text = teaching_path.read_text(encoding="utf-8")
    if "**Score ≥ 8 — passed.**" not in text or "**Score < 8 — not passed.**" not in text:
        error("Regression: teaching.md skip quiz pass mark is no longer 8")
    if text.count("session.failed_skip_quiz") < 2:
        error("Regression: teaching.md no longer limits exercises after a failed skip quiz (session.failed_skip_quiz)")
    if "Learn the lesson, or quiz first" not in text:
        error("Regression: teaching.md no longer offers 'learn or quiz first' at the start of every lesson")
slides_path = LEARN_COMMANDS / "slides.md"
if slides_path.exists() and "## Step 1B — Learn the Lesson, or Quiz First" not in slides_path.read_text(encoding="utf-8"):
    error("Regression: slides.md no longer offers 'learn or quiz first' at the start of every lesson")
order_path = LEARN_COMMANDS / "order.md"
if not order_path.exists():
    error("Missing reference module: .claude/commands/learn/order.md (lesson-order rules)")
else:
    text = order_path.read_text(encoding="utf-8")
    for needed in ("**Skip quiz passed:**", "**Exercises required:** yes", "quiz module", "## רשימת שיעורים"):
        if needed not in text:
            error(f"Regression: order.md no longer mentions '{needed}' (check-lesson-order.ps1 relies on it)")
quiz_path = LEARN_COMMANDS / "quiz.md"
if quiz_path.exists():
    text = quiz_path.read_text(encoding="utf-8")
    for needed in ("## Module Skip Quiz", "at least one correct multiple-choice answer for every lesson",
                   "Passed skip quiz — detailed explanations",
                   "**Skip quiz passed:**", "module-X.md"):
        if needed not in text:
            error(f"Regression: quiz.md module skip quiz no longer defines '{needed}'")
exercises_rules = LEARN_COMMANDS / "exercises.md"
if exercises_rules.exists():
    text = exercises_rules.read_text(encoding="utf-8")
    for needed in ("# תרגילים — שיעור {lesson_number}", "**נדרשים:**", "## תרגיל", "exercise-flags.md",
                   "## After a failed skip quiz"):
        if needed not in text:
            error(f"Regression: exercises.md no longer defines '{needed}' "
                  f"(check-lesson-order.ps1 and status.md rely on the tracking format)")
    # Paid-exercise flow: never wait for a mentor, never count a free trial as free, adapt before skipping
    if "**מדריך:**" in text or "contact the course mentor" in text:
        error("Regression: exercises.md paid-exercise flow waits for a mentor again (learning must never wait)")
    if "A free trial is not a free way" not in text:
        error("Regression: exercises.md no longer says a free trial isn't a free way")
    if "adapt the exercise" not in text or "(גרסה מותאמת)" not in text:
        error("Regression: exercises.md no longer adapts a paid exercise before skipping it")

# 5b. Fixes from the manual test (2026-11): save after showing, Hebrew output, quiz and status rules
learn_path = ROOT / ".claude" / "commands" / "learn.md"
if learn_path.exists():
    text = learn_path.read_text(encoding="utf-8")
    for needed in ("**Save after showing:**", "no escape sequences", "**הבא**", "**המשך**"):
        if needed not in text:
            error(f"Regression: learn.md no longer defines '{needed}'")
if teaching_path.exists():
    text = teaching_path.read_text(encoding="utf-8")
    for needed in ("original number", "Never show a sample answer", "מתוך 10", "no extra quiz"):
        if needed not in text:
            error(f"Regression: teaching.md no longer says '{needed}'")
if quiz_path.exists():
    text = quiz_path.read_text(encoding="utf-8")
    for needed in ("**Per lesson (DD-MM-YYYY):**", "no score so far", "The section's main idea",
                   "(מבחן דילוג)", "options must read clearly in Hebrew"):
        if needed not in text:
            error(f"Regression: quiz.md no longer says '{needed}'")
if order_path.exists():
    text = order_path.read_text(encoding="utf-8")
    if "only for a lesson the note says is **not started**" not in text:
        error("Regression: order.md offers the lesson skip quiz for a lesson whose learning already started")
    if "having no lesson started yet" not in text:
        error("Regression: order.md offers the module skip quiz for a module whose lessons already started")
if quiz_path.exists():
    text = quiz_path.read_text(encoding="utf-8")
    if "One attempt, offered only before the module's first lesson starts" not in text:
        error("Regression: quiz.md offers the module skip quiz again, or after a lesson of the module was started")
    if "Grading free-text answers — by ideas, not by wording" not in text:
        error("Regression: quiz.md no longer accepts free-text answers in the learner's own words")
status_path = LEARN_COMMANDS / "status.md"
if status_path.exists():
    text = status_path.read_text(encoding="utf-8")
    if "by completion, not by score" not in text or "Mastered" in text:
        error("Regression: status.md no longer shows lesson status by completion (quizzes are optional)")
if teaching_path.exists():
    text = teaching_path.read_text(encoding="utf-8")
    if "Never restart from the first slide without asking" not in text:
        error("Regression: teaching.md no longer asks where to continue when returning to a lesson in progress")
    if 'never "חלק"' not in text:
        error("Regression: teaching.md no longer calls the lesson's sections 'שקף' consistently")
resume_path = LEARN_COMMANDS / "resume.md"
if resume_path.exists() and "never that none were covered" not in resume_path.read_text(encoding="utf-8"):
    error("Regression: resume.md may again say no slides were covered for a lesson in progress")

# 5c. Fixes from the main-version retest (2026-11-23)
GUARDS_5C = [
    (learn_path, "**A reply that saves — always in this order:**", "learn.md no longer orders a saving reply: content, save, one closing line"),
    (learn_path, "never ends with a save and no text", "learn.md may let a reply end with a save and no visible text"),
    (LEARN_COMMANDS / "resume.md", "Ignore a review date when the only quiz in the file is a skip quiz",
     "resume.md may suggest a review based on an unlabeled skip quiz"),
    (learn_path, "in files you save", "learn.md's no-escape rule no longer covers saved files"),
    (learn_path, "**No HTML in chat:**", "learn.md no longer forbids HTML tags in chat"),
    (learn_path, "**Next lesson — only from `COURSE.md`:**", "learn.md no longer names the next lesson from COURSE.md only"),
    (order_path, "on Mac or Linux it doesn't run: check it yourself", "order.md no longer has the Mac/Linux fallback for the lesson-order hook"),
    (order_path, "**Name lessons only from `COURSE.md`.**", "order.md no longer ignores a script's mention of other lessons"),
    (teaching_path, "**Number slides from the script, not from memory.**", "teaching.md no longer numbers slides from the script"),
    (teaching_path, "skip this slide", "teaching.md's skip question no longer offers skipping one slide"),
    (teaching_path, "keep the exercise's own step numbers", "teaching.md may renumber an exercise's steps in reminders"),
    (teaching_path, "an earlier slide, or an earlier lesson", "teaching.md's thinking questions may go beyond the material"),
    (exercises_rules, "## תוכנית", "exercises.md no longer saves the planned exercises"),
    (slides_path, "save them in the tracking file's plan", "slides.md no longer saves its fresh exercises in the plan"),
    (LEARN_COMMANDS / "stuck.md", "Try the smallest fix first", "stuck.md no longer tries the smallest fix first"),
    (LEARN_COMMANDS / "progress.md", "Review suggestions come only from quizzes taken after learning",
     "progress.md may suggest a review based on a skip quiz"),
    (status_path, "לא עברת את מבחן הדילוג", "status.md no longer softens the skip-quiz wording"),
    (order_path, "**Optional lessons** (type `רשות`", "order.md no longer exempts optional lessons from the order"),
    (ROOT / ".claude" / "scripts" / "check-lesson-order.ps1", "רשות", "check-lesson-order.ps1 may block on optional lessons again"),
]
AI_DEV_COURSE = ROOT / "courses" / "ai-dev" / "COURSE.md"
GUARDS_5C += [
    (AI_DEV_COURSE, "מחליפים את ההוראה הישנה", "COURSE.md no longer says exercises.md replaces the old 'contact the mentor' instruction"),
    (exercises_rules, "these rules replace that instruction", "exercises.md no longer overrides the exercise files' 'contact the mentor' instruction"),
]
for path, needed, message in GUARDS_5C:
    if path.exists() and needed not in path.read_text(encoding="utf-8"):
        error(f"Regression: {message}")
# The no-escape rule's examples must stay escape sequences. Tools can silently decode an escape into
# the letter itself, which is the bug the rule describes. Hebrew range built with chr() for that reason.
_hebrew_letter_span = re.compile("`[" + chr(0x05D0) + "-" + chr(0x05EA) + "]`")
for path in (learn_path, LEARN_COMMANDS / "quiz.md"):
    if path.exists() and _hebrew_letter_span.search(path.read_text(encoding="utf-8")):
        error(f"Regression: {path.name}'s escape-sequence example is a literal Hebrew letter, not an escape sequence")
if AI_DEV_COURSE.exists():
    course_text = AI_DEV_COURSE.read_text(encoding="utf-8")
    for bad in ("מדיניות הקורס (מתוך קבצי התרגילים)", "לאישור"):
        if bad in course_text:
            error(f"Regression: COURSE.md contains '{bad}' again (contradicts exercises.md or isn't for outside users)")
if exercises_rules.exists():
    for line in exercises_rules.read_text(encoding="utf-8").splitlines():
        if line.startswith("- [n]") and "## תרגיל" in line:
            error("Regression: exercises.md plan lines use the '## תרגיל' heading the lesson-order check counts")

# 6. Every script referenced by a hook in .claude/settings.json exists
settings_path = ROOT / ".claude" / "settings.json"
if settings_path.exists():
    import json, re
    settings = json.loads(settings_path.read_text(encoding="utf-8"))
    for event, groups in settings.get("hooks", {}).items():
        for group in groups:
            for hook in group.get("hooks", []):
                cmd = " ".join([hook.get("command", "")] + hook.get("args", []))
                for script in re.findall(r"\.claude[\\/]+scripts[\\/]+([\w.-]+\.ps1)", cmd):
                    if not (ROOT / ".claude" / "scripts" / script).exists():
                        error(f"{event} hook references missing script: .claude/scripts/{script}")
                # PowerShell hooks must skip silently where PowerShell is missing (Mac/Linux)
                if ".ps1" in cmd and "command -v powershell >/dev/null 2>&1 || exit 0" not in cmd:
                    error(f"{event} hook runs PowerShell without the Mac/Linux guard "
                          "('command -v powershell >/dev/null 2>&1 || exit 0')")

# --- Report ---
if errors:
    print(f"FAILED — {len(errors)} error(s):\n")
    for e in errors:
        print(f"  ✗ {e}")
    sys.exit(1)
else:
    print("PASSED — all checks OK")
