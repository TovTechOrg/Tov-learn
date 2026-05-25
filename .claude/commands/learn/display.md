# Display Module — Visual Language

*Loaded by teaching.md, quiz.md, and progress.md. Defines the formatting standard for all learner-facing output.*

Use these formats consistently. Every interaction type has one format — don't invent variations.

---

## Section Header

Use at the start of every new lesson section:

```markdown
---
### 📚 [current] / [total] — [Section Title]
```

---

## Teaching Block (Journey Format)

```markdown
**The problem:** [one sentence — what breaks without this]

**The insight:** [2–3 sentences in your own words]

**In your project:** [connection to learner's project or real-world example]

---
❓ [One thinking question. Not trivia.]
```

---

## Answer Feedback

**Correct:**
```markdown
✅ [Brief reinforcement — one sentence]

Continue?
```

**Partially correct:**
```markdown
💡 Close. [One hint — don't give the answer]

Want to try again?
```

**Wrong:**
```markdown
↩️ Not quite. [One hint]

Give it another shot?
```

**After second wrong attempt — reveal:**
```markdown
The answer is: [explanation]

Got it? Continue?
```

---

## Quiz Question

```markdown
---
## 🎯 Question [n] / 4

[Question text]
```

---

## Quiz Results

```markdown
---
## 🏆 Score: [X] / 10

| # | Type | | Note |
|---|------|---|------|
| 1 | Factual | ✅ | [note] |
| 2 | Why it matters | ⚠️ | [note] |
| 3 | Scenario | ✅ | [note] |
| 4 | Weak point | ❌ | [note] |

**Next review:** in [N] days · [date]
```

---

## Session Summary (on "stop")

```markdown
---
## 📋 Session Summary — Lesson [X.X]

✅ **Covered:** [list of sections]
⏭ **Remaining:** [list of sections not covered, or "none"]
🔁 **Recommended next:** [lesson number + title]
```

---

## Commands Reminder

Show this once at session start, after the greeting:

```markdown
> **Available:** continue · quiz me · explain again · summary · exercises · stop · read aloud · settings
```
