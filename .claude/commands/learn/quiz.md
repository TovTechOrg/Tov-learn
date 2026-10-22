# Quiz Module

*Loaded when the "quiz me" trigger is used. TTS helper is defined in learn.md.*

Respond in `session.language` throughout. Address the learner using `session.address`.

---

## Quiz Modes

| Trigger | Scope | Questions |
|---------|-------|-----------|
| `quiz me` | only the sections covered in this session | 4 multiple-choice + 1 free-text |
| `quiz module X` (module skip quiz) | every lesson of module X — see **Module Skip Quiz** below | at least 1 multiple-choice per lesson (more for lessons with many important subjects; 8+ in total) + 1 free-text |
| `quiz me full` / `quiz full` | the **entire** lesson script (load `{lesson_number}_script.txt`, split by `[מעבר שקף]`, use all sections — do not assume a fixed count) | 8 multiple-choice + 1 free-text |

Before building questions, read the **Quiz History** in `~/skill-tutor-tutorials/tutorials/lesson-{lesson_number}.md`. If the learner has quizzed this lesson before, **vary the questions** — different angles, different distractors, and bias toward previously-recorded weak points. Keep all questions factually correct and on the lesson's material.

---

## Quiz Format

**Step 1 — Multiple-choice (batched in one `AskUserQuestion` call).**

Build the multiple-choice questions (4 for normal, 8 for full → two `AskUserQuestion` calls of 4) covering these types:

1. **Factual** — what / how
2. **Why it matters** — consequences and motivation
3. **Scenario** — "If X happened, what would you do?"
4. **Weak point** *(normal mode)* — a section the learner hesitated on this session. *In full mode there's no session history → replace with a **synthesis** question connecting two sections.*

Each question: **1 correct option + 2–3 plausible distractors**, all in `session.language`. `AskUserQuestion` auto-adds an **"Other"** option — if the learner picks it and free-texts, judge that answer qualitatively. Set `multiSelect: false`.

**IMPORTANT — never use the `description` field on quiz options.** Descriptions are visible to the learner before they answer and will reveal or hint at the correct answer. Leave `description` empty or omit it entirely on every option.

**IMPORTANT — vary correct answer position:** The correct option must appear in a different position for each question. Never place the correct answer in the same slot across all questions (e.g. always first). Distribute across positions — for example: Q1→3rd, Q2→1st, Q3→2nd, Q4→3rd. This prevents pattern-guessing.

**Step 2 — One free-text recall question at the end.**

After the multiple-choice box(es), ask **one** open-ended question (synthesis or "explain in your own words"). This is the recall test — wait for the learner to type their answer.

---

## Scoring

Give an overall score **1–10**, then immediately show a **full review table** — one row per question:

| # | השאלה | תשובתך | תשובה נכונה | הסבר קצר |
|---|-------|--------|------------|----------|
| 1 | ... | ✅ / ❌ [מה ענית] | [התשובה הנכונה] | [משפט-שניים מדוע] |

Rules for the table:
- Show **every** question — multiple-choice and free-text.
- For correct answers: mark ✅, still show the correct answer and a one-sentence "why this is right."
- For wrong or partial answers: mark ❌, show what the learner answered, the correct answer, and 1–2 sentences explaining the concept.
- For free-text: quote the key idea from the learner's answer vs. the expected key idea.
- Keep explanations in `session.language`, max 2 sentences each.

Scoring formula (unchanged):
- **Normal:** each correct multiple-choice = 1.5 pts (6 total) + free-text up to 4 pts → /10.
- **Full:** each correct multiple-choice = 1 pt (8 total) + free-text up to 2 pts → /10.
- **Module:** see **Module Skip Quiz** below.

*(Speak score summary if TTS enabled — skip the table)*

---

## Module Skip Quiz (`quiz module X`)

For a learner who already knows a whole module and wants to skip it: one quiz for the module instead of a skip quiz per lesson.

**Lessons covered:** every lesson in the course's `COURSE.md` lesson list (`## רשימת שיעורים`) whose number starts with `X.` — e.g. module 1 → 1.1, 1.2, … Load each lesson's `{lesson_number}_script.txt` and split it by `[מעבר שקף]`.

**Questions:**
- At least **one multiple-choice question per lesson**. Lessons with many important subjects get more questions, so each lesson is tested roughly in proportion to its key content. At least 8 multiple-choice questions in total.
- Keep track of which lesson each question tests.
- Same format rules as above: batches of 4 in `AskUserQuestion`, no `description`, varied correct-answer positions, mixed question types.
- Then one free-text question connecting ideas from at least two of the module's lessons.
- If `~/skill-tutor-tutorials/progress/module-X.md` shows earlier attempts, vary the questions.

**Scoring:** multiple-choice = 8 × (correct ÷ total), rounded to one decimal, + free-text up to 2 pts → /10. In the review table, show each question's lesson in the `#` column (e.g. `3 (1.4)`).

**Pass:** score ≥ 8 **and** at least one correct multiple-choice answer for every lesson in the module. Tell the learner the result and, if they didn't pass, why (the score, or which lessons had no correct answer).

**Save** to `~/skill-tutor-tutorials/progress/module-X.md` — create it if missing, keep earlier content, and don't use the two lesson locations below:
```markdown
# Module X — skip quiz

| Date | Score | Lessons with no correct answer | Result |
|------|-------|-------------------------------|--------|
| DD-MM-YYYY | X/10 | [lesson numbers, or —] | passed / not passed |
```
On a pass, also add the line `**Skip quiz passed:** X/10 (DD-MM-YYYY)` under the title. It marks every lesson of the module as done, so their slides and exercises aren't required.

**Not passed:** the module isn't skipped. The learner goes through its lessons in order; each lesson can still be skipped by its own skip quiz (`teaching.md`, Step 3).

---

## Save Results — Two Locations

**A. Update** `~/skill-tutor-tutorials/tutorials/lesson-{lesson_number}.md`:

Append to the end:
```markdown
## Quiz History

| Date | Score | Weak Points |
|------|-------|-------------|
| DD-MM-YYYY | X/10 | [topics to revisit] |
```

Update frontmatter: `understanding_score: X` and `last_quizzed: DD-MM-YYYY`.

**B. Save / update** `~/skill-tutor-tutorials/progress/lesson-{lesson_number}.md` (keep any content already in it, including the `**Slides covered:**`, `**Exercises required:**` and `**Skip quiz passed:**` lines — the lesson-order check relies on them, see `order.md`):

```markdown
# Progress: Lesson {lesson_number}

## Sessions
| Date | Sections Covered | Quiz Score | Notes |
|------|-----------------|-----------|-------|
| DD-MM-YYYY | [list] | X/10 | [weak points] |

## Spaced Repetition
- Score 1–3: review within 2 days
- Score 4–6: review within 13 days
- Score 7–8: review within 34 days
- Score 9–10: review within 89 days

Next recommended review: [date based on score]
```

---

## Next Lesson Recommendation

After saving the score, suggest the next lesson: always the first lesson in the course order that isn't complete (`order.md`). You may also load `~/skill-tutor-tutorials/topics/knowledge_map.md` and suggest a related earlier lesson for review.
