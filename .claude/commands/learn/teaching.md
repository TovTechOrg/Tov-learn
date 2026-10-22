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

**Mark the lesson as taught under the exercises rule** — once the lesson actually begins (after any lesson-order note is handled, `order.md`): silently create or update `~/skill-tutor-tutorials/progress/lesson-{lesson_number}.md` so it contains the line `**Exercises required:** yes` (keep everything else already in the file). It tells the lesson-order check that this lesson follows the current rules, unlike lessons learned before them. Do this before any quiz (lesson skip quiz). Do not tell the learner you are saving.

**Load saved learning style from `~/skill-tutor-tutorials/settings.json`:**

- `session.mode` ← `learning_style.mode` (default: `"standard"`)
- `session.detail_level` ← `learning_style.detail_level` (default: `2`)

**If a saved style exists:** apply it silently — no question needed. Mention it once in the greeting so the learner knows (e.g. "נלמד במצב diagnostic, רמת פירוט 2 — כפי שהגדרת. אפשר לשנות בכל שלב.").

**If no `learning_style` in settings (first-time or missing):** ask the learner explicitly:

> **איך תרצה ללמוד?**
> - **standard** — אסביר כל שקף ואשאל שאלה בסוף (ברירת מחדל)
> - **diagnostic** — תבחן אותי קודם על כל שיעור: 8 ומעלה — השיעור עובר; פחות — תלמד רק את מה שטעיתי ונתרגל רק אותו
> - **socratic** — הדרך אותי דרך שאלות; אני אגלה את הרעיונות בעצמי
>
> בכל סגנון אפשר לבחור לכל שיעור בנפרד: ללמוד אותו, או להיבחן עליו קודם. בתחילת מודול אפשר גם מבחן אחד על כל המודול.

And ask for detail level (1 / 2 / 3).

After the session, if the learner changed mode or detail level mid-lesson, ask:
> "רוצה לשמור את ההעדפה הזו לשיעורים הבאים?"
If yes — update `learning_style` in `settings.json`.

**Reminder — always valid:** "ניתן לעבור בין המצבים בכל שלב — פשוט אמור 'standard', 'diagnostic', 'socratic' או 'הסבר לי' / 'בחן אותי' / 'הדרך אותי'."

---

**Learn the lesson, or quiz first — ask at the start of every lesson, in every style** (not when the learner is coming back to finish a lesson already in progress):

> "רוצה ללמוד את השיעור, או להיבחן עליו קודם? במבחן: 8 ומעלה מתוך 10 — השיעור עובר, בלי שקפים ותרגילים; פחות מ-8 — נלמד רק את מה שטעית בו ונתרגל רק אותו."

(adapt to `session.language` and `session.address`)

- Suggest **quiz first** when `session.mode == "diagnostic"`, otherwise **learn**. The learner decides for each lesson separately.
- At the **first lesson of a module**, also offer the **module skip quiz**: one quiz on the whole module (`quiz.md`, "Module Skip Quiz" — `quiz module X`; pass = 8+ and a correct answer for every lesson of the module).

**Learn** → ask what they already know about the topic, if anything. Use `learner_profile.md` to calibrate depth. Offer to skip sections they clearly already know. Then go to Step 4 and teach in the learner's style (a diagnostic-mode learner who chooses to learn is taught the standard way), then Step 5 with all the lesson's exercises.

**Quiz first** → Step 3B.

*(Speak greeting if TTS enabled)*

---

## Step 3B — Quiz First (Lesson Skip Quiz)

*When the learner chose "quiz first" in Step 3 — the suggested choice in diagnostic mode.*

1. Read `quiz.md` in **`quiz me full`** mode — quiz on the entire lesson. It's the lesson skip quiz: pass mark 8.
2. **Score ≥ 8 — passed.** Silently create or update `~/skill-tutor-tutorials/progress/lesson-{lesson_number}.md` so it contains the line `**Skip quiz passed:** X/10 (DD-MM-YYYY)` (keep everything else already in the file). The lesson is done: its slides and exercises aren't required. Because the sections behind any wrong answers won't be taught, explain each of them in detail after the review table (`quiz.md`, "Passed skip quiz — detailed explanations"). Then recommend the next lesson (`order.md`).
3. **Score < 8 — not passed.** Set `session.failed_skip_quiz = true` and teach only what the learner got wrong:
   1. Collect the **weak sections** (questions answered incorrectly or partially) and set `session.weak_sections` = the slide indices or topics they map to.
   2. Tell the learner:
      > "קיבלת X/10. עכשיו נעבור רק על הנושאים שהיו פחות ברורים, ונתרגל רק אותם."
      (adapt to `session.language`)
   3. Switch to Step 4 but **cover only the weak sections**, in the learner's style (the standard Journey Format for standard and diagnostic, guiding questions for socratic), scaled by `session.detail_level`. Skip sections the learner answered correctly — at most, a one-sentence "you already know this" acknowledgment.
   4. After covering them, offer a short follow-up quiz on those topics only (`quiz me` mode, scoped to the weak sections) — optional.
   5. Then proceed to Step 5 (End of Lesson). Only the exercises related to the weak sections are required (`exercises.md`, "After a failed skip quiz").

