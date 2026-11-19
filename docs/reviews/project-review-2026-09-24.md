# Tov-learn — Project Review (multi-persona panel)

**Date:** 2026-09-24 · **Scope:** all tracked files except `courses/_archive/` · **Status:** read-only review, no repo changes made
**Working files:** `.review-panel/<persona>.round1.md` (independent reviews) and `.round2.md` (debate outcomes, merges, votes)

---

## 1. Executive summary

1. The engine is a promising idea. But the **active course content was ported from the archived "AI Engineer" course and never re-authored**. Lessons welcome learners to the wrong course, use 3.x/5.x lesson numbers, and claim prior lessons (Make/n8n, WhatsApp bots) that don't exist. All 7 panelists flagged this, and it is the #1 consensus priority.
2. **The Claude Code lessons (1.2, 1.3) teach facts that are wrong as of today** (verified against code.claude.com/docs):
   - Hooks "block on exit 1". Only exit 2 blocks, so the safety lab's guard doesn't guard.
   - Skills are taught as JSON files. They are `SKILL.md` files.
   - A project-root `MEMORY.md`, which auto memory never reads.
   - Routines defined inside CLAUDE.md.
   - Invented permission modes.
   - Wrong install commands.
   - Hebrew voice dictation, which isn't supported.
3. **Two one-line data bugs hide or break whole lessons.** `COURSE.md` omits 2.1/2.2, so resume and the dashboard skip "What is an API". Lesson 0.4 uses `[SLIDE TRANSITION]` instead of `[מעבר שקף]`, so the core prompt-engineering lesson arrives as one English block.
4. **Perishable AI facts are stale and contradict each other.** Module 0 names 4.6/4.7-era models, which are now Legacy, and gives three different lineups and context windows. It also advises temperature 0–0.5, which is deprecated on current Claude models and discouraged on the course's own Gemini 3 labs. Lesson 2.4 "Structured Output" presents JSON mode as schema-guaranteed and never makes a schema call.
5. **The final projects can't all be completed as written:**
   - non-existent `wrangler trigger cron`
   - a paid tier despite the "all free tier" promise
   - untaught RAG and Python Workers
   - self-reported completion

   They also **prescribe injection-prone designs** (a token-holding PR-review agent, a public WhatsApp bot), and the course never mentions prompt injection.
6. **The repo's own tooling contradicts what it teaches:**
   - A PowerShell Stop hook fires after every reply. It errors on macOS, Linux, WSL and Windows+Git Bash, and does nothing even where it runs.
   - All data helpers are PowerShell-only.
   - `/learn` sits in legacy `.claude/commands/`, leaking 16 model-invocable `/learn:*` entry points.
7. **Beginners can't get in.** Installing Claude Code is taught *inside* the tutor that needs it. There is no Hebrew zero-to-running guide and no terminal basics.
8. **CI prints `PASSED` on every one of these defects.** Content lint is the regression guard that would have caught items 1 and 3.
9. **Recommended direction:** structural option **B, "targeted re-platform, staged"** (§3). First, a quick-win PR that fixes the one-line bugs, deletes the hook and strips the archive residue. Then re-author lessons 0.x/1.2/1.3/2.4 and the capstone against a dated facts file. Then migrate `/learn` to a skill with cross-platform Python helpers and a data schema.
10. There are **no unresolved dissents**. Every severity dispute was settled with fetched evidence, most notably `/undo`, which *is* a `/rewind` alias, and prompt injection, which ended at unanimous P0.

---

## 2. Consensus priorities (ranked)

**How the ranking works:**
- **Vote points:** each panelist's top-10 vote gives 10 points to rank 1 down to 1 point to rank 10. A shared slot counts half each.
- **Order, per the brief:** Tier 1 = P0 wrong or outdated lesson/course content. Tier 2 = P0 platform and onboarding. Tier 3 = P1. Within a tier, items are ordered by vote points.
- **Rank is not execution order.** Several Tier-2/3 items are one-hour fixes and belong in the first PR (see "Quick-win PR" at the end of this section).

**Tier 1 vote summary:**

| # | Merged id | Sev | Top-10 votes | Points |
|---|---|---|---|---|
| 1 | M-archive-residue | P0 | 7/7 | 57 |
| 2 | M-1.2-setup-facts | P0 | 6/7 | 48 |
| 3 | M-1.3-claude-code-features | P0 | 6/7 | 48 |
| 4 | M-course-md-missing-2.1-2.2 | P0 | 6/7 | 34 |
| 5 | M-0.4-slide-marker | P0 | 6/7 | 28 |
| 6 | M-capstone-feasibility | P0 | 4/7 | 20 |
| 7 | M-prompt-injection-security | P0 | 4/7 (ta ranked it 11th) | 19.5 |
| 8 | M-prereq-sequencing | P0 | 3/7 | 18 |
| 9 | M-model-lineup-stale | P0 | 4/7 | 17 |
| 10 | M-2.4-structured-output | P0 | 2/7 | 10 |
| 11 | junior-03 (1.6 Supabase) | P0 | 1/7 | 5 |
| 12 | M-02-claude-vs-gemini-coherence | P0 | 1/7 | 5 |

**Tier 2:** M-stop-hook-powershell (P0, 5/7, 30 points) and novice-01 onboarding (P0, 3/7, 23 points).

**Tier 3 (P1):** M-ci-validator-gaps (5/7 voters, 8 points), M-verification-testing, M-settings-progress-schema, M-commands-to-skills, M-assessment-alignment, and others.

---

### Tier 1 — P0: wrong or outdated lesson and course content

#### 2.1 M-archive-residue: the course introduces itself as a different course — **P0**
- **Raised by:** all 7 (instructor-01, novice-02, ta-02, senior-dev-08, ai-engineer-05, agentic-expert-10, junior-07). Coordinator: instructor.
- **Evidence:**
  - `2.1_script.txt:1-3` "שיעור חמש נקודה אחת בקורס AI Engineer … בשיעור ארבע נקודה שש"; the lead confirmed this.
  - `0.2_script.txt:1-3,13-15` "ברוכים הבאים לקורס AI Engineer", describing an 8-module, 156-hour course with Make/n8n/ManyChat.
  - `1.1_script.txt:5` "בשיעורים הקודמים בנינו אוטומציות עם Make ו-n8n, בנינו בוטים לוואטסאפ".
  - `1.2_script.txt:229-235` points to lessons "3.3/3.7".
  - The last slide of `1.8_script.txt` says the next module is "מודול ארבע … יצירת תמונות".
  - Exercise headers are wrong too (`0.2_exercises.md:3,7`, and 2.x → "5.x").
  - `1.8_exercises.md:1` starts with a leaked LLM preamble ("בטח, בשמחה…").
  - Six files under `courses/ai-dev` contain "AI Engineer"; the lead confirmed this with grep.
- **Why it matters:** the tutor paraphrases these bridges, so every learner is told about prior learning that never happened. That undermines trust on day one and confuses beginners ("did I skip Make/n8n?").
- **Alternatives:**
  - **A. Mechanical pass.** Fix headers, numbers and strings, and add a CI denylist. *Effort:* S (1–2 days). *Risk:* narrative seams remain. *Beginner impact:* removes the false prerequisites.
  - **B. Re-author every opening and closing bridge** against the AI Dev syllabus, plus A. *Effort:* M. *Risk:* low. *Beginner impact:* high; bridges become real advance organizers.
  - **C. Rewrite Module 0 wholesale** (with 2.8) and do A for modules 1–2. *Effort:* M–L.
- **Panel recommendation:** **B**, with Module 0's rewrite folded into 2.8 and 2.9, and the denylist from 2.15.

