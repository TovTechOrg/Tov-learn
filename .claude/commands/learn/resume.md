# Resume Module

*Loaded when /learn is called with no arguments. Replaces the static "lesson or project analysis?" prompt with a smart suggestion based on actual progress.*

Respond in `session.language` throughout.

---

## Step 1 — Read Progress State

Silently read:
- `~/skill-tutor-tutorials/learner_profile.md` — find `## Lessons Studied` for last lesson
- All `~/skill-tutor-tutorials/progress/lesson-*.md` — extract next review dates
- `~/skill-tutor-tutorials/topics/knowledge_map.md` — find in-progress lessons
- `~/skill-tutor-tutorials/project/ai-dev-project.md` — final project state (may not exist)

Compute today's date. Classify each lesson:
- **Overdue** — next review date is before today
- **Due today** — next review date is today
- **In progress** — started, score under 8, not yet due
- **Next new** — first lesson in COURSE.md with no progress file

Check final project eligibility: learner is ready to start the final project if they have progress files for lessons in module 2 (any lesson 2.x), or have completed all lessons through 1.8.

---

## Step 2 — Build Smart Suggestion

Present options based on what you found. Show only options that actually apply.

**If there are overdue or due-today lessons:**
```
Welcome back. Here's where things stand:

🔁 Due for review: Lesson [X.X] — [title] ([N] days overdue)
📖 Next new lesson: [X.X] — [title]
🔍 Project analysis
[if eligible: 🏗️ Final Project — [show "starting" or current phase if already selected]]

What would you like to do?
```

**If nothing is due (good standing):**
```
Welcome back. You're up to date on reviews.

📖 Continue: Lesson [X.X] — [title] (in progress)
📖 Next new lesson: [X.X] — [title]
🔍 Project analysis
[if eligible: 🏗️ Final Project — [show "starting" or current phase if already selected]]

What would you like to do?
```

**If no progress exists yet (first time):**
```
Welcome. Let's start with the first lesson.

📖 Lesson 0.1 — [title]
🔍 Analyze your current project first

What would you like to do?
```

---

## Step 3 — Route Based on Answer

| Answer | Action |
|--------|--------|
| Picks a lesson number | Read `.claude/commands/learn/teaching.md` with that lesson |
| "review" / picks a due lesson | Read `.claude/commands/learn/teaching.md` with that lesson |
| "project analysis" | Read `.claude/commands/learn/project-analysis.md` |
| "final project" / "project" / picks 🏗️ | Read `.claude/commands/learn/project.md` |
| "status" / "dashboard" | Read `.claude/commands/learn/status.md` |
