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

Split the script into sections by `[מעבר שקף]`. English scripts use `[SLIDE TRANSITION]` instead; treat both markers the same. In text for the learner, call each section a **שקף** (slide), numbered as in the script — the same word in every reply, as in the style descriptions below — never "חלק".

**Freshness check (before teaching).** Skim the script and exercises for things that go stale: CLI commands, slash commands, model names, API endpoints, SDK method names, prices, plan limits. If you have web access, check the doubtful ones against the official docs. If something is wrong or you can't confirm it:
- Teach the correct, current version and tell the learner in one sentence that the slide is out of date.
- Silently append a line to `~/skill-tutor-tutorials/content-issues.md`: `DD-MM-YYYY | lesson X.Y | slide N | what is wrong | what is correct`. Instructors collect this file before each cohort.
- Never teach a command or API you believe does not exist.

---

## Step 3 — Open the Session

If COURSE.md marks this lesson as `רשות` (optional), say so in the greeting in one sentence and that skipping it is fine.

Greet the learner. State the lesson topic and number of sections, and say up front how many exercises the lesson ends with (count them in the exercises file). Exercises are part of the lesson, not optional. Give the greeting, the short intro and the "learn or quiz first" choice below in the same reply — don't announce what a later reply will contain.

If this is the learner's first lesson (no files in `~/skill-tutor-tutorials/progress/`), add one short paragraph: the course includes a personal project that applies the lessons as you go, plus a final project at the end, so it is worth keeping a project in mind from the start (see `/learn project`).

**If the learner already started learning this lesson** (its progress file has `**Exercises required:** yes`): this is a return to a lesson in progress, not a new start. Continue from where they stopped. If the slides are done (`**Slides covered:**` line), continue with the first exercise not recorded yet (`exercises.md`). If the slides aren't done, teaching mode doesn't save which slide the learner reached, so ask once, briefly, where to continue — e.g. "מאיפה נמשיך? כתבי את מספר השקף שעצרת בו, או **מההתחלה**." — and continue from there; if the file has a `**שקף אחרון:**` line (saved by slides mode), suggest the slide after it. Never restart from the first slide without asking. Don't offer the lesson skip quiz: once learning started, the lesson is completed by its slides and required exercises (`order.md`).

**Mark the lesson as taught under the exercises rule** — when the learner **starts learning** it: right after they choose **learn**, or right after a lesson skip quiz is **not passed** (Step 3B), together with saving that result. Silently create or update `~/skill-tutor-tutorials/progress/lesson-{lesson_number}.md` so it contains the line `**Exercises required:** yes` (keep everything else already in the file). It tells the lesson-order check that learning started under the current rules — the lesson skip quiz is no longer offered for it, and its exercises are required — unlike lessons not started yet or learned before these rules. Do not tell the learner you are saving.

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

(adapt to `session.language` and `session.address`; always say **"מתוך 10"** — the quiz has 9 questions, but the score is out of 10, so "8 ומעלה" alone reads like 8 of 9 correct)

- Suggest **quiz first** when `session.mode == "diagnostic"`, otherwise **learn** — except after a **module skip quiz that wasn't passed** (`~/skill-tutor-tutorials/progress/module-X.md` for this lesson's module, "Per lesson" results): in standard and socratic style, suggest **quiz first** only for a lesson whose module-quiz questions were **all** answered correctly, and **learn** for any other lesson. Whatever you suggest, the learner always chooses between both options, for each lesson separately — also when you mention a coming lesson, say you'll *ask* (with the suggested choice), never that it will start with a quiz.
- At the **first lesson of a module**, and only while **no lesson of that module was started** (none has a progress file under `~/skill-tutor-tutorials/progress/`) and the module skip quiz **wasn't taken before** (no `progress/module-X.md` — one attempt only), also offer the **module skip quiz**: one quiz on the whole module (`quiz.md`, "Module Skip Quiz" — `quiz module X`; pass = 8+ and a correct answer for every lesson of the module). If it isn't passed, the learner continues lesson by lesson, and at each lesson chooses again: learn it, or take its own skip quiz first. A lesson skip quiz is never mandatory.

**Learn** → mark the lesson as taught (above). Ask what they already know about the topic, if anything. Use `learner_profile.md` to calibrate depth. If they clearly know some sections, name those sections and offer to skip them, one question for all of them; add that all the lesson's exercises are still required, because only a lesson skip quiz can reduce them. Then go to Step 4 and teach in the learner's style (a diagnostic-mode learner who chooses to learn is taught the standard way), then Step 5 with all the lesson's exercises.

**Quiz first** → Step 3B.

*(Speak greeting if TTS enabled)*

---

## Step 3B — Quiz First (Lesson Skip Quiz)

*When the learner chose "quiz first" in Step 3 — the suggested choice in diagnostic mode.*