#### 2.2 M-1.2-setup-facts: the first hands-on lesson teaches wrong commands and modes — **P0**
- **Raised by:** novice-03/-04/-05, junior-01, agentic-expert-05/-06/-07/-08/-21, senior-dev-05; restructure from instructor-16 (P1). Coordinator: novice.
- **Evidence:**
  - **Install:**
    - `1.2_script.txt:27` points to `claude.ai/download`, which is the Desktop app, not the CLI installer.
    - `:31` and `1.2_exercises.md:16` use `brew install claude-code`; it needs `--cask`.
    - `:17-19` says Node 18 works; the npm package needs Node 22+.
    - `:21` says "WSL עדיף"; native Windows is first-class.
  - **Permission modes:**
    - `:153-163` lists "five modes" including an invented "Restricted" mode.
    - `1.2_exercises.md:108` "Ask Mode (ברירת מחדל)" is wrong, because Pro, Max and Team start in `auto`. The experiment won't reproduce, and it takes three Shift+Tab presses to reach plan mode.
    - A deny rule `Bash(rm *)` is presented as a safety boundary; it doesn't stop `/bin/rm` or `bash -c`.
  - **Voice:** `:5,171` promises "עשרים שפות נתמכות, כולל עברית". Hebrew is not among the 20 dictation languages, and the API-key login fallback disables voice.
  - **Commands:**
    - `:187` says the CLI has no cost counter; `/usage` (alias `/cost`) exists.
    - `:73` says `/undo` "undoes the last file change". `/undo` is an alias of `/rewind` and opens the checkpoint menu.
    - `:131` lists course skills (`/create-lesson`, `/commit`) that don't exist.
  - **Sources:** code.claude.com/docs/en/setup, /permission-modes, /voice-dictation, /commands.md (raw).
- **Alternatives:**
  - **A. Correct the facts in place.** *Effort:* S. *Risk:* the lesson stays overloaded (7 levels, 5 modes, voice and pricing in one lesson).
  - **B. Rewrite and split** into a graded core (install, first session, permission cycle with auto as the Pro default, plan mode, `/rewind`, `/init` → first CLAUDE.md, `/usage`) plus optional "going further" cards (voice, pricing, levels). *Effort:* M. *Beginner impact:* highest, since this is where zero-coders drop out.
  - **C. Link to the official install page instead of listing commands**, and turn install into a "verify what you installed" checklist (`claude --version`, `claude doctor`). *Effort:* S–M. Least perishable, but the page is English-only (`code.claude.com/docs/he/setup` returns 404) and assumes terminal literacy, which recreates the novice-01 gate. *Lead-added, not debated; rejected in the objection round.*
