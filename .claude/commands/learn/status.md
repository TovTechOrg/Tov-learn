# Status Module

*Loaded when $ARGUMENTS = "status". Generates an HTML progress dashboard.*

Respond in `session.language` throughout. Address the learner using `session.address`.

---

## Step 1 — Collect Data

Read these files silently:
- `~/skill-tutor-tutorials/topics/knowledge_map.md`
- All files matching `~/skill-tutor-tutorials/progress/lesson-*.md`
- All files matching `~/skill-tutor-tutorials/tutorials/lesson-*.md` (for frontmatter: topic, understanding_score, last_quizzed)
- All files matching `~/skill-tutor-tutorials/progress/exercises-lesson-*.md` (their **נדרשים** count and `## תרגיל` entries — see Exercises below)

Also read every `~/skill-tutor-tutorials/progress/module-*.md` (a module skip quiz pass marks all its lessons complete).

From each progress file extract:
- Lesson number
- Quiz scores and dates — and for each, whether it was a **skip quiz** (marked `מבחן דילוג` / skip quiz in the Sessions row or the Quiz History row, or the lesson's `**Skip quiz passed:**` line). A skip quiz is taken before learning, so it never counts as the lesson's score below.
- Next recommended review date — only one set by a quiz taken after learning

**Lesson status — by completion, not by score** (quizzes are optional, so a lesson is never "in progress" just because it has no quiz). Use the definitions in `order.md`:
- **Complete** — finished (all slides covered and the required exercises done), passed by a lesson skip quiz, or passed by a module skip quiz
- **In progress** — learning started but not complete (e.g. slides not finished, or required exercises missing)
- **Not started** — no progress file exists and its module wasn't passed (cross-reference with COURSE.md lesson list)

**Score — extra information only.** Show the latest quiz score taken after learning, if any. If a lesson only has a skip-quiz score, show it with the label "(מבחן דילוג)". Scores never change the lesson status.

Compute:
- **Overdue** — next review date is before today
- **Due today** — next review date is today
- **Upcoming** — next review date is within 7 days
- **Average score** — only quizzes taken after learning (no skip quizzes). If there are none, show "—".
- **Exercises** per lesson, from `exercises-lesson-X.Y.md` (format in `exercises.md`: a `**נדרשים:** N` header, then one `## תרגיל` entry per completed or paid-skipped exercise):
  - **done** — the number of `## תרגיל` entries equals **נדרשים**; mention how many were skipped as paid-only (`(דולג — דורש תשלום)`), if any
  - **incomplete** — the lesson's progress file says `Slides covered: all` and `**Exercises required:** yes`, but the exercises file is missing or has fewer entries than **נדרשים** (show "[recorded] of [N]")
  - **passed by skip quiz** — the lesson's progress file, or `progress/module-X.md` for its module, has `**Skip quiz passed:**` (exercises not required)
  - **not tracked** — the lesson was learned before the exercises rule (no `**Exercises required:**` line; `order.md` explains how such lessons count as finished)
  - **not yet** — otherwise
- **Exercises incomplete** — count of lessons with exercises = incomplete
- **Optional** — COURSE.md type `רשות` and not started. Show these greyed out with a "רשות" tag; do not count them in totals or as missing

---

## Step 2 — Generate HTML Dashboard

Save to `~/skill-tutor-tutorials/dashboard.html`:

```html
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <title>Learning Dashboard</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', sans-serif; background: #F9FAFB; padding: 40px; color: #111827; }

    .header { margin-bottom: 32px; }
    .header h1 { font-size: 1.6rem; font-weight: 700; }
    .header p { color: #6B7280; font-size: 0.9rem; margin-top: 4px; }

    .stats { display: flex; gap: 16px; margin-bottom: 32px; flex-wrap: wrap; }
    .stat { background: white; border-radius: 10px; padding: 16px 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); min-width: 120px; }
    .stat-value { font-size: 1.8rem; font-weight: 700; }
    .stat-label { font-size: 0.75rem; color: #6B7280; margin-top: 2px; }
    .stat.alert .stat-value { color: #EF4444; }
    .stat.good .stat-value { color: #10B981; }

    .section-title { font-size: 0.75rem; font-weight: 700; text-transform: uppercase;
                     letter-spacing: 1px; color: #6B7280; margin-bottom: 12px; }

    .due-list { margin-bottom: 32px; }
    .due-item { background: white; border-radius: 8px; padding: 14px 18px;
                margin-bottom: 8px; display: flex; justify-content: space-between;
                align-items: center; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
    .due-item .lesson-id { font-weight: 600; font-size: 0.9rem; }
    .due-item .lesson-topic { color: #6B7280; font-size: 0.85rem; }
    .due-item .badge { font-size: 0.75rem; padding: 3px 10px; border-radius: 999px; font-weight: 600; }
    .badge.overdue { background: #FEE2E2; color: #DC2626; }
    .badge.today { background: #FEF3C7; color: #D97706; }
    .badge.upcoming { background: #DBEAFE; color: #2563EB; }

    .lessons-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                    gap: 12px; margin-bottom: 40px; }
    .lesson-card { background: white; border-radius: 10px; padding: 16px;
                   box-shadow: 0 1px 3px rgba(0,0,0,0.07); border-top: 3px solid #E5E7EB; }
    .lesson-card.complete { border-top-color: #10B981; }
    .lesson-card.in-progress { border-top-color: #F59E0B; }
    .lesson-card.not-started { border-top-color: #E5E7EB; opacity: 0.7; }
    .lesson-card .lesson-num { font-size: 0.75rem; color: #6B7280; }
    .lesson-card .lesson-name { font-size: 0.9rem; font-weight: 600; margin: 4px 0; }
    .lesson-card .score { font-size: 0.8rem; color: #6B7280; }
    .score-bar { height: 4px; background: #E5E7EB; border-radius: 2px; margin-top: 8px; }
    .score-fill { height: 4px; border-radius: 2px; background: #10B981; }
    .score-fill.mid { background: #F59E0B; }
    .score-fill.low { background: #EF4444; }
    .exercises { font-size: 0.75rem; margin-top: 8px; }
    .exercises.done { color: #10B981; }
    .exercises.incomplete { color: #DC2626; font-weight: 600; }
    .exercises.not-yet { color: #9CA3AF; }
  </style>
</head>
<body>
  <div class="header">
    <h1>Learning Dashboard</h1>
    <p>Updated [DD-MM-YYYY]</p>
  </div>

  <div class="stats">
    <div class="stat good">
      <div class="stat-value">[N]</div>
      <div class="stat-label">Complete</div>
    </div>
    <div class="stat">
      <div class="stat-value">[N]</div>
      <div class="stat-label">In Progress</div>
    </div>
    <div class="stat alert">
      <div class="stat-value">[N]</div>
      <div class="stat-label">Due for Review</div>
    </div>
    <div class="stat">
      <div class="stat-value">[avg]/10</div>
      <div class="stat-label">Avg Score (after learning)</div>
    </div>
    <!-- Only show this stat if at least one lesson's exercises are incomplete -->
    <div class="stat alert">
      <div class="stat-value">[N]</div>
      <div class="stat-label">Exercises Incomplete</div>
    </div>
  </div>

  <!-- Only show this section if there are due/overdue lessons -->
  <div class="due-list">
    <div class="section-title">Due for Review</div>
    <div class="due-item">
      <div>
        <div class="lesson-id">Lesson [X.X]</div>
        <div class="lesson-topic">[topic title]</div>
      </div>
      <span class="badge overdue">Overdue</span>
    </div>
    <div class="due-item">
      <div>
        <div class="lesson-id">Lesson [X.X]</div>
        <div class="lesson-topic">[topic title]</div>
      </div>
      <span class="badge today">Today</span>
    </div>
  </div>

  <div class="section-title">All Lessons</div>
  <div class="lessons-grid">
    <!-- Repeat for each lesson -->
    <div class="lesson-card complete">
      <div class="lesson-num">0.1</div>
      <div class="lesson-name">[Lesson Title]</div>
      <div class="score">Complete · Score: 9/10</div>
      <div class="score-bar"><div class="score-fill" style="width: 90%"></div></div>
      <div class="exercises done">✓ Exercises done</div>
    </div>
    <div class="lesson-card complete">
      <div class="lesson-num">0.2</div>
      <div class="lesson-name">[Lesson Title]</div>
      <div class="score">Complete · No quiz after learning (optional)</div>
      <div class="score-bar"></div>
      <div class="exercises done">✓ Exercises done</div>
    </div>
    <div class="lesson-card complete">
      <div class="lesson-num">0.3</div>
      <div class="lesson-name">[Lesson Title]</div>
      <div class="score">Complete · 8/10 (מבחן דילוג)</div>
      <div class="score-bar"></div>
      <div class="exercises done">✓ Passed by skip quiz — exercises not required</div>
    </div>
    <div class="lesson-card in-progress">
      <div class="lesson-num">0.4</div>
      <div class="lesson-name">[Lesson Title]</div>
      <div class="score">In progress · 6/10 (מבחן דילוג)</div>
      <div class="score-bar"></div>
      <div class="exercises incomplete">✗ Exercises: 1 of 3 — finish them before the next lesson</div>
    </div>
    <div class="lesson-card not-started">
      <div class="lesson-num">1.1</div>
      <div class="lesson-name">[Lesson Title]</div>
      <div class="score">Not started</div>
      <div class="score-bar"></div>
      <div class="exercises not-yet">Exercises not yet</div>
    </div>
  </div>
</body>
</html>
```

Fill in all data from the files collected in Step 1. Build one card per lesson from COURSE.md. The card's class and first word come from the lesson status (complete / in-progress / not-started); the score bar is filled only for a score from a quiz taken after learning.

---

## Step 3 — Report to Learner

After saving the file:

```
Dashboard saved: ~/skill-tutor-tutorials/dashboard.html
Open it in a browser to view your progress.

[N] lessons complete · [N] in progress · [N] not started · [N] due for review
```

Say how lessons became complete when it helps (e.g. "0.3 passed by skip quiz", "module 1 passed by its module quiz"), and never call a complete lesson "in progress" because it has no quiz — the quiz is optional. If you mention an average score, say it covers only quizzes taken after learning. For a skip quiz below 8, say "לא עברת את מבחן הדילוג" (didn't pass), never "נכשלת" (failed) — it's an optional shortcut, not a failure.

If there are overdue lessons, add:
```
⚠️ [N] lessons are overdue for review: [lesson numbers]
Type `/learn` to see what to do next.
```

If any lesson's exercises are incomplete, add:
```
📝 Exercises incomplete in [N] lessons: [lesson numbers]
Exercises are part of every lesson — they'll be completed before you start the next lesson.
```