1. Read `quiz.md` in **`quiz me full`** mode — quiz on the entire lesson. It's the lesson skip quiz: pass mark 8.
2. **Score ≥ 8 — passed.** The lesson is done: its slides and exercises aren't required. Because the sections behind any wrong answers won't be taught, explain each of them in detail after the review table (`quiz.md`, "Passed skip quiz — detailed explanations"). After showing the result, silently create or update `~/skill-tutor-tutorials/progress/lesson-{lesson_number}.md` so it contains the line `**Skip quiz passed:** X/10 (DD-MM-YYYY)` (keep everything else already in the file). Then recommend the next lesson (`order.md`).
3. **Score < 8 — not passed.** Set `session.failed_skip_quiz = true` and teach only what the learner got wrong:
   1. Collect the **weak sections** (questions answered incorrectly or partially) and set `session.weak_sections` = the slide indices or topics they map to.
   2. Tell the learner:
      > "קיבלת X/10. עכשיו נעבור רק על הנושאים שהיו פחות ברורים, ונתרגל רק אותם."
      (adapt to `session.language`)
   3. After showing the result, save it (`quiz.md`) and mark the lesson as taught (Step 3) — learning starts now.
   4. Switch to Step 4 but **cover only the weak sections**, in the learner's style (the standard Journey Format for standard and diagnostic, guiding questions for socratic), scaled by `session.detail_level`. Skip sections the learner answered correctly — at most, a one-sentence "you already know this" acknowledgment.
   5. Then go straight to Step 5 (End of Lesson) — no extra quiz on the weak sections before the exercises. Only the exercises related to the weak sections are required (`exercises.md`, "After a failed skip quiz"). The usual optional quiz / mini project offer comes after them.

---

## Step 4 — Cover Every Slide

**IMPORTANT: Every slide (section split by `[מעבר שקף]`) MUST be represented in the lesson output.** Never silently skip a slide. At minimum, include one sentence summarizing it.

**Number slides from the script, not from memory.** Before each slide, take its number from its position in the split script (the Nth section is slide N), not from a running count in the conversation, and teach the slide that comes right after the last one shown. Before the last slide, check that every number up to it was shown; if one was missed, teach it first and say so in one sentence.

**If the learner asks to skip** (e.g. "דלגי") and it isn't clear what they mean, ask once, and include every option: skip this slide (one-sentence summary, then the next slide), go faster through the rest, or continue as is. Skipping slides never reduces the required exercises.

**One slide per message.** Teach exactly one slide, then stop and wait for the learner (an answer, `continue`, or a question). Never bundle several slides into one message, even at detail level 1 and even if the learner seems to be moving fast. The only exception: the learner explicitly asks for several at once (e.g. "show me slides 3 to 5"), and that applies to that one request only.

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
4. **Question** — one thinking question; wait for an answer before continuing. The learner must be able to answer it from this slide, an earlier slide, or an earlier lesson — if it builds on something earlier, name where (e.g. "כמו בתרגיל 3 בשיעור 2.5"). A "don't know" or partial answer gets a hint or a short explanation, never just "wrong".

Each block: max 5 sentences total.

### Detail Level 3 — Full Depth
Use the full Journey Format plus:
- Expand the insight to 4–5 sentences
- Add bullet points for key facts, numbers, or comparisons from the slide
- May include one extra "did you know" point not in the script if genuinely relevant
- Still ask a question and wait for an answer (answerable from the material learned so far, as in level 2)

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

After the learner has been shown the **last section**, do the following in order:

0. **Mark the lesson's slides as done — silently, right after the last section is shown, before the exercises.** Only after the last section's text is in front of the learner (never before it, in the same reply or an earlier one), create or update `~/skill-tutor-tutorials/progress/lesson-{lesson_number}.md` so it contains the lines `**Slides covered:** all [N]` and `**Exercises required:** yes` (keep everything else already in the file). After a failed skip quiz, write `**Slides covered:** all needed — weak sections only: [list] (after a failed skip quiz)` instead, so it doesn't read as if every slide was taught. This is how later lessons know this lesson's slides were finished and its exercises are required, even if the learner stops in the middle of the exercises (`order.md`). Do not tell the learner you are saving.

1. **Quick recap** — 2–3 bullet points summarizing the key takeaways from the entire lesson. Keep it sharp.

