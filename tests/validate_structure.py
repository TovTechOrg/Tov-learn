#!/usr/bin/env python3
"""Structural validation for Tov-learn skill files.

Checks:
  1. All modules in learn.md routing table exist
  2. Cross-references between modules are not broken
  3. Every lesson folder has both _script.txt and _exercises.md
  4. Regression guard: teaching.md contains Step 5 (End of Lesson)
  5. Regression guard: teaching.md and slides.md require and save end-of-lesson exercises
     under the shared rules in exercises.md (tracking-file format), mark the slides as done
     before the exercises, and keep the quiz / mini project optional
  6. Every script referenced by a hook in .claude/settings.json exists
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
LEARN_COMMANDS = ROOT / ".claude" / "commands" / "learn"
COURSES = ROOT / "courses"

errors = []


def error(msg):
    errors.append(msg)


# 1. Routing table — all targets must exist
ROUTING_MODULES = [
    "teaching.md",
    "status.md",
    "resume.md",
    "quiz.md",
    "progress.md",
    "project-analysis.md",
    "stuck.md",
]
for mod in ROUTING_MODULES:
    if not (LEARN_COMMANDS / mod).exists():
        error(f"Missing routed module: .claude/commands/learn/{mod}")

# 2. Cross-references between modules
CROSS_REFS = {
    "teaching.md": ["quiz.md", "progress.md", "exercises.md"],
    "slides.md": ["exercises.md"],
    "resume.md": ["teaching.md", "status.md", "order.md"],
    "setup.md": ["order.md"],
    "quiz.md": ["order.md"],
}
for src, refs in CROSS_REFS.items():
    for ref in refs:
        if not (LEARN_COMMANDS / ref).exists():
            error(f"{src} references missing file: .claude/commands/learn/{ref}")

# 3. Every lesson folder must have _script.txt and _exercises.md
for course_dir in sorted(COURSES.iterdir()):
    if not course_dir.is_dir():
        continue
    lessons_dir = course_dir / "lessons"
    if not lessons_dir.exists():
        continue
    for module_dir in sorted(lessons_dir.iterdir()):
        if not module_dir.is_dir():
            continue
        for lesson_dir in sorted(module_dir.iterdir()):
            if not lesson_dir.is_dir():
                continue
            rel = lesson_dir.relative_to(ROOT)
            if not list(lesson_dir.glob("*_script.txt")):
                error(f"Missing script:    {rel}")
            if not list(lesson_dir.glob("*_exercises.md")):
                error(f"Missing exercises: {rel}")

# 4. Regression guard: teaching.md must contain Step 5
teaching_path = LEARN_COMMANDS / "teaching.md"
if teaching_path.exists():
    if "Step 5" not in teaching_path.read_text(encoding="utf-8"):
        error("Regression: teaching.md is missing 'Step 5 — End of Lesson'")

# 5. Regression guard: both lesson modes give exercises at the end of the lesson, follow the
#    shared exercises rules, and save them where check-lesson-order.ps1 looks for them
for mod in ("teaching.md", "slides.md"):
    path = LEARN_COMMANDS / mod
    if path.exists():
        text = path.read_text(encoding="utf-8")
        if "Exercises — always, never skip" not in text:
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
        if "Quiz, mini project, or neither" not in text or "only the exercises are" not in text:
            error(f"Regression: {mod} no longer says the quiz / mini project is optional")
if teaching_path.exists() and "**Skip quiz passed:**" not in teaching_path.read_text(encoding="utf-8"):
    error("Regression: teaching.md no longer records a passed skip quiz ('**Skip quiz passed:**')")
if teaching_path.exists():
    text = teaching_path.read_text(encoding="utf-8")
    if "If they score ≥ 8" not in text or "If they score < 8" not in text:
        error("Regression: teaching.md skip quiz pass mark is no longer 8")
    if text.count("session.failed_skip_quiz") < 2:
        error("Regression: teaching.md no longer limits exercises after a failed skip quiz (session.failed_skip_quiz)")
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

# --- Report ---
if errors:
    print(f"FAILED — {len(errors)} error(s):\n")
    for e in errors:
        print(f"  ✗ {e}")
    sys.exit(1)
else:
    print("PASSED — all checks OK")