- **Panel recommendation:** **B.**
  - **Install commands:** the lesson gives the official commands in Hebrew context: `curl -fsSL https://claude.ai/install.sh | bash`, `irm https://claude.ai/install.ps1 | iex`, `winget install Anthropic.ClaudeCode` and `brew install --cask claude-code`.
  - **Staleness guard:** a "last verified <date>" link to code.claude.com/docs/en/setup, plus the §2.15 denylist.
  - **End of install:** the verify checklist from C (`claude --version`, `claude doctor`).
  - **Voice:** becomes an optional, ungraded exercise done in English, and the lesson says honestly that Hebrew is not supported.
  - *(Amended after novice's objection; see §5.)*

#### 2.3 M-1.3-claude-code-features: the extensibility lesson's labs can't work — **P0**
- **Raised by:** agentic-expert-01..04, junior-02, senior-dev-04, instructor-09. Coordinator: agentic-expert.
- **Evidence:**
  - **Hooks:**
    - `1.3_script.txt:27` "if PreToolUse returns non-zero … blocked", and `:29` has the guard return exit 1. Per hooks.md, only exit 2 blocks, so the `rm` guard lets deletion through.
    - `1.3_exercises.md:83` asks for a Y/N hook. Hooks can't read the TTY; the mechanism for this is `permissionDecision: "ask"`.
  - **Skills:**
    - `1.3_script.txt:19,23` teaches skills as "קובץ ג'ייסון … הפעלה אוטומטית כטרו", and `1.3_exercises.md:124` grades "JSON format".
    - Per skills.md, skills are `.claude/skills/<name>/SKILL.md` with YAML frontmatter, and the `description` drives invocation.
  - **Memory:** `1.3_script.txt:11` and `1.3_exercises.md:33` create a project `MEMORY.md`. Auto memory lives in `~/.claude/projects/<p>/memory/`.
  - **Scheduling:**
    - `1.3_exercises.md:108` defines routines in CLAUDE.md. Routines are created with `/schedule` (Pro+, minimum interval 1h, run on a fresh clone).
    - `/loop` is framed as run-until-done; that is `/goal`.
    - Stopping via "Ctrl+C or /stop" is wrong: Esc stops a self-paced loop, and `/stop` only stops background sessions.
- **Alternatives:**
  - **A. Correct each exercise in place.** *Effort:* S–M. Keeps a crowded lesson.
  - **B. Rebuild 1.3 around a graded core.** CLAUDE.md with `/init`; auto memory via `/memory`; one SKILL.md; one exit-2 PreToolUse hook with a negative test (it blocks, and `/bin/rm` / `python -c` don't bypass it); `claude mcp add`; one read-only custom subagent. Each gets a hands-on exercise. Rules, imports, headless, plugins, agent teams, workflows and routines go on optional unquizzed cards. *Effort:* M.
  - **C. B, plus use the repo's own `.claude/` as the worked example**, so learners inspect Tov-learn's SKILL.md and hooks. *Effort:* M–L; depends on 2.13 and 2.18.
- **Panel recommendation:** **B now, C after the skills migration.** Agreed by agentic-expert, instructor, novice and junior.

#### 2.4 M-course-md-missing-2.1-2.2: resume and the dashboard never offer the API fundamentals — **P0**
- **Raised by:** ta-01, instructor-05, senior-dev-03, novice-10; related note in ai-engineer-05. Coordinator: ta.
- **Evidence:**
  - `COURSE.md:16` lists module 02 as "2.3–2.6", with rows only for 2.3–2.6 (`:35-38`); the lead confirmed this.
  - `resume.md:21` picks "the first lesson in COURSE.md with no progress file".
  - `status.md:156` builds "one card per lesson from COURSE.md".
  - After 1.8, the learner jumps straight to Webhooks.
- **Alternatives:**
  - **A. Add the two rows.** *Effort:* XS.
  - **B. Generate the lesson list from disk** (folder scan or `COURSE.yaml`) so it can't drift. *Effort:* S.
  - **C. A, plus a CI check both ways** (COURSE.md ↔ folders). *Effort:* XS–S.
- **Panel recommendation:** **A + C immediately.** B as part of structural option B/C.

#### 2.5 M-0.4-slide-marker: the core prompt-engineering lesson is one undivided English slide — **P0**
- **Raised by:** ta-02, instructor-02, senior-dev-02, novice-09, ai-engineer-06. Coordinator: ta.
- **Evidence:**
  - `0.4_script.txt` has **0** `[מעבר שקף]` and **19** `[SLIDE TRANSITION]`; the lead confirmed this.
  - It is English-only and 4,425 words, against 1.1–2.5k for the other lessons.
  - `teaching.md:25`, `quiz.md:14` and `slides.md:25` split only on the Hebrew marker.
  - `0.4:172` also gives the effort levels as "standard, high, or maximum". The real values are `low|medium|high|xhigh|max` (platform.claude.com/docs/en/build-with-claude/effort).
- **Alternatives:**
  - **A. Swap the markers only.** *Effort:* XS. It stays an English lesson in a Hebrew course.
  - **B. Translate and re-author in Hebrew with `[מעבר שקף]`**, fixing its stale model and effort facts at the same time (see 2.9). *Effort:* M.
  - **C. Make the splitter accept both markers**, plus a CI minimum-marker check. *Effort:* XS. This is robustness only and doesn't fix the language.
- **Panel recommendation:** **A as a stop-gap in the quick-win PR, then B**, with C's CI check.

#### 2.6 M-capstone-feasibility: the graded final projects can't all be completed as written — **P0**
- **Raised by:** junior-06, instructor-12, ai-engineer-11/-19/-12, senior-dev-20. Coordinator: junior.
- **Evidence:**
  - **Project C:**
    - `projects.md:457` uses `wrangler trigger cron`, which isn't a command. Local testing is `wrangler dev` + `curl …/cdn-cgi/local/scheduled`.
    - The Python handler is `on_scheduled(event, env, ctx)`; it should be `scheduled(self, controller, env, ctx)` (developers.cloudflare.com/workers/configuration/cron-triggers).
    - Python Workers are never taught.
  - **Project D:**
    - Its hosting contradicts itself (FastAPI + Tunnel vs a "long-running" Workers server).
    - It costs "~$5/חודש", against `projects.md:37`'s "everything on the Free Tier".
  - **Project B:** targets Cloudflare Pages, but Cloudflare now says "Start new projects with Workers".
  - **Project A:** needs Supabase Vector/RAG, which is never taught, and fits WhatsApp Business setup into "2.5 שעות".
  - **Completion:** it is self-reported ("סמן שלב כ-Done", `project.md:105-109`), and the rubric has weights but no level descriptors.
  - **Data:** Gemini's free tier says "Content used to improve our products: Yes" (ai.google.dev/gemini-api/docs/pricing), yet Project A routes real customer messages through it.
  - **Why it matters:** `projects.md:12` says a failing live demo doesn't pass.
- **Alternatives:**
  - **A. Fix commands and targets in place**, keeping the current designs (correct cron testing and handler; Workers or Vercel for B). *Effort:* S–M. *Risk:* keeps untaught Python Workers and RAG.
  - **B. The panel's re-design:**
    - Projects C and D move to **GitHub Actions**, conditional on 1.8 first adding an Actions lab (CI plus a `schedule:` trigger).
    - Project D is hardened: `pull_request` only, never `pull_request_target`; a read-only `GITHUB_TOKEN` plus `pull-requests: write`; no model key on fork PRs; the diff treated as data; no push/merge tools; a red-team step.
    - Project B moves to **Vercel**.
    - Project A puts its 20-Q&A knowledge base **in context**, with RAG as an optional stretch, plus a free-tier data warning.
    - Add a phase ↔ prerequisite-lesson map, a leveled rubric and tutor-verified phase checkpoints.
    - *Effort:* M–L.
  - **C. Reduce to 1–2 capstones** (one guided, one open). *Effort:* M. Less to maintain, but less choice.
- **Panel recommendation:** **B.** One wording nuance, not a dissent: instructor's note says "RAG lab before A", but the coordinator's recorded fix makes RAG optional because the knowledge base fits in context.
- **UNVERIFIED:** whether GitHub exposes secrets to fork PRs in the configured setup; whether `google-genai` runs on Pyodide Python Workers (moot under B).

#### 2.7 M-prompt-injection-security: no LLM-security coverage, while the capstones prescribe injectable agents — **P0**
- **Raised by:** senior-dev-06/-14, ai-engineer-10/-15 (security half), ta-18. Coordinator: senior-dev. Unanimous P0 after debate; ta and instructor moved up from P1.
- **Evidence:**
  - `grep -rliE "prompt injection|הזרקת"` over the lessons and `security.md` finds 0 files.
  - **Project D** (`projects.md:490-650`) is an agent that reads untrusted PR diffs while holding a GitHub token. **Project A** is a public WhatsApp bot. **Lesson 2.6** gives an MCP agent filesystem access with no trust discussion.
  - **`security.md` itself:**
    - `:128-136` ships a `timingSafeEqual` snippet with no length guard. That it throws on unequal lengths is UNVERIFIED against the Node docs page.
    - `:17-60` curls `/.env` and POSTs to `/api/upload-doc` on **any** URL "silently", with no ownership check.
  - **Standards:** OWASP LLM Top 10 2025 lists LLM01 Prompt Injection and LLM06 Excessive Agency (genai.owasp.org/llm-top-10). The MCP spec treats tool content as untrusted.
- **Alternatives:**
  - **A. Add an "LLM app security" section to 2.4/2.6**, fix the `security.md` snippet and add the ownership gate. *Effort:* S–M.
  - **B. A new lesson 2.7 "Securing LLM apps":**
    - direct and indirect injection
    - least-privilege tools
    - model output treated as untrusted
    - server-side keys
    - cost and rate limits
    - a red-team step in each capstone
    - an "LLM" phase in `/learn security`

    *Effort:* M.
  - **C. Thread security through every build lesson** (1.3 hooks, 1.6 RLS and keys, 2.6 MCP, the capstones) as checklist items. *Effort:* M–L. Best retention, most authoring.
- **Panel recommendation:** **B**, with C's checklist items in each capstone. The ownership gate and snippet fix go in the quick-win PR.

#### 2.8 M-prereq-sequencing: prerequisites are used before they're taught — **P0**
- **Raised by:** instructor-03/-04, novice-08 (a, b, d, e), junior-11, ai-engineer-14 (Python part), ai-engineer-05 (reorder part). Coordinator: instructor.
- **Evidence:**
  - Module 0 runs backwards: the advanced 0.1 mental model comes before the 0.2 intro, and the tool survey is repeated three times.
  - Lessons 2.1–2.4 already use Python (requests, SDK, Flask, Pydantic); installing Python, venv and basics only comes in 2.5.
  - Lesson 1.1 homework needs Claude Code, Python and FastAPI before 1.2 installs anything.
  - Lesson 1.4 deploys before 1.8 teaches deployment.
  - The step from 1.4 to 1.5 is a cliff (Prisma plus local Postgres).
  - Module 01 is TypeScript and module 02 is Python, and the switch is never explained.
- **Alternatives:**
  - **A. Reorder and fill gaps:**
    - reorder Module 0 as intro/limitations → mental model → prompt and context engineering
    - merge the surveys into one dated landscape card
    - add a **0.0 "terminal & files"** lesson and a **2.0 "Python setup & basics"** lesson (from the first half of 2.5)
    - remove premature homework
    - a note in 1.5 on why module 01 is TS

    *Effort:* M.
  - **B. A, plus "one app through 1.4 → 1.8":** Next.js + Supabase directly, no Prisma or local Postgres, deployed in 1.8 (junior-04 alternative #1, endorsed by instructor). *Effort:* M–L. It flattens the cliff and gives 1.8 something real to deploy.
  - **C. Make Python an external prerequisite.** *Rejected by the panel:* a never-coder can't pass an external gate.
- **Panel recommendation:** **A + B.**

#### 2.9 M-model-lineup-stale: perishable model facts are frozen at Feb–Mar 2026 and contradict each other — **P0**
- **Raised by:** ai-engineer-01/-02/-07/-08/-17, novice-06/-14, instructor-10, junior-12, agentic-expert-10/-22, senior-dev-15. Coordinator: ai-engineer. This cluster absorbed "M-unsourced-claims" as a citation-policy sub-point.
- **Evidence:**
  - **Contradictory lineups:**
    - `0.1_script.txt:53` "Sonnet 4.6 … מאתיים אלף Tokens". Sonnet 4.6 has a 1M context (platform.claude.com/docs/en/models/sonnet-4-6/overview), so `0.1_exercises.md:113` asks the learner to "discover" an overflow that doesn't exist.
    - `0.2_script.txt:61,99-103` gives "GPT-5.4, Opus 4.6, Sonnet 4.6, Gemini 3.1 Pro" and a 1M context.
    - `0.3_script.txt:5` "מרץ 2026" prices, which the ROI exercise reuses.
    - `0.4_script.txt:3` gives "GPT-5.5, Opus 4.7, Sonnet 4.6".
  - **Current reality:** the models overview (platform.claude.com/docs/en/about-claude/models/overview) lists Fable 5.1, Opus 5.5, Sonnet 5 and Haiku 4.5; the 4.6/4.7 models are Legacy.
  - **Temperature:** `0.1_script.txt:69-75` says to use temperature 0–0.5 in production.
    - Claude's API reference: "Deprecated. Models released after Claude Opus 4.6 do not support setting" it (platform.claude.com/docs/en/api/messages/create).
    - Gemini 3: "strongly recommend keeping … 1.0"; lower values risk looping (ai.google.dev/gemini-api/docs/gemini-3).
  - **Other facts:**
    - Token counting uses OpenAI's tokenizer.
    - The "2026 research" statistics are unsourced.
    - `0.2_script.txt:129` makes an income promise with no source.
- **Alternatives:**
  - **A. Update names and prices in place.** *Effort:* S. *Risk:* it rots again within months.
  - **B. Separate perishable facts from teaching:**
    - Narrate in tiers ("frontier / balanced / fast-cheap").
    - Keep one dated `courses/ai-dev/landscape.md` with IDs, context windows and prices, each with an official URL and a "verified on" date. The tutor reads it at lesson time, and `quiz.md` never tests it.
    - A CI lint flags model strings not listed in that file.
    - Replace the temperature advice with effort/thinking level plus schemas plus evals.
    - A citation policy: every number gets a source URL and date, and there are no income promises without a source.

    *Effort:* M.
  - **C. B, plus the tutor fetches the providers' live model pages** at lesson time. Less to maintain, but it depends on the network and permissions and isn't deterministic. *Not debated.*
- **Panel recommendation:** **B.**

#### 2.10 M-2.4-structured-output: presents JSON mode as schema-guaranteed and never makes a schema-constrained call — **P0**
- **Raised by:** ai-engineer-03, junior-09; supported by instructor. Coordinator: ai-engineer.
- **Evidence:**
  - `2.4_script.txt:47` says `json_object` means "ה-API עצמו יוודא … תואם". OpenAI: "only Structured Outputs ensure schema adherence" (developers.openai.com/api/docs/guides/structured-outputs).
  - `2.4_exercises.md:163-200` hard-codes the model's response. The only real schema call in the course is in `projects.md:~103-115`.
  - Gemini's `generateContent`, which every lab uses, is now "legacy" (still supported). The **Interactions API** is "Generally Available as of June 2026 and recommended for all new projects" (ai.google.dev/gemini-api/docs/interactions).
- **Alternatives:**
  - **A. Correct the claim and add a live `generateContent` `response_schema` exercise.** *Effort:* S. Consistent with the other labs, but on the legacy API.
  - **B. Rename the lesson "JSON & Structured Outputs"**, with:
    - a live Interactions API `response_format` + Pydantic exercise
    - a comparison table: Claude `output_config.format` / `messages.parse`; OpenAI `json_schema` strict
    - a small golden-set eval exercise

    Lesson 2.2 documents once why the tool labs stay on `generateContent` (Python automatic function calling exists only there), or migrates them. *Effort:* M.
  - **C. Teach it through a provider-agnostic validation library.** *Lead-added, not debated; currency UNVERIFIED.*
- **Panel recommendation:** **B.**

#### 2.11 junior-03: lesson 1.6 (Supabase) is built on deprecated or invalid pieces — **P0**
- **Raised by:** junior. Standalone; no overlap and no challenges.
- **Evidence:**
  - **MCP command:** `1.6_exercises.md:99` uses `claude mcp add supabase --project-ref … --access-token …`, which is invalid. The hosted command is `claude mcp add --scope project --transport http supabase "https://mcp.supabase.com/mcp"` with `read_only`/`project_ref` parameters (supabase.com/docs/guides/getting-started/mcp).
  - **Keys:** `:17-22,168` use anon keys and `NEXT_PUBLIC_SUPABASE_ANON_KEY`. Supabase is "deprecating the anon and service_role keys by the end of 2026" (supabase.com/docs/guides/api/api-keys).
  - **Auth UI:** `:81` uses `@supabase/auth-ui-react`, unmaintained since 2024; its community repo was archived in October 2025.
- **Alternatives:**
  - **A. Fix the command, keys and auth package in place.** *Effort:* S.
  - **B. Rebuild 1.6 on current Supabase** (hosted read-only MCP, publishable/secret keys, `@supabase/ssr`) as part of the one app carried through 1.4→1.8 (see 2.8 B). *Effort:* M.
- **Panel recommendation:** **B.** Do A first if the rebuild is further than a few weeks away, because the anon keys stop working at the end of 2026.

#### 2.12 M-02-claude-vs-gemini-coherence: module "02 Claude API" has no Claude exercise, and scripts and exercises use different providers — **P0 (mismatch) / P1 (naming alone)**
- **Raised by:** ai-engineer-04, instructor-11, junior-07 (rename part), senior-dev-20. Coordinator: ai-engineer. Instructor accepted the P0/P1 split.
- **Evidence:**
  - Commit `98b31ae` moved the exercises and `projects.md` to Gemini but left the scripts narrating Claude.
  - `2.5_script.txt:42-57` makes a raw Claude `requests.post` with `os.getenv("CLAUDE_API_KEY")`. The SDK variable is `ANTHROPIC_API_KEY`, and the learner only has a Gemini key.
  - The folder is `02-claude-api` and COURSE.md calls the module "Claude API".
  - `0.1_script.txt:59` promises prompt caching "כשנגיע ל-Claude API"; it never comes.
- **Alternatives:**
  - **A. Provider-agnostic module:**
    - rename it "LLM APIs & Integrations"
    - teach concepts once, with a Claude/OpenAI/Gemini syntax table
    - free Gemini labs, plus an optional Claude-track box
    - align the scripts with the exercises
    - state "Claude Pro $20/mo, $0 API spend" in the README and COURSE.md

    *Effort:* M. *Beginner impact:* high; honest and free.
  - **B. Keep "Claude API"** and give cohorts instructor-provided or budget-capped Claude keys, with Gemini as a fallback. *Effort:* M, plus ongoing cost and key management. Consistent with the brand.
  - **C. Two tracks per lab**, each with Gemini and Claude variants. *Effort:* L. Double the maintenance.
- **Panel recommendation:** **A.**

---

### Tier 2 — P0: platform and onboarding

#### 2.13 M-stop-hook-powershell: the repo's own hook errors after every reply, and core helpers are PowerShell-only — **P0 for the hook / P1 for the helpers**
- **Raised by:** senior-dev-01/-13, agentic-expert-12/-13, ta-03/-13, novice-11, junior-08. Coordinator: senior-dev. 5/7 votes, 30 points; the highest-scoring non-content item.
- **Evidence:**
  - **Failure:**
    - `.claude/settings.json` has a `Stop` hook that runs `powershell … '$env:CLAUDE_PROJECT_DIR\.claude\scripts\auto-save-progress.ps1'`; the lead confirmed this.
    - There is no `powershell` on Linux, macOS or WSL, so every turn shows a "hook error" notice.
    - Under bash, the default shell, `$env` is expanded away. senior-dev reproduced this: the path becomes `':CLAUDE_PROJECT_DIR\...'`, so the hook also fails on Windows + Git Bash.
  - **Wrong event:** `Stop` fires once per turn; `SessionEnd` is the session-end event.
  - **No-op:** the script exits early unless `%TEMP%\tov_current_lesson.txt` exists. Only `generate-slideshow.ps1:30` writes that file, and that script needs slide assets no course has.
  - **PowerShell-only helpers:** TTS (`learn.md:17-33`), the setup RTL check, export/import, and slides.
  - **Contradiction:** lesson 1.2 recommends WSL.
- **Alternatives:**
  - **A. Delete the hook.** *Effort:* XS. Nothing is lost, since it's a no-op.
  - **B. One stdlib `python3` helper CLI** (e.g. `tovlearn.py save|due|status|export|import`) for all data operations, with PowerShell only for optional Windows TTS. Document the OS support matrix in the README. *Effort:* M.
  - **C. Port each `.ps1` to cross-platform `pwsh` 7.** *Effort:* M. Learners would have to install pwsh, which is hostile to beginners.
- **Panel recommendation:** **A in the quick-win PR, then B.** An opt-in async Stop hook for TTS and progress checkpoints can come back later (see 2.20).

#### 2.14 novice-01: no path from zero to a running `/learn` — **P0**
- **Raised by:** novice. Supported by instructor and agentic-expert (top-10 votes) and senior-dev (refinement). 3/7 votes, 23 points.
- **Evidence:**
  - **Prerequisites:** `README.md:23-34` says only "Claude Code installed (Pro plan or higher)", "git clone", then "Open the cloned folder in Claude Code". There are no install steps, no terminal basics and no costs.
  - **Chicken-and-egg:** installing Claude Code is taught in 1.2, which `/learn` delivers, and `/learn` needs Claude Code to run.
  - **Official beginner routes the course ignores:** the docs offer the Desktop app ("use Claude Code without the terminal") and a terminal guide for first-timers (code.claude.com/docs/en/setup, /desktop, /terminal-guide).
- **Alternatives:**
  - **A. A Hebrew `GETTING-STARTED.md`** readable outside Claude Code, covering:
    - a costs and accounts table (Pro $20/mo, $0 API)
    - the Desktop app as the route to get `/learn` running
    - downloading the repo as a ZIP or with git
    - `/learn setup`
    - troubleshooting (`claude doctor`)

    Plus a mandatory **0.0 terminal & files** lesson before 1.2, which Desktop's integrated terminal can host. *Effort:* S–M.
  - **B. A, plus plugin distribution later**, so no clone is needed. *Effort:* M–L. Blocked on 2.13 and 2.18.
- **Panel recommendation:** **A now, B later.**

---

### Tier 3 — P1: significant gaps

#### 2.15 M-ci-validator-gaps: the validator passes on every defect above — **P1**
- **Raised by:** novice-10, junior-10, senior-dev-12, ta-14, instructor-13, agentic-expert-19. Coordinator: novice. 5 of 7 panelists put it in their top 10, always near the bottom, as the regression guard.
- **Evidence:**
  - `tests/validate_structure.py:26-46` hard-codes 6 modules and never parses `learn.md`.
  - The lead ran it today and got "PASSED — all checks OK".
- **Alternatives:**
  - **A. Extend the Python validator with content lints**, combining all six panelists' proposals:
    - parse routes and every `Read .claude/…` reference
    - COURSE.md ↔ folders
    - header numbers ↔ folders
    - at least N `[מעבר שקף]` markers per script and no `[SLIDE TRANSITION]`
    - a denylist (archive strings, `brew install claude-code` without `--cask`, "Restricted Mode", "קוד יציאה אחד", JSON skills, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `wrangler trigger`)
    - model strings ↔ `landscape.md`
    - the settings template ↔ its schema
    - no `powershell` in `settings.json`
    - relative links
    - CLAUDE.md table ↔ files

    *Effort:* S–M.
  - **B. Split into pytest files** (`test_structure`, `test_content`, `test_snippets` using `py_compile`/`json.load` on fenced code) and run CI on Ubuntu, Windows and macOS. *Effort:* M.
  - **C. Later: behaviour evals of `/learn`** (`claude plugin validate` / `claude plugin eval`). *Effort:* M.
- **Panel recommendation:** **A, then B.** C after the plugin work.

#### 2.16 M-verification-testing: no verification or testing discipline, and no evals — **P1**
- **Raised by:** senior-dev-07, ai-engineer-09, instructor-18 (evals part). Coordinator: senior-dev. The duplicate proposals "M-evals-verification" and "M-missing-evals-rag" were withdrawn.
- **Evidence:**
  - **The course's thesis:** `1.1_script.txt:21` "אתה לא קורא כל שורה בפירוט. אתה בודק שהתוצאה עובדת", and `:31` "אתה לא מסתכל על הפרטים הטכניים".
  - **The missing caveat:** the course never adds the original "throwaway weekend projects" scope of vibe coding (https://simonwillison.net/2025/Mar/19/vibe-coding/).
  - **No tests anywhere:** `grep -rliE 'pytest|vitest|jest|TDD'` over lessons 1.4–1.8 and module 02 returns 0 files (lead re-ran it).
  - No build lesson reviews a diff as the check on AI output.
  - There is no evals lesson.
- **Alternatives:**
  - **A. A required verify loop in the 1.4–1.7 exercises:** commit → read the diff → failing test → implement → run → `/rewind` on failure, plus a CI lab in 1.8. Graded in the capstone.
  - **B. A dedicated evals lesson in module 02:** a golden set, exact-match and schema checks, and LLM-as-judge caveats.
  - **C. B only as optional material**, with a core golden-set exercise in 2.4.
- **Panel recommendation:**
  - A, with its required verify loop in 1.4–1.7 and a CI lab in 1.8.
  - A core golden-set eval in 2.4, with the full evals lesson optional.
  - A capstone rubric that requires passing tests/CI and an eval score (ai-engineer-09 proposed about 10% weight).
  - *(Corrected after senior-dev's objection: the draft had dropped the required verify loop and the capstone criteria, which all three members proposed.)*

#### 2.17 M-settings-progress-schema: settings and progress data drift, and spaced repetition is weak — **P1**
- **Raised by:** ta-05/-08/-09, senior-dev-10/-16, instructor-14, novice-13. Coordinator: ta.
- **Evidence:**
  - **Settings:** three incompatible versions (the template, what `setup.md:253-274` writes, and what the reader modules expect).
  - **Progress files:** three writers and formats.
  - **Thresholds:** the skip-quiz pass mark is 7 (`teaching.md:66`) but "Mastered" needs 8+ (`progress.md:69`, `status.md`). A learner who tests out at 7 skips the lesson yet shows "In progress" forever and is never counted as mastered. *(Wording corrected after instructor's objection.)* Quiz scores step by 1.5 (`quiz.md:59`), producing 7.5 and 8.5, which fall between the integer buckets at `quiz.md:92-95`.
  - **Reviews:**
    - `resume.md:72` re-teaches the whole lesson on review instead of quizzing first.
    - A lesson finished without a quiz never gets a review date.
    - Intervals are fixed and based only on the latest score.
- **Alternatives:**
  - **A. Document the schema in markdown and align the thresholds.** *Effort:* S. The model still parses free-text dates.
  - **B. Structured data with one writer:**
    - a `settings.schema.json` with a version field
    - machine-local values in a non-exported `local.json`
    - a progress schema with ISO dates
    - a single stdlib writer (`progress.py save|due|status`)
    - one mastery constant and continuous score buckets
    - reviews quiz first, intervals expand on success, and every finished lesson gets a review date

    *Effort:* M.
  - **C. B, plus an established spaced-repetition algorithm** (e.g. SM-2 or FSRS). Raised as a later step by instructor-14 (`instructor.round1.md:189`), senior-dev-16 and ta-09. The agreed B starts with a simple expanding rule. *(Attribution corrected after ta's objection.)*
- **Panel recommendation:** **B now, C later.**

#### 2.18 M-commands-to-skills: `/learn` uses legacy commands and leaks 16 model-invocable entry points — **P1 (plugin sub-step later)**
- **Raised by:** agentic-expert-14/-15, senior-dev-11, ta-17 (global-install part). Coordinator: agentic-expert.
- **Evidence:**
  - `learn.md:1` has no frontmatter.
  - Every module is exposed as `/learn:quiz`, `/learn:import`, …. This session's own skill list shows them.
  - These entry points skip `learn.md`'s settings and profile load.
  - `import.md`'s destructive full-replace mode can be invoked by the model.
  - The global install (`setup.md:279-309`) can't work, because every path is relative to the repo.
  - skills.md: "Custom commands have been merged into skills."
- **Alternatives:**
  - **A. Add frontmatter and `disable-model-invocation` to the current commands**, and delete the global install. *Effort:* S.
  - **B. Migrate to `.claude/skills/learn/{SKILL.md, modules/, scripts/, schema/}`**, with modules as supporting files. *Effort:* M.
  - **C. B, plus a plugin and marketplace.** *Effort:* L. It must not ship the PowerShell hook, and course paths must resolve from the plugin root.
- **Panel recommendation:** **B, then C.** C is P2, agreed by novice and agentic-expert. It is blocked on 2.13 and B: the plugin must not ship the PowerShell hook, and course paths must resolve from the plugin root (senior-dev). *(Corrected after agentic-expert's objection.)*

#### 2.19 M-assessment-alignment: no objectives, leaked or missing answer keys, classroom exercises in a solo tutor — **P1**
- **Raised by:** instructor-06/-07/-08/-15, senior-dev-16, ta-19, novice-08(c). Coordinator: instructor.
- **Evidence:**
  - No lesson states learning objectives.
  - `teaching.md:174` says to present exercises "exactly as written".
  - Exercises assume a classroom: "עצרו ופנו למדריך" (`2.1_exercises.md:17`), "שתפו בקבוצת הקורס" (`1.1_exercises.md:76`).
  - **Answer keys:** module 0 shows them inline (`0.2_exercises.md:49-56`); modules 1–2 have none.
  - **Quiz scoring:** the free-text item is 40% of the score, with no rubric.
- **Alternatives:**
  - **A. 3–5 observable objectives per lesson**, with quiz items mapped to them, tutor-only keys and rubrics for every exercise, and a 3-point free-text rubric weighted at most 25%.
  - **B. A, plus a `delivery: solo|cohort` setting** chosen in setup; the tutor adapts pair and class exercises only in solo mode.
- **Panel recommendation:** **A + B.**

#### 2.20 ta-12 + novice-13: closing the terminal, or typing "עצור", loses the session — **P1**
- **Raised by:** ta and novice.
- **Evidence:**
  - The only stop trigger is the English "stop" (`learn.md:80,95`).
  - There is no per-slide checkpoint.
- **Alternatives:**
  - **A. Hebrew command aliases** (עצור / סיום / בחן אותי / המשך). *Effort:* XS.
  - **B. A Stop hook that parses `last_assistant_message`** for the mandatory `### 📚 N / total` header to record `last_slide`, plus a SessionEnd final save. The docs confirm Stop hooks receive `last_assistant_message`. *Effort:* S–M. Requires teaching.md to make the header mandatory, folding in the orphaned `display.md`.
- **Panel recommendation:** **both.** A goes in the quick-win PR.

#### 2.21 Other P1s: each agreed, low controversy

| Id | Issue (evidence) | Options → recommended |
|---|---|---|
| M-1.7-subagents-review (agentic-expert-09, junior-05) | "8 subagents" (the default is 20); worktrees aren't automatic (need `isolation: worktree`); `/security-review` needs a git diff; ultracode must be enabled in `/config` on Pro; `/commit` doesn't exist (`1.7_exercises.md:17`) | A: fix the facts · **B: A + a custom read-only `.claude/agents/reviewer.md`, a worktree demo, and a `/code-review` → GitHub Actions path** |
| M-vat-17 (instructor-09, ai-engineer-16, junior-02) | Israeli VAT given as 17% (`1.3_exercises.md:36`, `2.2_exercises.md:175-176,184`, `2.6_script.txt:53`); it has been 18% since 1 Jan 2025 | **A: change to 18% now** · B: move into `landscape.md`/config |
| M-slides-dead-code (senior-dev-09, ta-07) | About 530 lines of PowerShell slide viewer that no course can run (no slide assets exist) | **A: delete** · B: rebuild as a cross-platform HTML viewer generated from the scripts, only if wanted |
| ta-06 | The TTS rate maps to 0 and −2, outside WinRT's 0.5–6.0 range; `"` and `$` in the text are injected into the PowerShell literal (`learn.md:26`) | A: clamp and escape · **B: an opt-in async Stop hook reading stdin JSON, installed in `settings.local.json`** |
| ta-10(a) | No learner or cohort id, although the course is taught to classes (`projects.md:12,29`; `project.md:28`) | **A: `learner.id`/`cohort` plus `/learn export --summary` (P1)** · B: a full cohort dashboard (P2, after 2.17) |
| ta-11 | Import's "merge (Recommended)" copies every file with `-Force` and never compares dates (`import.md:113-121`); "replace all" has no backup; export defaults to the repo folder | **Auto-backup before import; merge by newest mtime; export outside the repo** |
| junior-04 | Lesson 1.5's Prisma setup predates Prisma 7; `create-next-app` now writes its own CLAUDE.md/AGENTS.md | A: update · **B: remove Prisma via 2.8 B (one app, Next.js + Supabase)** |
| ai-engineer-15 | Lesson 2.6 narrates `uvicorn vat-server:mcp`, which won't work, and cites FastMCP 3.0 (current is 4.0); no transport, auth or trust content | **Fix the commands and versions; add transport and trust notes (links to 2.7)** |
| ai-engineer-12 | The Gemini free tier uses submitted content to improve Google's products, and this isn't disclosed | **A "practice data only" box in 2.2's key setup and in Project A** (part of 2.6/2.12) |
| instructor-16 | Lesson 1.2 is overloaded (7 levels, 5 modes, voice, pricing) | Resolved inside 2.2 B |

#### P2/P3 backlog (agreed, lower priority)
- **M-learner-data-permissions (P2; ta-04, agentic-expert-17).** The "silent" saves outside the repo prompt in Manual mode; auto mode (the Pro default) prompts only on the first outside read. Fix with `additionalDirectories` and allow rules, and tell learners what gets written where.
- **M-script-format-tts (P2; instructor-17, senior-dev-19, agentic-expert-20).** 244 `[warm]`/`[calm]` tags, and commands spelled out in Hebrew letters ("קלוד נקודה אם די"). Keep a canonical script with real identifiers and code fences, and generate the TTS variant from it.
- **ta-16 (P2).** The RTL dashboard has English-only labels, status shown by color only, "not started" text at about 2.8:1 contrast, and no ARIA on the score bars.
- **ta-15 (P2).** `display.md` claims to be loaded by other modules but none reference it, and it contradicts them.
- **Docs drift (P2; senior-dev-17, ta-17, agentic-expert-18).**
  - The README's example output uses archived-course titles.
  - The README's "run `/learn` in your other project" flow can't work.
  - CLAUDE.md's module table misses `display.md`, `project.md` and `security.md`, and gives no test command.
  - CONTRIBUTING describes a script format no lesson uses.
- **senior-dev-18 (P2).** `changes.md` is organised by personal branch names; switch to Keep-a-Changelog.
- **novice-07 (P2).** Cowork is described wrongly.
- **novice-12 (P2).** The README and FAQ don't serve a Hebrew beginner.
- **novice-14 (P2).** Hype tone; now covered by 2.9's citation policy.
- **ai-engineer-13, -18, -21 (P2).** Caching, batch and observability; webhook production essentials; agent vs workflow framing. Optional advanced track, **except** ai-engineer-13's minimal 429 retry/backoff snippet (SDK retries, or exponential backoff with jitter). That snippet is **core** and goes into 2.2/2.5, because `2.2_exercises.md:424` already hands learners `429 RESOURCE_EXHAUSTED` with only "המתינו רגע". *(Corrected after ai-engineer's objection; this was the split agreed with novice.)*
- **agentic-expert-22, ai-engineer-20, junior-13 (P3).** Minor inaccuracies and polish.

#### Quick-win PR (execution order, not rank): each item under about an hour
1. Add 2.1/2.2 to `COURSE.md` (2.4).
2. Delete the Stop hook from `.claude/settings.json` (2.13 A).
3. Change VAT from 17% to 18% in 3 files (2.21).
4. Replace the 0.4 markers with `[מעבר שקף]` as a stop-gap (2.5 A).
5. Fix lesson and exercise header numbers, remove "AI Engineer" strings and the leaked `1.8_exercises.md:1` preamble (2.1 A).
6. Add an ownership confirmation to `/learn security` and fix the `timingSafeEqual` snippet (2.7).
7. Add Hebrew stop/quiz/continue aliases (2.20 A).
8. Remove the broken global-install section (2.18).
9. Add the first content lints: COURSE.md ↔ folders, marker count, header numbers, archive denylist (2.15 A).

---

## 3. Structural options

**A — Keep the structure, fix the content.**
- **What:** the quick-win PR, then in-place rewrites of lessons 1.2, 1.3, 2.4 and 1.6, the capstone fixes and content lints. Keep `.claude/commands/`, the PowerShell helpers and the free-text data files.
- **Effort:** about 1–2 weeks of authoring.
- **Pros:** fastest, lowest risk, no migration.
- **Cons:** non-Windows learners are still second-class. Data keeps drifting because the LLM parses free text. The repo keeps contradicting what lesson 1.3 teaches. Perishable facts start rotting again at once.
- **Beginner impact:** medium; fixes what they hit, but not the Mac/Linux/WSL experience.

**B — Targeted re-platform, staged (recommended).**
- **Stage 0:** the quick-win PR.
- **Stage 1, content:**
  - Separate perishable facts from teaching: `landscape.md` with sources, and a citation policy.
  - Re-author Module 0 in the order intro → mental model → prompting, and 0.4 in Hebrew.
  - Add the 0.0 terminal and 2.0 Python lessons.
  - Split 1.2 and 1.3 into a graded core plus optional cards.
  - Carry one app through 1.4→1.8, with current Supabase and no Prisma.
  - Make module 02 "LLM APIs & Integrations": Gemini labs on the Interactions API, a new structured-outputs 2.4, a 2.7 security lesson, a golden-set eval exercise.
  - Re-design the capstones with GitHub Actions, hardening and verified checkpoints.
- **Stage 2, platform:**
  - `.claude/skills/learn/{SKILL.md, modules/, scripts/, schema/}`
  - a stdlib `python3` helper CLI for progress, export and import
  - settings and progress JSON schemas with ISO dates
  - quiz-first spaced repetition with expanding intervals
  - opt-in async Stop-hook TTS
  - `additionalDirectories`
  - pytest content tests on a three-OS CI matrix
  - a Hebrew GETTING-STARTED guide
- **Stage 3, later:** a plugin and marketplace, the cohort report, per-objective assessment.
- **Effort:** about 4–8 weeks, in increments that each ship on their own.
- **Pros:** fixes root causes (drift, platform lock-in, perishable facts). The repo becomes a worked example of its own lesson 1.3. Every stage is independently valuable.
- **Cons:** a real migration. Existing learners' `~/skill-tutor-tutorials` data needs a one-time converter. There are more moving parts to review.
- **Beginner impact:** highest. It fixes the entry path, the OS parity and the lesson accuracy.

**C — Full rebuild: course as data, plugin-first.**
- **What:**
  - Courses become structured data: `COURSE.yaml` generated from disk, `script.md` as the canonical source with the TTS text derived from it, `sources.md` per lesson, and objectives and answer-key blocks.
  - `/learn` ships as a plugin from day one.
  - The curriculum is rebuilt around learning objectives, with a core track and an advanced track (evals, RAG, caching/batch, agent patterns, observability).
  - CI adds behaviour evals of the tutor.
- **Effort:** about 2–3 months.
- **Pros:** the cleanest long-term architecture; supports several courses and cohorts; easy to distribute.
- **Cons:** a long time before learners see fixes; a big-bang risk; plugin details are partly UNVERIFIED (the plugin-root path variable, caching); more than a small volunteer team can easily carry.
- **Beginner impact:** high eventually, low in the short term.

**Panel direction:** B. It is consistent with every agreed merge fix: skills migration P1, plugin later, Python helpers, schema, `landscape.md`, and the core/advanced split. C's elements (`COURSE.yaml`, `script.md` with derived TTS, `sources.md`, the plugin) are adopted as later stages of B rather than a big-bang rebuild. Nobody argued for A as the end state, only as B's Stage 0.

---

## 4. Per-area summary

**Lessons: Module 00 (AI fundamentals).**
- It is AI-Engineer residue: wrong course, wrong numbering, and forward references to modules that don't exist.
- It runs backwards (0.1 before 0.2), and the tool survey is repeated three times.
- The model lineups are stale and contradict each other, and the temperature advice is wrong.
- Lesson 0.4 is English-only and never split into slides, and its effort levels are wrong.
- Other errors:
  - Cowork is described wrongly.
  - The hallucination exercise marks an unconfirmed claim as true.
  - Answer keys are shown inline.
- **Direction:** re-author as intro → mental model → prompt and context engineering, with one dated landscape card.

**Lessons: Module 01 (Claude Code).**
- 1.1 claims Make/n8n/WhatsApp prior learning and assigns homework before anything is installed.
- 1.2 has wrong install commands, invented permission modes, Hebrew voice, a mis-described `/undo`, and is overloaded.
- 1.3's hooks, skills, memory and routines labs can't work.
- 1.5 predates Prisma 7.
- 1.6 uses deprecated Supabase keys and MCP syntax.
- 1.7 has wrong subagent and worktree facts and a missing diff.
- 1.8 deploys a new toy app instead of the one built in 1.5–1.7.
- **Direction:** a graded core plus optional cards, and one app carried through 1.4→1.8.

**Lessons: Module 02 ("Claude API").**
- The scripts narrate Claude, but the exercises use Gemini, on the now-legacy `generateContent`.
- 2.4 presents JSON mode as structured outputs.
- 2.5 is mostly Python basics, taught after 2.1–2.4 already need Python.
- 2.6 has a wrong MCP run command and a stale FastMCP version.
- VAT is given as 17%.
- COURSE.md hides 2.1 and 2.2.
- **Direction:** "LLM APIs & Integrations", a 2.0 Python lesson, a new structured-outputs 2.4 on the Interactions API, a 2.7 security lesson, and a golden-set eval exercise.

**Lessons: Module 03 (final project).**
- Commands that don't exist, the wrong Python handler, Pages for Next.js, and a paid tier that breaks the free-tier promise.
- Untaught RAG, WhatsApp and Python Workers.
- Designs open to prompt injection.
- Completion is self-reported.
- **Direction:** GitHub Actions for C/D after an Actions lab in 1.8, a hardened Project D, Vercel for B, an in-context knowledge base for A, and tutor-verified checkpoints.

**`/learn` skill modules.**
- Legacy `.claude/commands/` with no frontmatter; 16 leaked `/learn:*` entry points that skip setup.
- `display.md` is orphaned.
- The broken global install.
- `teaching.md:174` forces exercises to be presented "exactly as written", so every broken step reaches the learner.
- `security.md` probes any URL without asking whether the site is the learner's, and ships a broken snippet.
- The model is told to do TTS and silent saves by instruction, which lesson 1.3 itself says should be hooks.
- **Direction:** a skill directory with modules as supporting files, `disable-model-invocation`, and hooks for deterministic behaviour.

**Dashboard and progress.**
- Three settings versions and three progress writers.
- Free-text dates in mixed formats.
- Mastery thresholds 7 vs 8, and score buckets with gaps.
- Reviews re-teach instead of quizzing first; un-quizzed lessons never come due.
- Only the English "stop" saves; no per-slide checkpoint.
- Import overwrites newer data.
- The dashboard has English labels on an RTL page, low contrast, color-only status, and no cohort view.
- **Direction:** JSON schemas, one Python writer, quiz-first expanding intervals, localized and accessible dashboard generated from data, and a learner/cohort id plus a summary export.

**Testing and CI.**
- `validate_structure.py` checks 6 hard-coded modules for existence only and passes today.
- **Direction:** content lints (§2.15), then pytest on a three-OS matrix, then behaviour evals of the tutor.

**Docs and memory files.**
- README: its prerequisites are insufficient for beginners, its sample output uses archived-course titles, its "run `/learn` in another project" flow doesn't work, and it understates the OS limits.
- CLAUDE.md's module table is missing 3 modules and there's no test command.
- `.claude/rules/` could scope rules for content authors (verify claims against the docs and cite URLs; numbers must match folders; marker convention).
- CONTRIBUTING describes a script format no lesson uses.
- `changes.md` is organised by branch name, not as a changelog.
- **Direction:** a Hebrew GETTING-STARTED guide, a docs pass, rules files, and Keep-a-Changelog.

**Scripts and cross-platform.**
- Every `.ps1` script is Windows-only: the no-op Stop hook, 530 lines of dead slide code, TTS with an out-of-range rate and string injection, and export/import.
- `security.md` uses bash while the rest uses PowerShell.
- **Direction:** delete the hook and the slides code, use one stdlib Python CLI for data, keep PowerShell only for optional Windows TTS, and publish an OS support matrix.

---

## 5. Unresolved disagreements

**There are no formal dissents.** Every severity dispute was settled with fetched evidence within the 3-exchange limit. Resolved disputes worth knowing:
- **`/undo`:** junior and agentic-expert said `/undo` doesn't exist; novice said it's an alias. The raw `code.claude.com/docs/en/commands.md` line 130 reads "`/rewind` … Aliases: `/checkpoint`, `/undo`", checked twice with curl (`.review-panel/novice.evidence-undo.txt`). Both conceded; their WebFetch summaries had dropped the table cell. The defect is the lesson's *description* of `/undo`.
- **Prompt-injection severity:** ta and instructor started at P1 ("a missing topic is a gap"); senior-dev and ai-engineer held P0. It is now unanimous P0, because the capstone *prescribes* insecure designs and `security.md` ships broken code.
- **M-02 severity:** instructor held P1 because the Gemini labs work; ai-engineer and junior held P0. The compromise was P0 for the script/exercise mismatch (the `CLAUDE_API_KEY` demo) and P1 for the naming alone.
- **Hebrew voice:** novice started at P0; it is now P1, because voice is not a learning goal and falls back to English. Windows voice typing doesn't support Hebrew either, so there's no OS workaround.
- **ta-04 permission prompts:** P1 → P2, because the Pro default is auto mode, where only the first outside read prompts.
- **ta-10 cohort view:** split into P1 (learner id plus summary export) and P2 (full dashboard).
- **Language of instruction:** instructor withdrew the "TypeScript for the whole course" option. Python stays for 02/03, with a 2.0 setup lesson.
- **Capstone A RAG:** instructor withdrew "add a RAG lesson"; the knowledge base goes in context and RAG becomes an optional stretch.

**Objection round on §2 (Phase 3):** 7/7 replied. One replied "no objection" (junior). Six raised one objection each, and **all six were accepted and incorporated**, so no objection is left as a dissent:

| Teammate | Objection | Resolution |
|---|---|---|
| novice | §2.2's "link the official page, don't copy commands" was a lead-added option that contradicts the agreed fix. The setup page is English-only (`/docs/he/setup` returns 404). | Recommendation now gives the official commands in Hebrew context, with a "last verified" link and the CI denylist. |
| instructor | §2.17 mislabeled `teaching.md:66` (the skip-quiz pass mark of 7) as a mastery threshold. | Reworded: pass mark 7 vs "Mastered" 8+, so a learner who tests out at 7 shows "In progress" forever. |
| ta | §2.17 option C (SM-2/FSRS) was wrongly marked lead-added. It was raised by instructor-14, senior-dev-16 and ta-09. | Attribution fixed; recommendation is "B now, C later". |
| ai-engineer | The P2 backlog put all of ai-engineer-13 on the optional track. The agreed split keeps a minimal 429 retry/backoff snippet in the core. | Backlog line amended. |
| agentic-expert | §2.18 recorded a P1-vs-P2 plugin "disagreement" that came from crossed messages. | Now P2, agreed by both. |
| senior-dev | §2.16's recommendation dropped the required verify loop in 1.4–1.7 and the tests/CI/eval-score criteria in the capstone rubric, and its evidence lacked citations. | Recommendation and evidence rewritten. |

ta also flagged a line-number slip (`generate-slideshow.ps1:29` → `:30`); it's fixed.

**Minor open points (not dissents):**
- **Capstone A wording:** instructor's merge note says "RAG lab before A"; the coordinator's recorded fix (junior, backed by ai-engineer) makes RAG optional. This report follows the coordinator.
- **Gemini tool labs:** migrate them to the Interactions API, or document once why they stay on `generateContent`. The decision is left to the author of 2.2.
- **Remaining UNVERIFIED items:**
  - whether GitHub exposes secrets to fork-PR workflows in the proposed setup
  - whether `google-genai` runs on Python Workers (moot if the capstone moves to GitHub Actions)
  - the plugin-root path variable and caching
  - that `timingSafeEqual` throws on unequal lengths (not confirmed on the Node docs page)
  - whether "only Gemini gives a free API key" holds as a blanket claim
  - any plan-level context cap in Claude Code
  - the Windows-side run of the Stop hook (the bash mangling is reproduced; native Windows is untested)

---

## 6. Method note

- **Panel:** 7 Claude agent teammates, each a persona, run as an agent team with a lead as moderator (who did not review):
  - `novice`: career-changer, never coded
  - `junior`: bootcamp graduate
  - `senior-dev`: AI-skeptical senior engineer, also covering repo engineering
  - `ta`: entry-level teaching assistant running cohorts
  - `instructor`: learning-experience designer
  - `agentic-expert`: Claude Code and agentic workflows
  - `ai-engineer`: LLM and API engineering
- **Phases:**
  1. **Independent review, no messaging.** 127 findings in total: novice 14, junior 13, senior-dev 20, ta 19, instructor 18, agentic-expert 22, ai-engineer 21.
  2. **Debate.** Each panelist challenged at least 2 findings from the other end of the beginner↔expert range, answered every challenge, and settled disputes with files and fetched sources, with at most 3 exchanges per point. Duplicates were merged into `M-*` clusters, each with a named coordinator. Each panelist then cast a ranked top-10 vote.
  3. **Lead synthesis**, followed by a single objection round on §2: 7/7 replied, 6 objections, all incorporated (see §5).
- **Date:** 2026-09-24. All "current state" claims come from pages the panelists fetched that day (code.claude.com, platform.claude.com, ai.google.dev, developers.openai.com, supabase.com, developers.cloudflare.com, docs.github.com, genai.owasp.org, modelcontextprotocol.io). Anything not confirmed is marked UNVERIFIED.
- **Lessons about method:**
  - WebFetch summaries can drop table cells (this caused the `/undo` error), so any "X is absent from the docs" claim must rest on the raw `.md` plus grep.
  - Running `cat -n` on several files at once shifted line numbers. ta and instructor published correction tables in their round-2 files; the citations here use the corrected numbers.
- **Lead spot-checks:** the lead confirmed these in the repo:
  - COURSE.md "2.3–2.6"
  - the 0/19 marker counts in 0.4
  - the PowerShell Stop hook
  - the "AI Engineer" strings (6 files)
  - the 2.1 opening line
  - `validate_structure.py` printing PASSED
- **Excluded:**
  - `courses/_archive/`, entirely
  - running `/learn` or touching real learner data
  - any paid or metered API call, and any use of credentials
- **Writes:** read-only on the repo. The only files written are `.review-panel/*` (git-excluded) and this report, later committed at `docs/reviews/project-review-2026-09-24.md`.
