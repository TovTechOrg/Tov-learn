# Setup Module

*Loaded by learn.md when settings.json is missing or $ARGUMENTS = "setup".*

Respond in the language the user answers with in section B. Default to Hebrew if unclear.

---

## A. Show Current Settings

If `~/skill-tutor-tutorials/settings.json` exists, display a friendly summary table showing: session language, course path, TTS enabled/disabled, voice name, TTS language, speed, and mode.

If the file does not exist — skip directly to section B.

---

## B. Session Language

Ask: "In which language would you like the session to run? (Hebrew / English)"

Set `session.language` to `"he"` or `"en"`. Use this language for all communication from this point on.

---

## C. Course Selection

Use the `AskUserQuestion` tool to display a course picker:

```
question: "באיזה קורס תרצה ללמוד?"
header: "בחירת קורס"
options:
  - label: "AI Dev"
    description: "פיתוח מוצרי AI עם Claude Code ו-API (ברירת מחדל)"
  - label: "AI Engineer"
    description: "אוטומציות ו-AI לאנשי ביזנס ומקצוע"
  - label: "נתיב מותאם אישית"
    description: "הגדרת נתיב קורס ידנית"
```

Map the selection to settings:

| בחירה | course.name | course.path |
|-------|-------------|-------------|
| AI Dev | `ai-dev` | `courses/ai-dev/lessons` |
| AI Engineer | `ai-engineer` | `courses/ai-engineer/lessons` |
| נתיב מותאם אישית | (שאל שם) | (שאל נתיב) |

If the learner types "Other" with free text — treat as custom path.

---

## D. TTS Setup

Ask: "Would you like the tutor to speak aloud? (yes / no)"

**If yes:**

1. Run PowerShell to list available voices:
```powershell
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Media.SpeechSynthesis.SpeechSynthesizer,Windows.Media.Speech,ContentType=WindowsRuntime]
[Windows.Media.SpeechSynthesis.SpeechSynthesizer]::AllVoices | ForEach-Object { "$($_.DisplayName) — $($_.Language)" }
```

2. Show the list and ask which voice they want.

3. Ask for speaking rate: 0 = normal, -5 = very slow, 5 = very fast.

4. Ask for TTS mode: (a) automatic — speaks after every response, (b) on-demand — only when triggered.

5. Test the voice by speaking a greeting in the configured session language.

6. Ask: "Does it sound good? (yes / no / change)" — if "change", go back to step 2.

**If no:** set `tts.enabled = false`.

---

## E. Save Settings

Save `~/skill-tutor-tutorials/settings.json`:

```json
{
  "session": {
    "language": "he"
  },
  "course": {
    "name": "ai-dev",
    "path": "courses/ai-dev/lessons"
  },
  "tts": {
    "enabled": true,
    "voice_name": "[selected voice name]",
    "voice_lang": "[voice language code]",
    "rate": 0,
    "mode": "auto"
  }
}
```

---

## F. Global Install

Copy all skill files to the global Claude commands folder:

```powershell
$dest = "$env:USERPROFILE\.claude\commands"
if (!(Test-Path $dest)) { New-Item -ItemType Directory -Force -Path $dest | Out-Null }
Copy-Item -Force "$PWD\.claude\commands\learn.md" "$dest\learn.md"

$moduleDest = "$dest\learn"
if (!(Test-Path $moduleDest)) { New-Item -ItemType Directory -Force -Path $moduleDest | Out-Null }
Copy-Item -Force "$PWD\.claude\commands\learn\*.md" "$moduleDest\"
```

Confirm to the learner that settings are saved and `/learn` is now available globally in any project.
