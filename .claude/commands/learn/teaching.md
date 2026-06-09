# Teaching Module

*Loaded by learn.md when the learner selects a lesson. TTS helper is defined in learn.md and available in this session.*

Respond in `session.language` throughout. Address the learner using `session.address`.

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

**Load saved learning style from `~/skill-tutor-tutorials/settings.json`:**

- `session.mode` ← `learning_style.mode` (default: `"standard"`)
- `session.detail_level` ← `learning_style.detail_level` (default: `2`)

**If a saved style exists:** apply it silently — no question needed. Mention it once in the greeting so the learner knows (e.g. "נלמד במצב diagnostic, רמת פירוט 2 — כפי שהגדרת. אפשר לשנות בכל שלב.").

**If no `learning_style` in settings (first-time or missing):** ask the learner explicitly:

> **איך תרצה ללמוד?**
> - **standard** — אסביר כל שקף ואשאל שאלה בסוף (ברירת מחדל)
> - **diagnostic** — תבחן אותי קודם, למד אותי רק על מה שטעיתי, ואז נמשיך
> - **socratic** — הדרך אותי דרך שאלות; אני אגלה את הרעיונות בעצמי

And ask for detail level (1 / 2 / 3).

After the session, if the learner changed mode or detail level mid-lesson, ask:
> "רוצה לשמור את ההעדפה הזו לשיעורים הבאים?"
If yes — update `learning_style` in `settings.json`.

**Reminder — always valid:** "ניתן לעבור בין המצבים בכל שלב — פשוט אמור 'standard', 'diagnostic', 'socratic' או 'הסבר לי' / 'בחן אותי' / 'הדרך אותי'."

---

**If `session.mode == "diagnostic"`:** Skip all further questions in Step 3 — no prior-knowledge question, no skip-quiz offer — and go directly to **Step 3B**.

**Otherwise (standard / socratic):**

Ask what they already know about the topic, if anything.

- If the learner says they already know it well (e.g. "I know this", "familiar with this", "studied it before") — offer a skip quiz: "Want to prove it with a quick quiz? Pass and we'll mark this lesson done and move on." If they agree, read `quiz.md` in `quiz me full` mode. If they score ≥ 7, save progress and recommend the next lesson instead of teaching this one. If they score < 7, proceed with teaching from the beginning.

Use `learner_profile.md` to calibrate depth. Offer to skip sections they clearly already know.

*(Speak greeting if TTS enabled)*

---

## Step 3B — Diagnostic Mode Entry

*Only if `session.mode == "diagnostic"`*

Before teaching anything:

1. Read `quiz.md` in **`quiz me full`** mode — quiz on the entire lesson.
2. After scoring, collect the list of **weak sections** (questions answered incorrectly or partially).
3. Tell the learner:
   > "קיבלת X/10. עכשיו נעבור רק על הנושאים שהיו פחות ברורים."
   (adapt to `session.language`)
4. Set `session.weak_sections` = list of slide indices or topics that map to wrong answers.
5. Switch to Step 4 but **cover only weak sections** using the standard Journey Format (scaled by `session.detail_level`). Skip sections the learner answered correctly — at most, give them a one-sentence "you already know this" acknowledgment.
6. After covering weak sections, offer a short follow-up quiz on those topics only (`quiz me` mode, scoped to weak sections).
7. Then proceed to Step 5 (End of Lesson).

---

## Step 4 — Cover Every Slide

**IMPORTANT: Every slide (section split by `[מעבר שקף]`) MUST be represented in the lesson output.** Never silently skip a slide. At minimum, include one sentence summarizing it.

*In `diagnostic` mode — cover only `session.weak_sections`; all other slides get a single-sentence acknowledgment.*

For every slide, choose the format based on `session.mode`:

---

### Mode: socratic

Instead of explaining first, lead with a question:

1. **Pose the challenge** — one sentence framing the problem or concept from the slide, without revealing the answer. E.g. "מה לדעתך קורה כשמודל שפה מקבל טקסט ארוך מידי?"
2. **Wait** — let the learner respond. Do not give hints yet.
3. **Guide, don't tell** — if the answer is wrong or incomplete, respond with a Socratic prompt (a question that nudges, not an explanation). Max 2 rounds of hints.
4. **Confirm and complete** — once they reach the right idea, affirm it and add any key detail they missed (max 2 sentences).
5. Move to the next slide.

The learner drives the pace. If they ask "just explain it" mid-slide, switch to Journey Format for that slide only and continue socratic from the next.

---

### Mode: standard (default)

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

**The learner can switch learning mode at any time** — "standard", "socratic", "diagnostic", or in Hebrew "הסבר לי" / "הדרך אותי" / "בחן אותי". Apply from the next slide onward.

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