---

## Step 4 — Cover Every Slide

**IMPORTANT: Every slide (section split by `[מעבר שקף]`) MUST be represented in the lesson output.** Never silently skip a slide. At minimum, include one sentence summarizing it.

*After a failed skip quiz (Step 3B, any style) — cover only `session.weak_sections`; all other slides get a single-sentence acknowledgment.*

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
- **The goal is still to teach** — every sentence must make the concept land, not just restate it. Explain the *why* or the *so what*, even in one sentence.
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

0. **Mark the lesson's slides as done — silently, right away, before the exercises.** Create or update `~/skill-tutor-tutorials/progress/lesson-{lesson_number}.md` so it contains the lines `**Slides covered:** all [N]` and `**Exercises required:** yes` (keep everything else already in the file). This is how later lessons know this lesson's slides were finished and its exercises are required, even if the learner stops in the middle of the exercises (`order.md`). Do not tell the learner you are saving.

1. **Quick recap** — 2–3 bullet points summarizing the key takeaways from the entire lesson. Keep it sharp.

2. **Exercises — always, never skip. Present from the exercises file.** Exercises are part of every lesson, not an optional extra. First read `.claude/commands/learn/exercises.md` and follow it: create the tracking file `~/skill-tutor-tutorials/progress/exercises-lesson-{lesson_number}.md` with its header before the first exercise, and apply its paid-resources rule. If `session.failed_skip_quiz` is true, give only the exercises related to the sections the learner got wrong (`exercises.md`, "After a failed skip quiz"). Then go through the exercises from the loaded exercises file, one at a time:
   - Present each exercise exactly as written — do not rewrite or replace it
   - Wait for the learner to respond before moving to the next
   - For exercises that require an external tool (tokenizer site, external API, drawing, etc.) — tell the learner to go do it and come back with their results. When they return, give feedback on what they found
   - For exercises that can be done in the conversation — do them together here
   - Give specific feedback on every answer: what's right, what's missing, what to think about
   - If the learner is stuck, give one hint — not the answer
   - **After each exercise is completed**, silently append the learner's answers to `~/skill-tutor-tutorials/progress/exercises-lesson-{lesson_number}.md`:
     ```
     ## תרגיל [N] — [exercise title]
     **תשובה:** [learner's answer, verbatim or summarized if long]
     **פידבק:** [your feedback in one sentence]
     ---
     ```
     Create the file if it doesn't exist. Do not tell the learner you are saving.

3. **Quiz, mini project, or neither — optional, offer once** after exercises. Tell the learner plainly that this step is optional and that they can go on to the next lesson without it. They choose at most one:

   - **Quiz** → Read `.claude/commands/learn/quiz.md`
   - **Mini project** → a small hands-on task completable in 2–3 prompts with Claude (not an external tool unless the lesson topic is that tool)
   - **Neither** → skip to step 4.

   Neither the quiz nor the mini project is required before the next lesson — only the exercises are.

4. **Save progress silently** — write to `~/skill-tutor-tutorials/progress/lesson-{lesson_number}.md`:
   ```
   # Progress — Lesson X.Y

   **Completed:** [timestamp]
   **Slides covered:** all [N]
   **Summary:** [2–3 sentence summary of what was taught this session]
   ```
   Preserve any existing content already in the file (quiz scores, the `**Slides covered:**` and `**Exercises required:**` lines from step 0). Do not tell the learner you are saving. Then read `.claude/commands/learn/progress.md` and save full session summary.

*(Speak the recap and offer if TTS enabled)*

---

## Teaching Principles

- **Make asking for help normal.** Once per lesson, right after the first section, add one short line telling the learner they can say **נתקעתי** / **stuck** at any time — when something isn't clear or something they built doesn't work — and you'll help (`stuck.md`). Don't repeat it every section.
- **The primary goal is always to teach** — detail levels control length and depth, never whether teaching is happening. A 1-sentence response at detail level 1 must still make the concept click, not just name it.
- Use `session.language` for all output
- Max 5 sentences per teaching block — then the learner speaks
- Always emphasize **why** before **how**
- Use the learner's project from their profile as the primary example
- If the learner already knows a section — offer to skip it
- Be direct: if an answer is wrong, say so — then help them reach the right one
