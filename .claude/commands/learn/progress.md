# Progress Module

*Loaded after covering at least one section, and on the "stop" command.*

Respond in `session.language` throughout.

---

## Save Tutorial File

Create or update `~/skill-tutor-tutorials/tutorials/lesson-{lesson_number}.md`.

**If the file does not exist — create:**

```markdown
---
topic: [lesson title]
lesson: {lesson_number}
source_project: [learner's project from profile]
understanding_score: null
last_quizzed: null
created: DD-MM-YYYY
last_updated: DD-MM-YYYY
---

# [Lesson Title]

## Why This Matters
[Connection to learner's goals — what they can do after this lesson]

## Topics Covered
[Bullet list of each section covered, in the learner's words — not copied from the script]

## Key Insights
[2–3 mental models the learner gained]

## In Your Project
[How the topics connect to the learner's specific project]

## Common Mistakes to Watch For
[What the learner got wrong or hesitated on]

## Practice
[Specific practice suggestion in the context of their project]

## Q&A
[Every question the learner asked + the short answer]

## Quiz History
[Updated by quiz module]
```

**If the file exists — update only:**
- Append to Topics Covered
- Append to Key Insights
- Append to Q&A
- Refresh `last_updated`
- **Do not replace** existing content

---

## Update Knowledge Map

Update `~/skill-tutor-tutorials/topics/knowledge_map.md`:

```markdown
# Knowledge Map

## Mastered Topics (score 8+)
- [Lesson X.X — Title]: [one sentence — what the learner can now do]

## Topics In Progress (score 4–7)
- [Lesson X.X — Title]: [what needs reinforcement]

## Topics to Explore
- [Lesson X.X]: [why relevant to learner's goals]

## Connections Between Topics
- [Lesson A] → [Lesson B]: [how they connect]
```

If the file exists — update only; do not delete previous entries.

---

## Update Learner Profile

Update `~/skill-tutor-tutorials/learner_profile.md` — add/update `## Lessons Studied`:

```markdown
## Lessons Studied
| Lesson | Title | Score | Last Date |
|--------|-------|-------|-----------|
| X.X | [title] | X/10 | DD-MM-YYYY |
```

---

## Session End (on "stop" command)

After saving all files, display a session summary:
- What was covered
- What remains
- Recommended next step based on knowledge map
