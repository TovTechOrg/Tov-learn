# Tov-learn — מערכת הלמידה האינטלגנטית

מערכת טיוטור אינטלגנטית המבוססת על Claude Code skills.

---

## Skill Modules

הסקיל `/learn` בנוי ממודולים נפרדים. כל מודול אחראי על תחום אחד ועצמאי לחלוטין.

| מודול | קובץ | תוכן |
|-------|------|------|
| Entry point + routing | `.claude/commands/learn.md` | Routing + TTS helper + Step 0-2 |
| Setup | `.claude/commands/learn/setup.md` | הגדרות ראשוניות, קול, global install |
| Resume | `.claude/commands/learn/resume.md` | Smart entry — suggests next action based on progress |
| Teaching | `.claude/commands/learn/teaching.md` | טעינת שיעור, Journey format, לולאת הוראה |
| Quiz | `.claude/commands/learn/quiz.md` | בחינה, ציונים, spaced repetition |
| Progress | `.claude/commands/learn/progress.md` | שמירת tutorials, knowledge map |
| Status | `.claude/commands/learn/status.md` | HTML dashboard — all lessons, scores, due reviews |
| Project Analysis | `.claude/commands/learn/project-analysis.md` | סריקת קוד, ראיון ארכיטקט, מפת HTML |

**כלל פיתוח:** כל מודול עצמאי — לא מניחים שמודול אחר כבר נטען. מידע שמודול צריך — הוא קורא בעצמו. TTS helper מוגדר ב-`learn.md` ונטען לפני כל מודול.

---

## מבנה קורסים

```
courses/
  [course-name]/
    COURSE.md                          ← שם, תיאור, רשימת מודולים, course.path ברירת מחדל
    lessons/
      [XX-module-name]/
        [X.Y]-[lesson-name]/
          [X.Y]_script.txt             ← סקריפט (split by [מעבר שקף])
          [X.Y]_exercises.md           ← תרגילים
```

קורסים זמינים:

| קורס | תיקייה | course.path ברירת מחדל |
|------|--------|----------------------|
| AI Dev | `courses/ai-dev/` | `courses/ai-dev/lessons` |
| AI Engineer | `courses/ai-engineer/` | `courses/ai-engineer/lessons` |

---

## Data — per-learner (מחוץ ל-repo)

נשמר ב-`~/skill-tutor-tutorials/`:

```
settings.json                          ← שפה, TTS, course.name, course.path
learner_profile.md                     ← פרופיל אישי + לומד נוכחי
tutorials/lesson-X.Y.md               ← סיכומי שיעורים + Q&A
progress/lesson-X.Y.md                ← ציונים + תאריך חזרה מומלץ
topics/knowledge_map.md               ← מפת ידע מלאה
architectures/[project-name].html     ← מפות ארכיטקטורה
```

---

## הוספת מודול חדש

1. צור קובץ ב-`.claude/commands/learn/[module-name].md`
2. הוסף שורה לטבלת ה-Modules למעלה
3. הוסף routing ב-`learn.md` (Step 2 — Route table)
4. עדכן את הפקודה לגלובל אינסטול ב-`setup.md`
