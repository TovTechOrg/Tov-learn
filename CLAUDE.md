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
| Status | `.claude/commands/learn/status.md` | HTML dashboard — all lessons by completion (complete / in progress / not started), scores as extra info, due reviews |
| Project Analysis | `.claude/commands/learn/project-analysis.md` | סריקת קוד, ראיון ארכיטקט, מפת HTML |
| Slides | `.claude/commands/learn/slides.md` | קריאה מילה במילה מסקריפטים, viewer אינטראקטיבי, TTS אוטומטי |
| Export | `.claude/commands/learn/export.md` | ייצוא כל נתוני התלמיד ל-ZIP — גיבוי/מעבר למכשיר אחר |
| Import | `.claude/commands/learn/import.md` | ייבוא נתוני תלמיד מ-ZIP — החלפה מלאה או הוספה בלבד |
| Deploy | `.claude/commands/learn/deploy.md` | בחירת כלי פריסה (GitHub Pages / Cloudflare / Render / Vercel), CLI-first, תרומה ל-FAQ |
| Project | `.claude/commands/learn/project.md` | פרויקט גמר: בחירה, repo ו-deploy URL מההתחלה, שלבים, checklist |
| Security | `.claude/commands/learn/security.md` | סריקת אבטחה על הפרויקט החי אחרי deploy |
| Display (ref) | `.claude/commands/learn/display.md` | שפה ויזואלית אחידה לפלט ללומד; נטען ע"י teaching, quiz, progress |
| CLI-First (ref) | `.claude/commands/learn/cli-first.md` | עקרון משותף — העדפת CLI על דאשבורד; מודולים אחרים מפנים אליו |
| Stuck | `.claude/commands/learn/stuck.md` | עזרה כשהלומד תקוע — לא הבין חומר / משהו לא עובד; מלמד איך לבקש עזרה טוב |
| Lesson order (ref) | `.claude/commands/learn/order.md` | שיעורים לפי סדר הקורס: שיעור מתחיל רק כשכל השיעורים הקודמים הושלמו (שקפים + תרגילים נדרשים) או עברו מבחן דילוג (שיעור / מודול) |
| Exercises (ref) | `.claude/commands/learn/exercises.md` | כללי תרגילים משותפים ל-teaching ו-slides: כל התרגילים לפני השיעור הבא, קובץ מעקב, תרגילים בתשלום (דרך חינמית ← גרסה מותאמת לכלים חינמיים ← רק אז דילוג ודגל למנחים; בלי לחכות למנחה, ניסיון חינם לא נחשב חינמי) |

**Hooks** (`.claude/settings.json`, סקריפטים ב-`.claude/scripts/`):

| Hook | סקריפט | תפקיד |
|------|--------|-------|
| Stop | `auto-save-progress.ps1` | שמירת שיעור/שקף נוכחי (מצב שקפים) |
| UserPromptSubmit | `detect-stuck.ps1` | הודעה כמו "לא הבנתי" / "לא עובד" ← הערה ל-Claude על `stuck.md` |
| PostToolUse (Read) | `check-lesson-order.ps1` | כש-Claude קורא סקריפט של שיעור (תחילת שיעור) ושיעור קודם כלשהו לפי סדר הקורס לא הושלם ← הערה ל-Claude לפי `order.md` (בכל פעם שמתחילים את השיעור, בכל סשן, עד שהשיעורים הקודמים הושלמו) |

Hooks רצים ב-exec form לפי התיעוד (`"command": "powershell.exe"`, `"args": [..., "-File", "${CLAUDE_PROJECT_DIR}/..."]`). סקריפט עם טקסט בעברית נשמר ב-UTF-8 **עם BOM** (Windows PowerShell 5.1). הערות של hooks ל-Claude מנוסחות כעובדות, לא כפקודות (התיעוד מזהיר שניסוח פקודה עלול להפעיל הגנות prompt-injection).

סקריפטים תומכים נמצאים ב-`.claude/scripts/` (PowerShell — slide server, HTML generator, auto-save).

**פלטפורמה:** TTS, viewer השקפים וה-Stop hook דורשים Windows (PowerShell). ב-Mac/Linux הלמידה עובדת, ה-hook מדלג בשקט, והשקפים מוקראים בצ'אט.

**בדיקה:** `python tests/validate_structure.py` רץ ב-CI. הוא בודק שכל מודול בטבלת ה-routing וב-CLAUDE.md קיים, ש-COURSE.md תואם לתיקיות השיעורים, ושלכל שיעור יש script ו-exercises. מוסיפים מודול או שיעור ← מעדכנים את הטבלאות, אחרת ה-CI נכשל.

**בדיקת ה-hooks:** `python tests/test_hooks.py` מריץ כל hook כמו ש-Claude Code מריץ אותו, עם קורס ותיקיית לומד מזויפים (לא נוגע בנתונים אמיתיים). רץ ב-CI על Windows. משנים hook ← מוסיפים לו מקרה בדיקה.

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

הקורס הפעיל היחיד הוא **AI Dev** — ברירת המחדל בכל מקום (setup, template, docs).

| קורס | תיקייה | course.path | סטטוס |
|------|--------|-------------|-------|
| AI Dev | `courses/ai-dev/` | `courses/ai-dev/lessons` | פעיל (ברירת מחדל) |
| AI Engineer | `courses/_archive/ai-engineer/` | `courses/_archive/ai-engineer/lessons` | בארכיון — לא מוצע ב-setup; נגיש רק דרך נתיב מותאם אישית |

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
4. (אופציונלי) אם ההתקנה הגלובלית מופעלת — עדכן את רשימת הקבצים שמועתקים ב-`setup.md` סעיף F. ברירת מחדל: `/learn` רץ מתוך הריפו בלבד, ללא התקנה גלובלית.
