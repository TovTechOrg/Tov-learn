# Slides Module

*Loaded when the learner types `/learn slides` or "slides" during a session. Switches to verbatim slide reading mode.*

Respond in `session.language` throughout. Address the learner using `session.address`.

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

## Step 4 — Per-Slide Loop

Repeat this sequence for every slide, starting at slide 1:

**a. Display text** — show the verbatim slide content (translated to `session.language`).

**b. Fire TTS — MANDATORY, do not skip.** Immediately after displaying the text, run:
```powershell
Invoke-RestMethod -Uri "http://localhost:7823/" -Method POST -Body "SLIDE_NUMBER" | Out-Null
```
Replace `SLIDE_NUMBER` with the current slide number (integer). This tells the server to speak the slide and sync the viewer. TTS fires automatically on every slide — the learner should never have to ask for it.

**c. Wait** for the learner to say **next** before advancing.

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
