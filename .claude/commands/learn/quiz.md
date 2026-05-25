# Quiz Module

*Loaded when the "quiz me" trigger is used. TTS helper is defined in learn.md.*

Respond in `session.language` throughout.

---

## Quiz Format

Ask 4 questions — **one at a time**, wait for each answer:

1. **Factual** — what / how
2. **Why it matters** — consequences and motivation
3. **Scenario** — "If X happened, what would you do?"
4. **Weak point** — on a section the learner hesitated on earlier in the session

After all 4 answers: give an overall score (1–10) with specific feedback per question.

*(Speak score summary if TTS enabled)*

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
