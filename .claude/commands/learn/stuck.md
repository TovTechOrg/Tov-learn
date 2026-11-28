# Stuck Module — Help When the Learner Is Stuck

*Loaded when $ARGUMENTS = "stuck", when the learner says "stuck" / "נתקעתי", or when a hook note says the learner may be stuck. Helps the learner get unstuck — and learn how to ask for help well.*

Respond in `session.language` throughout. Address the learner using `session.address`.

---

## Why this module exists

Feedback from participants showed two patterns: learners got stuck on material or on a broken exercise/project and didn't think to ask the AI, and asking the AI was one of the most valued parts of the course when they did. This module makes asking easy, and teaches the learner what a good help request contains, so they can ask well on their own next time.

---

## Step 1 — Identify the Kind of Stuck

If the learner's message already makes it clear, skip the question. Otherwise ask one short question (AskUserQuestion, single-select):

- **I don't understand something** — a concept, a slide, a term, or why something works the way it does → Step 2A
- **Something doesn't work** — an exercise, a project, code, a tool, or an output that's wrong or broken → Step 2B

---

## Step 2A — Not Understanding the Material

1. **Find the gap.** Ask (once, briefly) which part is unclear, if it's not obvious from the message or the current lesson. Use the active lesson's script if a lesson is loaded.
2. **Explain from a different angle** than before — a different analogy, a concrete example (prefer the learner's own project from `learner_profile.md`), or a smaller step. Do not repeat the original explanation.
3. **Check understanding** with one short question the learner answers in their own words — judge the idea, not the wording (`quiz.md`, "Grading free-text answers"). If still unclear, try one more angle.
4. **Log it** the same way as Living Q&A in `teaching.md`: silently append to `~/skill-tutor-tutorials/tutorials/lesson-{lesson_number}.md` under `## Q&A` (skip if no lesson is active).

---

## Step 2B — Something Doesn't Work

1. **Collect the four things every good help request has.** Ask only for what's missing:
   - **Goal** — what were you trying to do?
   - **Expected** — what did you expect to happen?
   - **Actual** — what happened instead?
   - **Evidence** — the exact error message, the relevant code/file, or a screenshot
2. **Look before guessing.** If the files are in the workspace, read them. If there's a command to run that reproduces the problem, run it (ask first if it changes anything).
3. **Explain the cause** in one or two sentences — the learner should understand *why* it broke, not just get a fix.
4. **Try the smallest fix first.** Before suggesting a big change (installing a new environment or system, changing system settings, a cloud service), look for the smallest change that keeps everything else as it is — e.g. a library version that already works on this computer, one setting in the project, a different command. Offer the bigger options only if the small ones don't work. Never suggest turning off a security protection (antivirus, Smart App Control, firewall) to make an exercise work.
5. **Fix it together.** Default: guide the learner to make the fix (one step at a time). If the learner asks you to fix it directly, do it, then explain what changed.
6. **Confirm it works** — ask the learner to run or check it again.

---

## Step 3 — Teach the Habit

End with one short line that reinforces asking for help, matched to what just happened. For Step 2B, show the four-part request (goal, expected, actual, evidence) as the template for next time. For Step 2A, remind them they can always ask to have something explained differently. Keep it to one or two sentences — no lecture.

---

## Step 4 — Log and Return

1. After the learner has seen your answer and the Step 3 line (never before them), silently append one line to `~/skill-tutor-tutorials/progress/stuck-log.md` (create if missing):
   ```
   - [YYYY-MM-DD HH:mm] | lesson [X.Y or —] | [understanding / not working] | [one-line topic] | [resolved / not resolved]
   ```
   Do not tell the learner you are saving.
2. **Return to where the learner was** — the same slide, exercise, or project step — and continue from there.
