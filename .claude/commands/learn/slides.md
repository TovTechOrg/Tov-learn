# Slides Module

*Loaded when the learner types `/learn slides` or "slides" during a session. Switches to verbatim slide reading mode.*

Respond in `session.language` throughout. Address the learner using `session.address`.

---

## Overview

Slides Mode reads the course script verbatim — no Journey Format, no reformulation. The learner hears the slides exactly as written, translated to `session.language` if needed. Exercises are still written by the tutor (not taken from the exercises file verbatim), and are always given at the end of the lesson (Step 5).

---

## Step 1 — Resolve Lesson

If a lesson number was specified (e.g. `/learn slides 3.1`), load that lesson's script file.

If no lesson number was given, use the current lesson already loaded in the session. If no lesson is active, ask the learner which lesson they want (lessons go in course order — `order.md`).

Resolve the script path using the same priority as `teaching.md`:
1. Check `./lessons/` at project root
2. Fallback to `course.path` from settings

Split the script by `[מעבר שקף]`.

**Mark the lesson as taught under the exercises rule** — once the lesson actually begins (after any lesson-order note is handled, `order.md`): silently create or update `~/skill-tutor-tutorials/progress/lesson-{lesson_number}.md` so it contains the line `**Exercises required:** yes` (keep everything else already in the file). It tells the lesson-order check that this lesson follows the current rules, unlike lessons learned before them. Do not tell the learner you are saving.

---

## Step 1B — Learn the Lesson, or Quiz First

The same choice as `teaching.md` Step 3, at the start of every lesson (not when switching into slides mode in the middle of a lesson, or coming back to finish a lesson already in progress): ask whether to learn the lesson or take its skip quiz first, with the same wording and rules. At the first lesson of a module, also offer the module skip quiz.

- **Learn** → continue with Step 2 and read all the slides.
- **Quiz first** → follow `teaching.md` Step 3B — the quiz, pass mark 8, what to save, and the detailed explanations after a pass — with one difference for a score below 8: instead of teaching the weak sections in the Journey Format, read **only the slides behind the wrong answers**, verbatim, in the chat, one at a time (the learner says **next**). Don't launch the viewer — it plays the whole lesson. After the last of those slides, go to Step 5; only the exercises related to them are required.

---

## Step 2 — Announce Mode

Tell the learner:
> "Switching to Slides Mode. I'll read each slide verbatim. Say **next** to advance, **stop slides** to return to teaching mode, or **exercises** to get the exercises for this lesson."

---

## Step 3 — Launch Viewer

On entry to Slides Mode, start the slide server and generate the HTML viewer:

