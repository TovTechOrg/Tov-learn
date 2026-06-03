#!/usr/bin/env python3
"""Structural validation for Tov-learn skill files.

Checks:
  1. All modules in learn.md routing table exist
  2. Cross-references between modules are not broken
  3. Every lesson folder has both _script.txt and _exercises.md
  4. Regression guard: teaching.md contains Step 5 (End of Lesson)
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

# --- Report ---
if errors:
    print(f"FAILED — {len(errors)} error(s):\n")
    for e in errors:
        print(f"  ✗ {e}")
    sys.exit(1)
else:
    print("PASSED — all checks OK")