2. **Exercises — mandatory: always, never skip. Present from the exercises file.** Exercises are part of every lesson, not an optional extra. First read `.claude/commands/learn/exercises.md` and follow it: create the tracking file `~/skill-tutor-tutorials/progress/exercises-lesson-{lesson_number}.md` with its header before the first exercise, and apply its paid-resources rule. If `session.failed_skip_quiz` is true, give only the exercises related to the sections the learner got wrong (`exercises.md`, "After a failed skip quiz"). Then go through the exercises from the loaded exercises file, in order, one at a time:
   - Before the first exercise, say how many there are (e.g. "יש 4 תרגילים, נעבור עליהם אחד אחד").
   - Present each exercise exactly as written — do not rewrite or replace it — under its **original number** from the exercises file (after a failed skip quiz, e.g. exercises 1, 2 and 4 — not renumbered 1, 2, 3), and record it under the same number
   - **Never show a sample answer, solution or answer key before the learner answers.** If the exercises file includes one ("תשובה לדוגמה", a solution, a key), leave it out when presenting the exercise; use it only for your feedback afterwards
   - If the exercise says to submit something (homework, "הגישו עד השיעור הבא"), tell the learner that here, submitting means pasting it in this conversation for your feedback
   - When you repeat or shorten an exercise's instructions later (a reminder, a summary), keep the exercise's own step numbers ("שלבים 2–4"), never a new numbering
   - Wait for the learner to respond before moving to the next
   - For exercises that require an external tool (tokenizer site, external API, drawing, etc.) — tell the learner to go do it and come back with their results. When they return, give feedback on what they found
   - For exercises that can be done in the conversation — do them together here
   - Give specific feedback on every answer: what's right, what's missing, what to think about. Judge the answer by what the exercise asked. Don't mark the learner down for something the exercise didn't ask for; if you suggest more (e.g. a Production practice), say it goes beyond the exercise ("התרגיל ביקש X, וזה בסדר לתרגול; ב-Production…") so it doesn't read as a mistake
   - If the learner is stuck, give one hint — not the answer
   - **After each exercise's feedback has been shown** (never before it), silently append the learner's answers to `~/skill-tutor-tutorials/progress/exercises-lesson-{lesson_number}.md`:
     ```
     ## תרגיל [N] — [exercise title]
     **תשובה:** [learner's answer, verbatim or summarized if long]
     **פידבק:** [your feedback in one sentence]
     ---
     ```
     Create the file if it doesn't exist. Do not tell the learner you are saving.
   - **Self-check before moving on:** compare the number of exercises in the file with the number you presented. If any is missing, present it now.

3. **Quiz, mini project, or neither — optional, offer once** after exercises. Tell the learner plainly that this step is optional and that they can go on to the next lesson without it. They choose at most one:

   - **Quiz** → Read `.claude/commands/learn/quiz.md`
   - **Mini project** → a small hands-on task completable in 2–3 prompts with Claude (not an external tool unless the lesson topic is that tool)
   - **Neither** → skip to step 4.

   Neither the quiz nor the mini project is required before the next lesson — only the exercises are.

4. **Save progress silently** — after the learner has seen the feedback on the last exercise (and the quiz or mini project results, if they chose one) — write to `~/skill-tutor-tutorials/progress/lesson-{lesson_number}.md`:
   ```
   # Progress — Lesson X.Y

   **Completed:** [timestamp]
   **Slides covered:** all [N]
   **Summary:** [2–3 sentence summary of what was taught this session]
   ```
   Preserve any existing content already in the file (quiz scores, the `**Slides covered:**` and `**Exercises required:**` lines from step 0). Do not tell the learner you are saving. Then read `.claude/commands/learn/progress.md` and save full session summary.

5. **Lesson summaries file** — append this lesson's summary to `~/skill-tutor-tutorials/lesson-summaries.md` (create it if missing, with the main heading `# סיכומי שיעור`). Use a `## מודול [N]` heading per module (add it if missing) and under it `### שיעור X.Y — [title]` followed by 4–8 bullets of the key points **from the lesson material itself**, regardless of how the learner did in exercises or quizzes. If the lesson already has a section, replace it. If `settings.json → summaries_language` is `"en"` or `"both"`, also write `~/skill-tutor-tutorials/lesson-summaries-en.md` with the headings `# Lesson Summaries`, `## Module [N]`, `### Lesson X.Y — [title]`. Tell the learner once, at the end of their first lesson, that this file exists and that `summaries` shows it.

*(Speak the recap and offer if TTS enabled)*

---

## Teaching Principles

- **Make asking for help normal.** Once per lesson, right after the first section, add one short line telling the learner they can say **נתקעתי** / **stuck** at any time — when something isn't clear or something they built doesn't work — and you'll help (`stuck.md`). After that, keep it short: whenever a reply ends by asking the learner to move on, the same line also offers **נתקעתי** — e.g. "כתבי **המשך** כדי להמשיך, או **נתקעתי** אם משהו לא ברור." (adapt to `session.address`).
- **The primary goal is always to teach** — detail levels control length and depth, never whether teaching is happening. A 1-sentence response at detail level 1 must still make the concept click, not just name it.
- Use `session.language` for all output
- Max 5 sentences per teaching block — then the learner speaks
- Always emphasize **why** before **how**
- Use the learner's project from their profile as the primary example
- If the learner already knows a section — offer to skip it
- Be direct: if an answer is wrong, say so — then help them reach the right one
- **No black boxes on request.** When you write or show code, or use a tool or technology the learner did not choose, add one sentence on what it is and why it was picked. If the learner says `explain the code` / `הסבר את הקוד` or asks what something is, explain the code or technology line by line at their level, then return to the lesson.
- **Questions about project requirements set by the instructors** (what a deliverable must include, how an assignment will be graded) are not something you can know. Say so plainly and tell the learner to ask the instructors in Slack; you may suggest how to phrase the question. Questions about the lesson material itself you answer as usual.
- **English-only option.** If `settings.json → content_language` is `"en"`, teach, quiz and summarize fully in English, including terms that would normally stay in Hebrew. This helps learners who struggle with mixed Hebrew/English direction in the terminal.