1. **Start the server** (if not already running on port 7823). Reference the script relative to the repo root (`$PWD` is the project directory during a session):
   ```powershell
   Start-Process powershell -ArgumentList "-NoProfile -File `"$PWD\.claude\scripts\slide-server.ps1`"" -WindowStyle Normal
   Start-Sleep -Seconds 2
   ```

2. **Resolve the lesson's absolute path** on disk — the lesson directory resolved in Step 1 (under `course.path`). The viewer expects two optional asset subfolders inside that lesson directory:
   - Slide images: `[LESSON_DIR]\digital-course-screenshots\`
   - TTS scripts: `[LESSON_DIR]\digital-course-tts-scripts\`

   These asset folders ship with some courses only. If the active course's lesson has neither folder, skip the viewer launch (Step 3) and read the script text verbatim in the chat instead.

3. **Generate and open the viewer**:
   ```powershell
   & "$PWD\.claude\scripts\generate-slideshow.ps1" -LessonPath "ABSOLUTE_LESSON_PATH"
   Start-Process "$env:TEMP\tov_slideshow.html"
   ```

---

## Step 4 — Viewer Launched — Go Silent

**Once the viewer is open, stop generating slide content. The viewer handles TTS and navigation entirely. Claude output = 0 tokens per slide.**

Tell the learner:
> "הויואר פתוח. לחץ **A** (או כפתור ⏭ אוטו) להפעלה אוטומטית ידנית. ← / → לניווט ידני. P להשהיה."

Then **wait silently** for the learner to say something (e.g. "stop slides", a question, "exercises").

**Do NOT:**
- Type out slide content
- Call `Invoke-RestMethod` per slide — the viewer calls `postSlide()` automatically on every slide change
- Count slides or narrate progress
- Do anything until the learner speaks

**Manual mode** (learner didn't enable auto): learner uses keyboard/clicks in the viewer, TTS fires automatically via `postSlide()` inside the viewer.

**Auto mode** (learner pressed A or the Auto button): viewer auto-advances on `speaking→idle` TTS transition — completely hands-free, 0 Claude involvement.

**Do not** apply Journey Format. **Do not** ask thinking questions between slides.

---

## Step 4 — Exercises

When the learner says **exercises** (and always at the end of the lesson — see Step 5):
- First read `.claude/commands/learn/exercises.md` and follow it: create the tracking file `~/skill-tutor-tutorials/progress/exercises-lesson-{lesson_number}.md` with its header before the first exercise, and apply its paid-resources rule
- Do NOT read from the exercises file verbatim
- Write fresh, interactive exercises based on the slide content covered so far
- Follow the exercise design rule: most exercises completable through Claude directly; external tool exercises only when the lesson topic is that specific tool
- Present them one at a time, wait for the learner's answer, and give specific feedback on each. If the learner is stuck, give one hint — not the answer
- **After each exercise is completed**, silently append the learner's answers to `~/skill-tutor-tutorials/progress/exercises-lesson-{lesson_number}.md`, in the format from `exercises.md`:
  ```
  ## תרגיל [N] — [exercise title]
  **תשובה:** [learner's answer, verbatim or summarized if long]
  **פידבק:** [your feedback in one sentence]
  ---
  ```
  Create the file if it doesn't exist. Do not tell the learner you are saving.

---

## Step 5 — End of Lesson / Exit

**When the last slide is reached** (after a failed skip quiz: the last of the slides behind the wrong answers):
1. Tell the learner they've finished the lesson's slides. **Mark the lesson's slides as done — silently, right away, before the exercises.** Create or update `~/skill-tutor-tutorials/progress/lesson-{lesson_number}.md` so it contains the lines `**Slides covered:** all [N]` and `**Exercises required:** yes` (keep everything else already in the file). This is how later lessons know this lesson's slides were finished and its exercises are required, even if the learner stops in the middle of the exercises (`order.md`). Do not tell the learner you are saving.
2. **Exercises — always, never skip.** Run the exercises flow from Step 4, even if the learner didn't ask for it. Exercises are part of every lesson, not an optional extra. If exercises for this lesson were already completed earlier in this session, skip this step. If `session.failed_skip_quiz` is true, give only the exercises related to the slides the learner got wrong (`exercises.md`, "After a failed skip quiz").
3. **Quiz, mini project, or neither — optional, offer once.** Tell the learner plainly that this step is optional and that they can go on to the next lesson without it. They choose at most one:
   - **Quiz** — 3–5 questions on the lesson content, one at a time
   - **Mini project** — 2–3 prompt hands-on task (not external tool unless that's the lesson topic)
   - **Neither** — go to step 4.

   Neither the quiz nor the mini project is required before the next lesson — only the exercises are.
4. **Save progress silently** — after the exercises (and the quiz or mini project, if the learner chose one), write to `~/skill-tutor-tutorials/progress/lesson-{lesson_number}.md`:
   ```
   # Progress — Lesson X.Y

   **Completed:** [timestamp]
   **Slides covered:** all [N]
   **Summary:** [2–3 sentence summary of what was covered]
   ```
   Preserve any existing content in the file (quiz scores, the `**Slides covered:**` and `**Exercises required:**` lines from step 1). Do not tell the learner you are saving.

**When the learner says `stop slides` or `teaching mode`:**
- Save progress with slides covered so far (not "all [N]" — note actual last slide reached)
- Return to the teaching module at the slide where they left off
- Resume in the previously set `session.detail_level`
