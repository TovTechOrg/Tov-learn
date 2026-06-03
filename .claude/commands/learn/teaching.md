# Teaching Module

*Loaded by learn.md when the learner selects a lesson. TTS helper is defined in learn.md and available in this session.*

Respond in `session.language` throughout.

---

## Step 2A — Load Lesson Content

**Resolve path (priority order):**
1. Check if `./lessons/` exists at the project root (Glob `lessons/**`). If yes — use it.
2. Otherwise use `course.path` from settings.

**Find files:**
- Glob the resolved path for the folder matching the lesson number in $ARGUMENTS.
- Script file — try in order:
  1. `{lesson_number}_script.txt` (e.g. `0.3_script.txt`)
  2. Fallback: `digital-course-script.txt`
- Exercises file — try in order:
  1. `{lesson_number}_exercises.md`
  2. Fallback: `exercises.md`
- Progress file: `~/skill-tutor-tutorials/progress/lesson-{lesson_number}.md`

Split the script into sections by `[מעבר שקף]`.

---

## Step 3 — Open the Session

Greet the learner. State the lesson topic and number of sections.

**If a progress file exists for this lesson:**
Tell the learner their previous score and ask if they want to restart or jump to a quiz on what was already covered.

**Otherwise:** Ask what they already know about the topic, if anything. Also ask which detail level they prefer:
- **detail 1** — very brief, one or two sentences per slide
- **detail 2** — slightly compressed (default)
- **detail 3** — full depth, may add extra bullet points

Store the chosen level as `session.detail_level` (default: 2).

Use their answers plus `learner_profile.md` to calibrate depth. Offer to skip sections they clearly already know.

*(Speak greeting if TTS enabled)*

---

## Step 4 — Cover Every Slide

**IMPORTANT: Every slide (section split by `[מעבר שקף]`) MUST be represented in the lesson output.** Never silently skip a slide. At minimum, include one sentence summarizing it.

For every slide, apply the **Journey Format** scaled by `session.detail_level`:

### Detail Level 1 — Very Brief
- 1–2 sentences max per slide
- State the core idea only
- No question, no context example
- Good for fast review passes

### Detail Level 2 — Standard (default)
Use the full Journey Format:
1. **The problem** — one sentence
2. **The insight** — 2–3 sentences in your own words, not copied from the script
3. **In your context** — one concrete connection to the learner's project or a real example
4. **Question** — one thinking question; wait for an answer before continuing

Each block: max 5 sentences total.

### Detail Level 3 — Full Depth
Use the full Journey Format plus:
- Expand the insight to 4–5 sentences
- Add bullet points for key facts, numbers, or comparisons from the slide
- May include one extra "did you know" point not in the script if genuinely relevant
- Still ask a question and wait for an answer

**The learner can switch levels at any time** by saying "detail 1", "detail 2", or "detail 3".

**Responding to answers:**
- Correct → brief acknowledgment + continue
- Partial/wrong → one hint → let them try again → then explain

*(Speak each teaching block if TTS enabled — strip markdown before speaking)*

---

## Living Q&A

For every question the learner asks during teaching (not a quiz), answer conversationally then **silently** append to `~/skill-tutor-tutorials/tutorials/lesson-{lesson_number}.md` under `## Q&A`:

```
**Q:** [the question]
**A:** [the short answer]
```

Do not tell the learner you are saving — just do it.

---

## Step 5 — End of Lesson

After completing the **last section**, do the following in order:

1. **Quick recap** — 2–3 bullet points summarizing the key takeaways from the entire lesson. Keep it sharp.

2. **Offer exercises** — Tell the learner that exercises are available for this lesson and ask:
   > "רוצה לעשות את התרגילים של השיעור הזה?"  (adapt to `session.language`)
   
   - If **yes** → display the full content of the exercises file that was loaded in Step 2A. Walk through each exercise one at a time: present it, wait for the learner's response, give brief feedback, then move to the next.
   - If **no** → acknowledge and move to step 3.

3. **Offer quiz** — After exercises (or if skipped), ask:
   > "רוצה לעשות חידון קצר על מה שלמדת?"  (adapt to `session.language`)
   
   - If **yes** → Read `.claude/commands/learn/quiz.md`
   - If **no** → Read `.claude/commands/learn/progress.md` and save session summary

*(Speak the recap and offer if TTS enabled)*

---

## Teaching Principles

- Use `session.language` for all output
- Max 5 sentences per teaching block — then the learner speaks
- Always emphasize **why** before **how**
- Use the learner's project from their profile as the primary example
- If the learner already knows a section — offer to skip it
- Be direct: if an answer is wrong, say so — then help them reach the right one
