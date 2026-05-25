# Tov-learn

Interactive AI tutor for the TovTech AI Engineer course, built as a Claude Code skill.

---

## Getting Started

### Step 1 — Prerequisites

- [Claude Code](https://claude.ai/code) installed (Pro plan or higher)
- Git

### Step 2 — Clone the repo into your project

Open Claude Code inside your project folder and run:

```bash
git clone https://github.com/RazHadas/Tov-learn.git .tov-learn
```

Then copy the skill files:

```bash
# Windows (PowerShell)
Copy-Item -Recurse .tov-learn\.claude\commands\learn .claude\commands\learn
Copy-Item .tov-learn\.claude\commands\learn.md .claude\commands\learn.md
```

### Step 3 — Run setup

Inside Claude Code, type:

```
/learn setup
```

This will:
- Ask for your preferred session language (Hebrew / English)
- Ask for your course content folder path
- Optionally configure a TTS voice
- Install `/learn` globally so it works in any future project

That's it. Type `/learn 0.1` to start the first lesson.

---

## Usage

```
/learn setup        — configure language, TTS, and course path (run once)
/learn 0.1          — start lesson 0.1
/learn 1.3          — start lesson 1.3
/learn              — open menu: choose lesson or project analysis
```

### Commands during a session

| Command | Action |
|---------|--------|
| `continue` | Move to the next section |
| `quiz me` | 4-question quiz on everything covered so far |
| `explain again` | Re-explain current section from a different angle |
| `summary` | Bullet-point recap of what was covered |
| `exercises` | Show this lesson's exercises |
| `stop` | End session — shows what's covered, what's left, next recommendation |
| `read aloud` | Speak the last response (on-demand TTS) |
| `settings` | Show current language, TTS, and course path |

---

## What the Tutor Does

Every section is taught using the **Journey Format**:
1. **The problem** — why this matters
2. **The insight** — what experts understand that beginners don't
3. **In your project** — connects the concept to your actual work
4. **Question** — one thinking question before moving on

After quizzes, the tutor tracks your score and tells you when to review the lesson again (spaced repetition: 2 / 13 / 34 / 89 days based on score).

---

## Course Content Structure

Lessons live in `courses/[course-name]/lessons/`:

```
courses/
  ai-engineer/
    COURSE.md
    lessons/
      00-ai-fundamentals/
        0.1-intro-to-ai/
          0.1_script.txt       ← lesson script (split by [מעבר שקף])
          0.1_exercises.md     ← exercises
      01-prompt-engineering/
        ...
```

The tutor auto-detects lesson files by number — `/learn 0.1` finds `0.1_script.txt` automatically.

---

## Files Created at Runtime

All learner data is saved to `~/skill-tutor-tutorials/` (outside the repo):

```
~/skill-tutor-tutorials/
├── settings.json           — language, TTS config, course path
├── learner_profile.md      — background, current project, learning style
├── tutorials/              — per-lesson notes, key insights, Q&A
├── progress/               — quiz scores and next review dates
├── topics/knowledge_map.md — full map of mastered vs. in-progress topics
└── architectures/          — HTML architecture diagrams (from project analysis)
```

---

## Project Structure

```
.claude/commands/
  learn.md                  ← entry point + routing
  learn/
    setup.md                ← first-run configuration
    teaching.md             ← lesson loop + Journey format
    quiz.md                 ← quiz format + spaced repetition
    progress.md             ← saving tutorials and knowledge map
    project-analysis.md     ← codebase scan + architecture map
    display.md              ← visual formatting conventions
courses/
  ai-engineer/              ← course content
CLAUDE.md                   ← architecture overview for contributors
```

---

## Adding a New Module

1. Create `.claude/commands/learn/[module-name].md`
2. Add a row to the modules table in `CLAUDE.md`
3. Add a routing entry in `learn.md` (Step 2 — Route table)
4. Update the global install command in `setup.md`

---

## Requirements

- Claude Code (Pro plan or higher)
- Windows (for TTS voice support) — TTS can be disabled on any OS

## License

MIT
