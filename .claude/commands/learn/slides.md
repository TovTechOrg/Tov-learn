# Slides Module

*Loaded when the learner types `/learn slides` or "slides" during a session. Switches to verbatim slide reading mode.*

Respond in `session.language` throughout.

---

## Overview

Slides Mode reads the course script verbatim — no Journey Format, no reformulation. The learner hears the slides exactly as written, translated to `session.language` if needed. Exercises are still written by the tutor (not taken from the exercises file verbatim).

---

## Step 1 — Resolve Lesson

If a lesson number was specified (e.g. `/learn slides 3.1`), load that lesson's script file.

If no lesson number was given, use the current lesson already loaded in the session. If no lesson is active, ask the learner which lesson they want.

Resolve the script path using the same priority as `teaching.md`:
1. Check `./lessons/` at project root
2. Fallback to `course.path` from settings

Split the script by `[מעבר שקף]`.

---

## Step 2 — Announce Mode

Tell the learner:
> "Switching to Slides Mode. I'll read each slide verbatim. Say **next** to advance, **stop slides** to return to teaching mode, or **exercises** to get the exercises for this lesson."

---

## Step 3 — Read Slides Verbatim

For each slide:
1. Display the slide content as-is (translated to `session.language` if the script is in a different language)
2. Open the slide image in the browser using PowerShell:
   - Slide images are at: `C:\Users\yuval\ai-track\courses\ai-engineer\lessons\[module]\[lesson]\digital-course-screenshots\slide-NN.png`
   - Use zero-padded numbers: slide-01.png, slide-02.png, etc.
   - Run this PowerShell to open the image:
   ```powershell
   Start-Process "SLIDE_IMAGE_PATH"
   ```
3. Run TTS from the per-slide TTS script file if it exists:
   - TTS scripts are at: `C:\Users\yuval\ai-track\courses\ai-engineer\lessons\[module]\[lesson]\digital-course-tts-scripts\slide-NN.txt`
   - Read the file content and speak it using the TTS helper
   - If no TTS script file exists, speak the slide text directly
4. Wait for the learner to say **next** before advancing

**Do not** apply Journey Format. **Do not** ask thinking questions between slides.

---

## Step 4 — Exercises

When the learner says **exercises**:
- Do NOT read from the exercises file verbatim
- Write fresh, interactive exercises based on the slide content covered so far
- Follow the exercise design rule: most exercises completable through Claude directly; external tool exercises only when the lesson topic is that specific tool

---

## Step 5 — Exit Slides Mode

When the learner says **stop slides** or **teaching mode**:
- Return to the teaching module (`teaching.md`) at the slide where they left off
- Resume in the previously set `session.detail_level`
