# Setup Module

*Loaded by learn.md when settings.json is missing or $ARGUMENTS = "setup".*

Respond in the language the user answers with in section B. Default to Hebrew if unclear.

---

## A. Show Current Settings

If `~/skill-tutor-tutorials/settings.json` exists, display a friendly summary table showing: session language, course path, TTS enabled/disabled, voice name, TTS language, speed, and mode.

If the file does not exist — skip directly to section B.

---

## B. Session Language

Use the `AskUserQuestion` tool:

```
question: "In which language would you like the session to run?"
header: "Session Language"
options:
  - label: "עברית"
    description: "המערכת תתקשר איתך בעברית"
  - label: "English"
    description: "The system will communicate with you in English"
```

Set `session.language` to `"he"` or `"en"`. Use this language for all communication from this point on.

---

## B.1. פנייה אישית (עברית בלבד)

**Run this section only if `session.language == "he"`. Skip entirely if English was selected.**

Use `AskUserQuestion`:

```
question: "איך להתייחס אליך בשיחה?"
header: "פנייה"
options:
  - label: "אתה (יחיד זכר)"
    description: "פנייה בלשון זכר"
  - label: "את (יחיד נקבה)"
    description: "פנייה בלשון נקבה"
  - label: "ניטרלי / מעורב"
    description: "ללא פנייה מגדרית — מתאים לקבוצות מעורבות או העדפה אישית"
  - label: "רבים / רבות"
    description: "פנייה בלשון רבים — ציין אם זכר (אתם) או נקבה (אתן)"
```

*(The tool auto-adds an "Other" option for free text — use that value as-is.)*

Save the result as `session.address`. Examples:
- "אתה (יחיד זכר)" → `"masculine"`
- "את (יחיד נקבה)" → `"feminine"`
- "ניטרלי / מעורב" → `"neutral"`
- "רבים / רבות" → `"plural-m"` or `"plural-f"` (ask follow-up if needed)
- free text → save verbatim as `"other:<text>"`

**Use `session.address` for all Hebrew communication from this point on.**

---

## B.2. RTL Extension for Hebrew Users

**Run this section only if `session.language == "he"`. Skip entirely if English was selected.**

First, check if the extension is already installed:

```powershell
code --list-extensions | Select-String "yechielby.claude-code-rtl"
```

**If already installed:** skip this section entirely — no message needed.

**If not installed:** use `AskUserQuestion`:

```
question: "האם להתקין את תוסף ה-RTL?"
header: "תוסף RTL"
options:
  - label: "כן, התקן"
    description: "yechielby.claude-code-rtl — משפר תצוגת עברית ב-Claude Code"
  - label: "לא תודה"
    description: "דלג על שלב זה"
```

**If yes:** first tell the user:

> "מתקין את התוסף. שים לב שהתקנה עלולה לקטוע את השיחה — אם זה יקרה: אם השיחה עדיין פתוחה, כתוב **המשך**; אם נסגרה, פתח שיחה חדשה וכתוב **`/learn setup`**."

Then run:

```powershell
code --install-extension yechielby.claude-code-rtl
```

After the command completes, add:

> "לאחר שה-extension ייטען, הפעל מצב אוטומטי פעם אחת:
> `Ctrl+Shift+P` ← **Activate RTL (Auto)**
>
> **למה זה חשוב?** בלי מצב זה, כל הטקסט מוצג משמאל לימין — עברית מופיעה הפוכה, פסקאות מתחילות בצד הלא נכון, והקריאה מסורבלת. מצב Auto מזהה לבד איזה בועת שיחה היא עברית ואיזו אנגלית, ומסדר כל אחת בכיוון הנכון — בלי שתצטרך לעשות כלום.
>
> התוסף מוסיף כפתור קטן בשורת הסטטוס בתחתית המסך — משם ניתן בכל עת לשנות מצב או לבטל לחלוטין."

**If no:** skip silently and continue to section C.

---

## C. Course Selection

Use the `AskUserQuestion` tool to display a course picker:

```
question: "באיזה מסלול תרצה ללמוד?"
header: "בחירת מסלול"
options:
  - label: "AI Dev"
    description: "פיתוח מוצרי AI עם Claude Code ו-API (המסלול הפעיל היחיד)"
  - label: "נתיב מותאם אישית"
    description: "הגדרת נתיב מסלול ידנית"
```

Map the selection to settings:

| בחירה | course.name | course.path |
|-------|-------------|-------------|
| AI Dev | `ai-dev` | `courses/ai-dev/lessons` |
| נתיב מותאם אישית | (שאל שם) | (שאל נתיב) |

> מסלול ה-AI Engineer הועבר לארכיון תחת `courses/_archive/ai-engineer/`. אם לומד צריך אותו — אפשר להזין נתיב מותאם אישית: `courses/_archive/ai-engineer/lessons`.

If the learner types "Other" with free text — treat as custom path.

---

## D. TTS Setup

Use the `AskUserQuestion` tool:

```
question: "האם תרצה שהמורה ידבר בקול?"
header: "קול מורה"
options:
  - label: "כן"
    description: "המערכת תקרא את התשובות בקול"
  - label: "לא"
    description: "טקסט בלבד"
```

**If yes:**

