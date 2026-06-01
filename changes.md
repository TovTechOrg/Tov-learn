# Changes — yuval_ver branch

## Overview

Three additions to the `/learn` skill system, focused on giving the learner more control over how they experience course content.

---

## 1. Detail Levels (`detail 1 / 2 / 3`)

**What changed:** `teaching.md`, `learn.md`

The learner can now type `detail 1`, `detail 2`, or `detail 3` at any point during a session to change how deeply Claude explains each slide.

| Level | Behavior |
|-------|----------|
| `detail 1` | 1–2 sentences per slide — just the core idea, no follow-up question |
| `detail 2` | Full Journey Format, max 5 sentences — the default |
| `detail 3` | Journey Format + extended insight + bullet points with extra context |

Claude now asks for the preferred detail level at the start of each session so learners don't have to discover this themselves.

**Why:** Some learners are already familiar with parts of the material and want to move faster. Others want a deeper dive. This makes the tutor adapt to the learner rather than forcing everyone through the same pace.

---

## 2. Cover Every Slide Rule

**What changed:** `teaching.md`

Claude is now required to cover every slide in the lesson — no skipping, no merging slides silently. If a slide is short or repetitive, it may summarize briefly (according to the active detail level), but it must represent every slide.

**Why:** Previously Claude could skip slides it deemed redundant. Learners were missing content without knowing it.

---

## 3. Slides Mode (`/learn slides` or `slides` command)

**What changed:** `learn.md` (routing), new file `slides.md`, new scripts `slide-server.ps1` + `generate-slideshow.ps1`

A new mode the learner can switch into at any time. Instead of Claude's teaching format, the learner sees and hears the actual course slides verbatim.

**How it works:**
- Claude opens an interactive browser window showing the real slide images from the course
- The existing הבא / הקודם buttons in the slide images are made clickable via transparent overlays
- Extra controls are added: ⏸ השהה (pause TTS) and ⛶ מסך מלא (fullscreen)
- A local server (`localhost:7823`) keeps the browser viewer and Claude in sync — if Claude advances, the browser follows, and vice versa
- TTS reads the official course script for each slide automatically — no manual trigger needed
- Exercises in this mode are still written fresh by Claude (not pulled verbatim from the exercises file)

**Learner commands in this mode:**

| Command | Action |
|---------|--------|
| `next` | Advance to next slide |
| `stop slides` | Return to teaching mode at the current slide |
| `exercises` | Get fresh exercises based on slides covered so far |

**Supporting scripts** (in `.claude/scripts/`):
- `slide-server.ps1` — preloads all TTS scripts at startup, speaks via Windows TTS on every slide change, handles pause/resume
- `generate-slideshow.ps1` — generates the HTML viewer for any lesson, positions click overlays over the existing nav buttons in the slide images

**Why:** Some learners want to experience the slides the way they were designed — visually, with the recorded voiceover — rather than Claude's reformulation. This mode gives them that while keeping Claude available for exercises and Q&A.

---

## File Map

| File | Status | Purpose |
|------|--------|---------|
| `.claude/commands/learn.md` | Modified | Added slides routing + detail 1/2/3 and slides to learner commands |
| `.claude/commands/learn/teaching.md` | Modified | Cover-every-slide rule, detail levels, ask preference at session start |
| `.claude/commands/learn/slides.md` | New | Slides Mode — verbatim reading, viewer launch, TTS loop |
| `.claude/scripts/generate-slideshow.ps1` | New | Generates interactive HTML slide viewer |
| `.claude/scripts/slide-server.ps1` | New | Local TTS + slide state server on localhost:7823 |
| `CLAUDE.md` | Modified | Added Slides to modules table, noted scripts folder |
