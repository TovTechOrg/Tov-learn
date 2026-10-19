#!/usr/bin/env python3
"""Structural validation for Tov-learn skill files.

Checks:
  1. All modules in learn.md routing table exist
  2. Cross-references between modules are not broken
  3. Every lesson folder has both _script.txt and _exercises.md
  4. Regression guard: teaching.md contains Step 5 (End of Lesson)
  5. Regression guard: teaching.md and slides.md require and save end-of-lesson exercises
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
    "teaching.md": ["quiz.md", "progress.md"],
    "resume.md": ["teaching.md", "status.md"],
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

# 5. Regression guard: both lesson modes give exercises at the end of the lesson,
#    and save them where the check-exercises hook looks for them
for mod in ("teaching.md", "slides.md"):
    path = LEARN_COMMANDS / mod
    if path.exists():
        text = path.read_text(encoding="utf-8")
        if "Exercises — always, never skip" not in text:
            error(f"Regression: {mod} end of lesson no longer requires exercises")
        if "exercises-lesson-{lesson_number}.md" not in text:
            error(f"Regression: {mod} no longer saves exercises to progress/exercises-lesson-X.Y.md")

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
