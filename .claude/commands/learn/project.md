# Project Module

*Loaded when /learn is called with "project" argument, or when learner picks the final project from resume.*

Respond in `session.language` throughout.

---

## Step 1 — Load Project State

Read `~/skill-tutor-tutorials/project/ai-dev-project.md`.

- **Missing** → go to Project Selection (Step 2)
- **Exists, status = in_progress** → go to Project Dashboard (Step 3)
- **Exists, status = completed** → show completion summary and ask if they want to review or present

---

## Step 2 — Project Selection

Load `courses/ai-dev/lessons/03-final-project/projects.md`.

Present a short summary of each project:

```
🎓 פרויקט גמר — AI Dev

בחרו פרויקט אחד. כל הפרויקטים מחייבים: deploy פעיל, הדגמה חיה בפני הכיתה, ו-commit history אמיתי.

א — מערכת תמיכת לקוחות WhatsApp (14 שעות | בינונית-גבוהה)
WhatsApp webhook + Vertex AI + Supabase + Next.js Dashboard.

ב — Document Intelligence Service (12 שעות | בינונית-גבוהה)
PDF/CSV → Vertex AI Structured Output → Dashboard + REST API.

ג — סוכן Intelligence יומי בTelegram (12 שעות | גבוהה)
Agent Loop מאפס, 5+ Tools, Cloudflare Cron.

ד — מנוע Code Review אוטונומי לGitHub (16 שעות | גבוהה)
3 Specialist Agents במקביל → PR Comment אוטומטי.

איזה פרויקט בוחרים?
```

After learner selects, load the full spec for their chosen project from `projects.md`. Then create `~/skill-tutor-tutorials/project/ai-dev-project.md`:

```markdown
---
project: [א/ב/ג/ד]
project_title: [title]
selected_at: DD-MM-YYYY
status: in_progress
current_phase: 1
total_phases: [N from project spec]
---

## Checklist
[all phase lines from the chosen project's שלבי הפרויקט, formatted as:]
- [ ] שלב 1 — [phase title]
- [ ] שלב 2 — [phase title]
...

## Project Checklist (final)
[all checklist items from the chosen project's Checklist section, all unchecked]

## Help Requests

## Notes
```

Then go to Step 3.

---

## Step 3 — Project Dashboard

Display current state based on the state file:

```
🏗️ פרויקט [letter] — [title]

התקדמות:
✅ שלב 1 — [title] (done)
🔄 שלב 2 — [title] ← עכשיו
☐ שלב 3 — [title]
...

מה רוצים לעשות?
1. עזרה עם שלב [N] (הנוכחי)
2. סמן שלב [N] כ-Done
3. הצג checklist מלא של ה-deliverables
4. הצג מפרט מלא של השלב הנוכחי
```

---

## Step 4 — Handle Commands

**עזרה עם שלב / שאלה ספציפית:**
- Load the relevant phase from `projects.md` for the chosen project
- Answer in the context of that specific phase
- Reference the learner's tech background from `learner_profile.md`
- Append to "Help Requests" section in `ai-dev-project.md`

**סמן שלב כ-Done:**
- Update the checklist in `ai-dev-project.md` — mark `[ ]` → `[x]`
- Advance `current_phase` counter
- Show updated dashboard (Step 3)
- If all phases done → go to Step 5

**checklist / deliverables:**
- Show all final checklist items from `projects.md` with current check/uncheck state

**מפרט / spec:**
- Show the full phase spec for the current phase from `projects.md`

---

## Step 5 — Project Completion

When all phases are marked done, update the state file:
- `status: completed`
- Add `completed_at: DD-MM-YYYY`

Display:

```
🎉 סיימת את פרויקט [letter]!

לפני ההגשה — ודא:
☐ GitHub repo URL עם commit history אמיתי (לא push אחד בסוף)
☐ URL פעיל — פתוח מכל מכשיר, לא localhost
☐ CLAUDE.md מתועד עם Tech Stack ו-Conventions
☐ חישוב עלות מדויק: X ש"ח ל-100 בקשות/יום
☐ מצגת 10 דקות מוכנה + הדגמה חיה שעובדת

בהצלחה בהגשה!
```

Update `~/skill-tutor-tutorials/topics/knowledge_map.md` — add under Mastered Topics:
```
- Final Project [letter] — [title]: deployed [URL], completed [date]
```
