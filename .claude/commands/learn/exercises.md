# Exercises — Shared Rules (reference)

*Reference module, not routed. `teaching.md` and `slides.md` follow these rules whenever they give a lesson's exercises. Read this file before starting a lesson's exercises.*

Respond in `session.language` throughout. Address the learner using `session.address`.

---

## Principle

**Every exercise of every lesson is done before moving on to the next lesson.** Exercises are not optional. After a failed skip quiz, only the exercises related to the sections the learner got wrong are required (see "After a failed skip quiz" below). The only other exception is an exercise that needs a paid resource that isn't provided and has no free way around it (see "Paid resources" below) — and even then it's skipped only after the free ways and an adapted version of the exercise were tried, and it's flagged for the mentors. Learning never waits for a mentor's answer.

---

## Tracking file

All tracking lives in `~/skill-tutor-tutorials/progress/exercises-lesson-{lesson_number}.md`.

**1. When the exercises start** — before presenting the first exercise — if the file doesn't exist, create it with this header (fill in the number of exercises you're about to give):

```
# תרגילים — שיעור {lesson_number}
**נדרשים:** [N]
```

Right under the header, save the **plan** — the exercises you're about to give, in order, under a heading that is not `## תרגיל` (so it isn't counted as done):

```
## תוכנית
- [n] — [exercise title]
```

When the exercises are fresh ones you wrote yourself (slides mode), save each one's full text under its plan line, indented, so a later conversation gives exactly the same exercise. Nothing in the plan may start a line with `## תרגיל` — only done exercises use that heading, and the lesson-order check counts them.

This marks the exercises as started. If the file already exists (e.g. the learner is coming back to finish), read it and continue with the first exercise in the plan that isn't recorded yet, under the same number and with the same text — never re-choose or rewrite the remaining exercises. (A file from before plans were saved has no plan: continue from the first exercise that isn't recorded.)

**2. After each exercise's feedback has been shown to the learner** (never before it), silently append:

```
## תרגיל [n] — [exercise title]
**תשובה:** [learner's answer, verbatim or summarized if long]
**פידבק:** [your feedback in one sentence]
---
```

**3. If an exercise is skipped** under the paid-resources rule, append instead:

```
## תרגיל [n] — [exercise title] (דולג — דורש תשלום)
**סיבה:** [one sentence — what's needed and why it isn't available for free]
---
```

The lesson's exercises are **complete** when the number of `## תרגיל` entries (completed + skipped) equals **נדרשים**.

Don't tell the learner you are saving.

---

## After a failed skip quiz

When the lesson was taught only partly because the learner's skip quiz scored below 8 (`teaching.md` Step 3B, or `slides.md` Step 1B; `session.failed_skip_quiz = true`), only the exercises that relate to at least one of the sections the learner got wrong (`session.weak_sections`) are required. In teaching mode, choose them from the course's exercises file and keep their original numbers (e.g. 1, 2 and 4). In slides mode, write fresh exercises on those slides only (`slides.md`, Step 4), numbered 1, 2, 3…. Set **נדרשים** to their number, and note why in the header:

```
# תרגילים — שיעור {lesson_number}
**נדרשים:** [N] (רק התרגילים שקשורים לנושאים שנענו לא נכון במבחן הדילוג)
```

Tell the learner briefly which exercises these are and why. If no exercise relates to those sections, **נדרשים** is 0 and the lesson has no required exercises. The paid-resources rule below still applies to the chosen exercises.

---

## Paid resources

Some exercises need an external service, tool, or API key. Before starting such an exercise:

1. **Check the course's resource list** — the `## משאבים` section of the active course's `COURSE.md`. If the resource is listed as free or provided (including tools Tov-Tech pays for), just do the exercise.
2. **If it seems to need payment**, don't skip. Suggest every free way you know to get what the exercise needs — a free tier, an equivalent free service, or a local tool that serves the same learning goal — and help the learner try them, one at a time. **A free trial is not a free way**: it uses up a trial the learner may want later for their own work. Don't suggest one.
3. **If none of the free ways work, adapt the exercise.** Write a variation that keeps the same learning goal but uses only free tools or tools Tov-Tech provides (`## משאבים`) — e.g. a different free service, a local tool, or a simulated input instead of a paid API. Present it in the conversation as an adapted version of exercise [n], say what changed and why, and do it with the learner like any other exercise. It counts as that exercise: record it under the same number, with `(גרסה מותאמת)` after the title. The course files stay unchanged.
4. **Only if no adapted version can keep the learning goal** — skip the exercise:
   - Record it in the tracking file as skipped (format above).
   - Append a flag to `~/skill-tutor-tutorials/progress/exercise-flags.md` (create if missing):
     ```
     ## [YYYY-MM-DD] — שיעור [X.Y], תרגיל [n]: [exercise title]
     **משאב נדרש:** [service / key / tool]
     **ניסיונות חינמיים:** [each free way tried, and why it didn't work]
     **התאמה:** [why no adapted version with free tools could keep the learning goal]
     **נימוק:** [why the exercise can't be done for free]
     ---
     ```
   - Tell the learner the exercise was skipped and flagged for the mentors to review, and continue with the next exercise. The learner doesn't wait for a mentor's answer at any step.
   - **Never edit or remove course files** (scripts, exercises, COURSE.md). Flags are for the mentors to review; they decide whether to change the course.

---

## Unfinished exercises from an earlier lesson

A lesson can't start while an earlier lesson's required exercises are incomplete. A hook notes this when the lesson starts; `order.md` says what to do (complete the remaining exercises following the rules above, then continue in order).
