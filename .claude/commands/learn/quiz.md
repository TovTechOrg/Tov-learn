# Quiz Module

*Loaded when the "quiz me" trigger is used. TTS helper is defined in learn.md.*

Respond in `session.language` throughout. Address the learner using `session.address`.

---

## Quiz Modes

| Trigger | Scope | Questions |
|---------|-------|-----------|
| `quiz me` | only the sections covered in this session | 4 multiple-choice + 1 free-text |
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

*(Speak score summary if TTS enabled — skip the table)*

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

**B. Save / update** `~/skill-tutor-tutorials/progress/lesson-{lesson_number}.md`:

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

After saving the score, load `~/skill-tutor-tutorials/topics/knowledge_map.md` and suggest a related lesson based on what was covered.
