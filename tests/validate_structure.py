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

# --- Report ---
if errors:
    print(f"FAILED — {len(errors)} error(s):\n")
    for e in errors:
        print(f"  ✗ {e}")
    sys.exit(1)
else:
    print("PASSED — all checks OK")