1. Run PowerShell to list available voices:
```powershell
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Media.SpeechSynthesis.SpeechSynthesizer,Windows.Media.Speech,ContentType=WindowsRuntime]
[Windows.Media.SpeechSynthesis.SpeechSynthesizer]::AllVoices | ForEach-Object { "$($_.DisplayName) — $($_.Language)" }
```

2. Show the list and ask which voice they want (free text — list is dynamic).

3. Use the `AskUserQuestion` tool for speaking rate:

```
question: "באיזה קצב תרצה שהמורה ידבר?"
header: "קצב דיבור"
options:
  - label: "רגיל"
    description: "קצב ברירת מחדל (0)"
  - label: "איטי"
    description: "מומלץ למתחילים (-2)"
  - label: "מהיר"
    description: "למי שרוצה להאיץ (+2)"
```

Map: רגיל → 0, איטי → -2, מהיר → 2.

4. Use the `AskUserQuestion` tool for TTS mode:

```
question: "מתי תרצה שהמורה ידבר?"
header: "מצב קול"
options:
  - label: "אוטומטי"
    description: "מדבר אחרי כל תשובה"
  - label: "לפי דרישה"
    description: "רק כשתבקש"
```

Map: אוטומטי → `"auto"`, לפי דרישה → `"on-demand"`.

5. Test the voice by speaking a greeting in the configured session language.

6. Use the `AskUserQuestion` tool:

```
question: "הקול נשמע טוב?"
header: "בדיקת קול"
options:
  - label: "כן, מעולה"
    description: "שמור את ההגדרות"
  - label: "לא, שנה קול"
    description: "חזור לבחירת קול (שלב 2)"
```

**If no:** set `tts.enabled = false`.

---

## D.5. Learning Style

Use `AskUserQuestion` (two questions, can be shown together):

```
question: "איך תעדיף ללמוד בדרך כלל?"
header: "סגנון למידה"
options:
  - label: "standard — הסבר ואז שאלה (ברירת מחדל)"
    description: "אסביר כל נושא ואז אשאל שאלה לבדיקת הבנה"
  - label: "diagnostic — בחן אותי קודם"
    description: "תבחן אותי על כל השיעור קודם, ותלמד אותי רק את מה שטעיתי"
  - label: "socratic — הדרך אותי בשאלות"
    description: "תשאל שאלות שיובילו אותי לגלות את התשובות בעצמי"
```

```
question: "איזו רמת פירוט מתאימה לך?"
header: "רמת פירוט"
options:
  - label: "detail 1 — קצר מאוד"
    description: "רק הרעיון המרכזי, 1–2 משפטים לשקף"
  - label: "detail 2 — ברירת מחדל"
    description: "מאוזן — הסבר + דוגמה + שאלה"
  - label: "detail 3 — עומק מלא"
    description: "כל הפרטים, תוספות, השוואות"
```

Map to values:
- mode: `"standard"` / `"diagnostic"` / `"socratic"`
- detail_level: `1` / `2` / `3`

---

## E. Save Settings

Save `~/skill-tutor-tutorials/settings.json`:

```json
{
  "session": {
    "language": "he",
    "address": "masculine"
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
  },
  "learning_style": {
    "mode": "standard",
    "detail_level": 2
  }
}
```

---

## F. Global Install (optional)

By default `/learn` works inside this repo — no install needed. Global install is only useful if the learner wants to run `/learn` from *other* projects (a future cross-repo use case).

**Note the trade-off:** a global copy is a second source of truth. If the repo's modules are later edited, the global copy goes stale until re-synced. Most learners should say no.

Use the `AskUserQuestion` tool:

```
question: "להתקין את /learn גם בפרויקטים אחרים? (רוב הלומדים: לא)"
header: "התקנה גלובלית"
options:
  - label: "לא, רק בריפו הזה"
    description: "/learn יעבוד בתוך הריפו. מומלץ — אין עותק כפול שעלול להתיישן."
  - label: "כן, התקן גלובלית"
    description: "אעתיק את המודולים ל-~/.claude/commands כדי שאפשר יהיה להשתמש מכל מקום."
```

**If no:** skip — confirm settings are saved and `/learn` is ready inside this repo.

**If yes:** copy the skill files to the global Claude commands folder, then warn that future repo edits require re-running setup to re-sync.

```powershell
$dest = "$env:USERPROFILE\.claude\commands"
if (!(Test-Path $dest)) { New-Item -ItemType Directory -Force -Path $dest | Out-Null }
Copy-Item -Force "$PWD\.claude\commands\learn.md" "$dest\learn.md"

$moduleDest = "$dest\learn"
if (!(Test-Path $moduleDest)) { New-Item -ItemType Directory -Force -Path $moduleDest | Out-Null }
Copy-Item -Force "$PWD\.claude\commands\learn\*.md" "$moduleDest\"
```

---

## G. Setup Complete — REQUIRED

**You MUST always send this message after completing all steps above, regardless of which options the learner chose.**

Send a summary message in `session.language` that includes:
1. A confirmation that setup is complete and settings are saved.
2. A one-line recap of the chosen settings (language, course, TTS on/off).
3. A prompt asking what they'd like to do next — offer to start the first lesson or jump to a specific one.

Example (English):
```
Setup complete! Here's your configuration:
- Language: English
- Course: AI Dev
- Voice: Off

Ready to start learning. Would you like to begin with Lesson 0.1, or jump somewhere specific?
```

Do not skip this step even if any previous section was skipped or the learner said "no" to optional features.
