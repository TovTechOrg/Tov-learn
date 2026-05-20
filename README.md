# Tov-learn

Interactive AI tutor for the TovTech AI Engineer course by Raz Hadas.

## What it does

`/learn` is a Claude Code skill that acts as a personal tutor (Tal) for the AI Engineer course. It:

- Teaches lessons interactively using the Journey format (problem → insight → your project → question)
- Adapts explanations to the learner's profile and current project
- Tracks progress, quiz scores, and spaced repetition schedules
- Supports TTS (text-to-speech) via Windows Speech API
- Can analyze a project's architecture and generate a visual HTML map

## Installation

1. Copy `.claude/commands/learn.md` into your project's `.claude/commands/` directory
2. Copy `skill-tutor-tutorials/settings.template.json` to `~/skill-tutor-tutorials/settings.json` and edit it
3. Open Claude Code and run `/learn setup` to configure language, TTS, and course path

## Usage

```
/learn setup          — configure voice, language, course path
/learn 0.3            — start lesson 0.3
/learn 1.1            — start lesson 1.1
/learn                — open menu (lesson or project analysis)
```

## Commands during a session

| Command | Action |
|---------|--------|
| `continue` | Skip to next section |
| `quiz me` | Run a 4-question quiz on covered material |
| `explain again` | Re-explain current section from a different angle |
| `summary` | Bullet-point summary of everything covered |
| `exercises` | Show lesson exercises |
| `stop` | End session with next-step recommendation |
| `read` | Speak last response aloud (on-demand TTS) |
| `settings` | Show current TTS and session settings |

## Directory structure created at runtime

```
~/skill-tutor-tutorials/
├── settings.json           — TTS, language, course path
├── learner_profile.md      — background, project, learning style
├── tutorials/              — per-lesson notes and Q&A
├── progress/               — quiz scores and spaced repetition dates
├── topics/                 — knowledge map across lessons
└── architectures/          — HTML architecture diagrams (project analysis mode)
```

## Requirements

- Claude Code (Pro plan or higher)
- Windows TTS voices (for voice mode) — or disable TTS in settings
- Course content folder with `digital-course-script.txt` per lesson

## License

MIT
