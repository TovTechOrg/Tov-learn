# Contributing to Tov-learn

## Ways to Contribute

- **Add course content** — new lessons to an existing course
- **Add a new course** — a full course following the standard structure
- **Improve a skill module** — enhance teaching, quiz, or display logic
- **Add a new module** — extend the skill with new capabilities
- **Fix bugs** — open an issue first so we can align on the fix

---

## Adding a Lesson

1. Find the right module folder under `courses/[course-name]/lessons/`
2. Create a folder: `[X.Y]-[lesson-name]/`
3. Add two files:
   - `[X.Y]_script.txt` — lesson script, sections split by `[מעבר שקף]`
   - `[X.Y]_exercises.md` — 2–4 exercises, one per concept
4. Update `courses/[course-name]/COURSE.md` with the new lesson row

**Script format:**
```
Title: [Lesson Title]

[מעבר שקף]

[Section content — 3–5 paragraphs]

[מעבר שקף]

[Next section]
```

Each section should be teachable in 5–10 minutes. Focus on one concept per section.

---

## Adding a New Course

1. Create `courses/[course-name]/COURSE.md` (copy from `courses/ai-engineer/COURSE.md`)
2. Create `courses/[course-name]/lessons/` with at least one complete module
3. Open an issue with the label `content` to discuss structure before adding many lessons

---

## Adding or Modifying a Skill Module

Modules live in `.claude/commands/learn/`. Each module is a standalone markdown file with instructions for Claude.

**Rules:**
- Instructions in English
- First line after the title: `Respond in session.language throughout.`
- Module must be self-contained — don't assume another module's state
- If the module is user-facing, follow the display conventions in `display.md`

**To add a new module:**
1. Create `.claude/commands/learn/[module-name].md`
2. Add a routing entry in `.claude/commands/learn.md` (Step 2 — Route table)
3. Add a row to the modules table in `CLAUDE.md`
4. Update the global install `Copy-Item` command in `setup.md`

---

## Pull Requests

- One PR per change (lesson, module, or fix)
- Test the flow manually with `/learn` before opening the PR
- Describe what the learner experience looks like after your change
