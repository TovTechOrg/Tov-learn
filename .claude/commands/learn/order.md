# Lesson Order — Shared Rules (reference)

*Reference module, not routed. Read it when a hook note says earlier lessons are not complete, and whenever you suggest or start a lesson (`resume.md`, `setup.md`, `teaching.md`, `slides.md`, `quiz.md`).*

Respond in `session.language` throughout. Address the learner using `session.address`.

---

## Principle

**Lessons are learned in the course order** — the lesson list (`## רשימת שיעורים`) in the active course's `COURSE.md`. A lesson starts only when **every earlier lesson is complete**. The learner can't go from lesson A straight to lesson C without completing lesson B.

A lesson is **complete** when one of these is true:

1. **Finished** — all its slides were covered and its required exercises are done (`exercises.md`; exercises skipped under the paid-resources rule count as done). Its progress file `~/skill-tutor-tutorials/progress/lesson-{lesson_number}.md` has `**Slides covered:** all [N]`.
   - Lessons learned under the current rules get the line `**Exercises required:** yes` in their progress file when they start (`teaching.md` Step 3, `slides.md` Step 1).
   - Lessons learned before these rules have no such line. For those, covering all the slides is enough — shown by `**Slides covered:** all`, or by a row in the file's Sessions table whose "Sections Covered" says all (e.g. `All 15`, `All sections`). Their exercises aren't checked.
2. **Passed by a lesson skip quiz** — score 8+ (`teaching.md`, Step 3). Its progress file has `**Skip quiz passed:**`.
3. **Passed by a module skip quiz** — its whole module was passed (`quiz.md`, "Module Skip Quiz"). `~/skill-tutor-tutorials/progress/module-{X}.md` has `**Skip quiz passed:**`.

Reviewing an earlier lesson is always allowed.

---

## When earlier lessons are not complete

A hook checks this whenever a lesson starts and adds a note listing the earlier lessons that aren't complete. When that happens, **before teaching the requested lesson**:

1. Tell the learner briefly that lessons go in order, and which earlier lessons aren't complete yet.
2. Offer the ways to complete them, starting from the **first** incomplete lesson:
   - **Finish it** — continue its slides, or do its remaining exercises (following `exercises.md`).
   - **Lesson skip quiz** — for a learner who already knows that lesson (`teaching.md`, Step 3: pass mark 8; below 8, only the sections answered wrong are taught, then their related exercises).
   - **Module skip quiz** — for each earlier module the note lists (not the requested lesson's own module): one quiz passes the whole module (`quiz module X`; pass = 8+ and a correct answer for every lesson). If it isn't passed, the learner continues that module lesson by lesson.
3. Go with the learner's choice, in order, until every earlier lesson is complete. Only then start the requested lesson.

Don't start the requested lesson "just this once", even if asked; explain the rule kindly and offer the options above. The exercises rules (`exercises.md`), including the paid-resources exception, still apply.

A note that comes back while you're building a module skip quiz (you read the module's scripts) isn't about a lesson start — ignore it for that read.

---

## Suggesting the next lesson

The **next lesson** is always the first lesson in the course order that isn't complete. You may also suggest related lessons for **review** (e.g. from the knowledge map), but never suggest a later lesson as the next one to learn.
