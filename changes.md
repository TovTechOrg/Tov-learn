# Changes — sean_changes branch

Modifications made while testing the `/learn` user flow on the AI Dev course (lesson 1.1) and streamlining the repo.

---

## 1. Quiz flow redesign — [quiz.md](.claude/commands/learn/quiz.md)

**Before:** 4 open-ended questions, asked one at a time (back-and-forth).

**After:**
- **Normal `quiz me`** — 4 multiple-choice questions batched into a single `AskUserQuestion` box, then **1 free-text recall question** at the end.
  - Multiple-choice = token-efficient and fast UX (recognition).
  - The free-text closer preserves the stronger recall test without back-and-forth.
  - Each MC question has 1 correct + 2–3 plausible distractors; the auto-added "Other" option lets the learner free-text any answer.
- **New `quiz me full` mode** — 8 multiple-choice (two boxes of 4) + 1 free-text synthesis closer, drawn from the **whole** lesson script.
  - No hardcoded section count — scales to whatever sections a lesson has.
  - Reads prior **Quiz History** and **varies the questions** on repeat attempts, keeping them correct and on-topic.
- **Scoring rubric (1–10):**
  - Normal: each MC = 1.5 pts (6 total) + free-text up to 4 pts.
  - Full: each MC = 1 pt (8 total) + free-text up to 2 pts.

## 2. Quiz routing — [learn.md](.claude/commands/learn.md)

- Added `quiz me full` to the Learner Commands table; clarified `quiz me` is scoped to covered sections.

## 3. Global install made opt-in — [setup.md](.claude/commands/learn/setup.md)

**Before:** Section F always copied the skill files to `~/.claude/commands/` (global).

**After:** Global install is **optional, defaulting to off**.
- `/learn` works inside this repo with no install step (the primary goal: learn the material in this repo).
- Setup now asks whether to also install globally (for the future cross-repo use case); most learners say no.
- Avoids a second source of truth / stale copies when repo modules are edited.
- Learner *data* (`~/skill-tutor-tutorials/`) stays per-user and outside the repo — unchanged.

## 4. Docs — [CLAUDE.md](CLAUDE.md)

- "Adding a module" checklist no longer treats global install as required; notes repo-local is the default.

---

## Possible follow-up (not yet implemented)

- A normal `quiz me` can mark a lesson as "Mastered" (score 8+) even if only a few sections were covered. Consider requiring full coverage — or `quiz me full` — before granting mastery in the knowledge map.
