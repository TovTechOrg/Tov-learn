# Tov-learn — Project Redesign PRD

**Date:** 2026-09-25 · **Revised:** 2026-09-26, after an independent review (§5); **amended** 2026-09-29 by the locked Stage 0 spec (§8) · **Status:** decisions agreed in brainstorming; input to per-unit specs
**Input:** `docs/reviews/project-review-2026-09-24.md` (multi-persona panel review, 2026-09-24; section refs below as "§2.x")
**Scope:** the active course `courses/ai-dev/` and the `/learn` tutor. `courses/_archive/` is out of scope throughout.

---

## 1. Context and goal

Tov-learn is a Claude Code–based tutor that teaches Hebrew-speaking beginners, including people who have never coded, to build software with AI. The panel review found three kinds of problem:

- **Content** was ported from the archived "AI Engineer" course and is wrong or stale in places.
- **Platform:** the helpers only run on Windows, the data formats drift, and the command layout is legacy.
- **Onboarding:** a beginner has no way to get from nothing to a running `/learn`.

**Goal:** fix what learners hit now, then fix the root causes (drift, platform lock-in, facts going stale), in small increments that each ship on their own. The team is a small group of volunteers, and most of the work will go through Claude Code sessions.

### Assumptions
- **Fresh installs only.** The previous cohort has finished, and new learners start on a fresh install. Any existing install is assumed to come from the redesign itself. Anything left over from before the redesign that could trip it up is out of scope, and if it breaks, it breaks.
- **Testers only until the first-cohort gate (D10).** Until the gate passes, the course is used only by contributors and invited volunteers who accept data resets. Two temporary aids exist for them and are removed at the gate:
  - the README tester note (D2 item 13)
  - the clean-slate step in `/learn setup` (D2 item 14)

### Success criteria
1. A never-coder on Windows or macOS can follow `GETTING-STARTED.md` to a running `/learn`. This is checked by one real run-through per OS, and the Windows run starts from a machine with no Python and no Git.
2. Every graded lab and capstone can be completed on free tiers ($0 API; Claude Pro is the only paid item), checked by a dry run of each.
3. CI enforces every lint listed in review §2.15 A, plus the model-string, denylist, `node-version` and no-`python3` lints. Each lands in the unit named in D7c and is checked by a seeded regression.
4. The tutor gives the same results on macOS, Linux, WSL and Windows: no PowerShell-only data path, 3-OS CI.
5. Every perishable fact that learners see has a source URL and a "verified on" date.

### Non-goals
- A full rebuild or plugin-first re-platform (option C). Its pieces come in as later stages instead.
- New advanced lessons in Stage 1: the full evals lesson, RAG, caching/batch/observability, webhook production essentials, agent-vs-workflow framing. They stay in the backlog (D6d).
- SM-2/FSRS spaced repetition, the full cohort dashboard, TTS improvements beyond what's listed.
- Any change to `courses/_archive/`.
- Supporting, detecting or migrating installs from before the redesign (see Assumptions). The only exception is the temporary clean-slate step for testers.

---

## 2. Decisions

Each decision records what was chosen, why, and the facts verified during brainstorming or by the independent reviewer (marked "reviewer"). Facts the panel had already verified with sources are not repeated.

### D1 — Structural direction: option B (staged re-platform), with four changes
Stage 0 quick wins → the skills move (M) → Stage 1 content → Stage 2 platform → Stage 3 plugin.
1. **Stage 1 is split into slices that ship on their own**, ordered by where learners feel the pain (see §3).
2. **Hebrew GETTING-STARTED moves from Stage 2 to early Stage 1.** It is P0 (§2.14 "A now") and depends on no platform work.
3. **The skills move runs first, then the remaining platform work runs alongside Stage 1.**
   - Content and platform work *do* touch the same tutor files: G edits `setup.md`, F edits `quiz.md` and `teaching.md`, D5 edits `project.md`, D6a edits `security.md`.
   - So the move to `.claude/skills/learn/` (unit M, D8d) comes straight after Stage 0, and Stage 1 edits files in their final locations.
   - After M, S2a–S2d can run alongside Stage 1 under the **one-unit-per-file rule** (D10).
4. **Supabase keys are fixed early.** Supabase deprecates anon/service_role keys by the end of 2026. The key swap and the MCP command fix go in Stage 0 (D2 item 16). The `@supabase/ssr`/auth rewrite and removing Prisma stay in 1d.

*Why:* option A leaves the root causes in place. Option C (2–3 months, big-bang) is too big for this team.

### D2 — Stage 0: a 16-item quick-win PR
*Amended by the Stage 0 spec: see §8, items A1–A9.*

The review's 9 items, several tightened, and seven added:

| # | Item | Source |
|---|---|---|
| 1 | Add 2.1/2.2 rows to `COURSE.md` | §2.4 A |
| 2 | Delete the PowerShell Stop hook from `.claude/settings.json` | §2.13 A |
| 3 | VAT 17% → 18% in the 3 files | §2.21 |
| 4 | Replace `[SLIDE TRANSITION]` with `[מעבר שקף]` in 0.4 (stop-gap) | §2.5 A |
| 5 | Archive residue: the course-name strings, header numbers and the leaked `1.8_exercises.md:1` preamble. **Tightened:** also delete the claims about lessons that never happened: `1.1_script.txt:5` (Make/n8n/WhatsApp), the course description in 0.2, the "module 4 images" teaser at the end of 1.8, and the "3.3/3.7" pointers in 1.2. "AI Engineer" used as a **job title** (`0.2_script.txt:123-129`, `0.3_script.txt:111`) stays | §2.1 A+ |
| 6 | Add an ownership confirmation to `/learn security`; fix the `timingSafeEqual` snippet (length check first, or compare SHA-256 digests) | §2.7 |
| 7 | Hebrew stop/quiz/continue aliases | §2.20 A |
| 8 | Remove the broken global install from `setup.md` **and** from `README.md:46`; add the test command to CLAUDE.md | §2.18, D10 |
| 9 | First lints (details in D7c):<br>• COURSE.md ↔ folders<br>• a minimum `[מעבר שקף]` count, and no `[SLIDE TRANSITION]`<br>• header numbers ↔ folders<br>• a course-name denylist that matches the course name, not the bare phrase "AI Engineer"<br>• route and `Read .claude/…` references resolve<br>• no `powershell` in `settings.json`<br>• relative links resolve<br>Stage 0 adds only denylist entries it fully fixes; the rest arrive in F with the baseline. Lints skip `_archive/` and `old_B` | §2.15 A |
| 10 | **Added:** make the current 1.3 hook exercise safe to run. There is **no destructive test**: nothing deletes files, and learners aren't asked to try to delete anything. The script's exit-code claim (`1.3_script.txt:27,29`) is corrected. The Stage 0 spec decides the exact exercise, using these inputs (reviewer):<br>• exercise 5 (`1.3_exercises.md:75-85`) has no exit code<br>• it asks for a Y/N prompt, which hooks can't do because they have no terminal (hooks.md)<br>• it points at global settings; it should use project scope<br>• on Windows the PowerShell tool bypasses a `Bash`-only matcher<br>The full lab is replaced in 1a (D4c) | §2.3 |
| 11 | **Added:** `disable-model-invocation: true` frontmatter on the 15 `learn/*.md` sub-modules. This is a safety net in case unit M slips | §2.18 A |
| 12 | **Added:** move old Project B into its own `old_B` file, and make `/learn project` show "the final projects are being rebuilt" instead of a list until 1e (D5) | D5 |
| 13 | **Added:** a temporary tester note in `README.md`: "Fresh install only. Before testing, delete `~/skill-tutor-tutorials/` (`%USERPROFILE%\skill-tutor-tutorials` on Windows) and any old global install at `~/.claude/commands/learn.md` and `~/.claude/commands/learn/`." It is **removed at the first-cohort gate** (D10) | Assumptions |
| 14 | **Added:** a temporary **clean-slate step in `/learn setup`**. During the tester period it finds leftovers (`~/skill-tutor-tutorials/` and `~/.claude/commands/learn*`), **shows them, backs them up, and deletes them only after an explicit yes**. It is **removed at the gate**. It never deletes `.claude/settings.local.json` (D8b). The Stage 0 spec defines how it works | R1 |
| 15 | **Added:** bump `.github/workflows/validate.yml` from `checkout@v4`/`setup-python@v5` (both `node20`) to current action majors that run on `node24`, pinned by SHA (D7d) | R5 |
| 16 | **Added:** Supabase keys and MCP in 1.6:<br>• `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` / `SUPABASE_SECRET_KEY` replace the anon/service_role keys (`1.6_exercises.md:17-21,30,168`)<br>• the documented hosted MCP command replaces the invalid one at `:99`<br>The `@supabase/ssr`/auth rewrite and removing Prisma stay in 1d | R14 |

**Why each leftover matters (items 13–14):** they fail quietly, not loudly. Per `skills.md`, a personal skill beats a project skill of the same name, so a stale global copy could keep running the old tutor with no error, and an old `settings.json` would be half-read. Testers would then report bugs that aren't in the new code.

*Verified facts:*
- **`timingSafeEqual`:** Node docs (raw `nodejs/node` `doc/api/crypto.md`) say "An error is thrown if `a` and `b` have different byte lengths." So `security.md:133` returns a 500, not a 401, when a key has the wrong length.
- **Item 11:** code.claude.com `skills.md` (raw) says a command file "supports the same frontmatter except `name` and `paths`". `learn.md` routes with `Read .claude/commands/learn/X.md` (lines 44–95), so routing is unaffected. There are 15 sub-modules (`ls .claude/commands/learn/`).
- **Item 16:** the supabase.com api-keys page (rendered, fetched 2026-09-26) says "deprecating the anon and service_role keys by the end of 2026. Use the publishable (`sb_publishable_…`) and secret (`sb_secret_…`) keys". Its `.env` example uses `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` and `SUPABASE_SECRET_KEY`. The Supabase MCP page gives `claude mcp add --scope project --transport http supabase "https://mcp.supabase.com/mcp?…"`.

*Not added:* piecemeal 1.2 fixes (brew `--cask`, Node 22). Slice 1a rewrites 1.2 soon, so fixing it now would be done twice.

### D3 — Module 02 provider strategy
**D3a: option A, provider-agnostic.**
- Rename to "LLM APIs & Integrations", including the folder: `02-claude-api/` → `02-llm-apis/` in slice 1c. With fresh installs only, the rename costs nothing. Labs use Gemini's free tier.
- Claude stays at the centre of the course through Module 01 (Claude Code).
- The optional Claude track is **small**: one Claude/OpenAI/Gemini syntax table per concept and at most one optional, ungraded Claude box (natural spot: 2.4, `messages.parse`). No parallel labs.
- Add a "practice data only" warning in 2.2's key setup and in capstone A.
- Scripts and exercises are aligned (the review's `CLAUDE_API_KEY` mismatch).

*Why:* option B means ongoing cost and handing API keys to beginners. Option C doubles the maintenance.

**D3b: move all Gemini labs to the Interactions API**, not just 2.4.
- Pin the `google-genai` version in one `requirements.txt` per module, and record the call shape in `landscape.md` (D7).
- **State framing (R13):** 2.2 teaches "the model is stateless; this API stores interactions by default". Labs set `store=False` unless they are demonstrating state (`previous_interaction_id`).
- **A weekly free-tier smoke test** (one call, one repo secret) goes in 1c. SDK pins don't pin the server-side schema, and the May 2026 breaking change was server-side.

*Verified facts:*
- **Interactions API status:** the rendered page ai.google.dev/gemini-api/docs/interactions (last updated 2026-09-23) says "As of June 2026, it is Generally Available and recommended for all new projects… `generateContent`… now considered legacy… remains fully supported."
  - Features it lacks: automatic function calling (Python), Batch, explicit caching, custom safety settings.
  - **Method caveat:** the page's `.md.txt` export is stale and still says "beta… for production, continue to use generateContent" (D7b).
  - Per the reviewer, the same page says "By default, the API stores all Interaction objects (store=true)", retained for 1 day on the free tier.
- **The panel's reason to stay on `generateContent` doesn't apply.** Automatic function calling is used nowhere in `courses/ai-dev/`, and the 2.2 tool lab (`2.2_exercises.md:197-218`) is already a manual loop, which carries over to Claude `tool_use` and OpenAI function calls.
- **"Only Gemini gives a free API key" is false as a blanket claim.**
  - Cloudflare Workers AI offers "10,000 Neurons per day at no charge".
  - Anthropic's rate-limits page documents no free allocation.
  - Allowed wording: "Gemini offers a free API tier".
- **Gemini free-tier data use:** ai.google.dev/gemini-api/docs/pricing (last updated 2026-09-24) still says "Content used to improve our products".

### D4 — Curriculum shape
**D4a: reorder Module 0 and swap the numbers.**
- New order:
  - 0.1 intro to AI (the current 0.2, re-authored)
  - 0.2 mental model (the current 0.1)
  - 0.3 a short tools-landscape lesson that reads `landscape.md` and replaces the three repeated surveys
  - 0.4 prompt and context engineering, in Hebrew

**D4b: new setup lessons follow one rule, "X.0 = the tooling setup for this module", placed just before it's first needed.**
- **1.0 "Terminal & files"**, not 0.0. Module 0 is conceptual and needs no terminal.
  - **Shell on Windows: Git Bash.** Git is required anyway (D9a), so one set of bash commands works on every OS. PowerShell notes appear only where unavoidable.
    - *UNVERIFIED:* which shell the Desktop terminal pane opens on Windows. The 1a spec checks it in the Windows run-through. Fallback: 1.0 teaches opening Git Bash explicitly.
  - **1.0 installs Node.js at the version pinned in `landscape.md` (24, D7d).** `create-next-app` in 1.4 needs it. The tutor doesn't, so it isn't an onboarding prerequisite.
- **2.0 "Python setup & basics"**, built from the first half of 2.5. It also explains the switch from TypeScript to Python. Python *installation* happens during onboarding (D8b, D9a), so 2.0 covers venv and basics.

**D4c: core vs optional, with one convention for the whole course.**
- **Convention:** a single marker or section for optional material, e.g. `## להרחבה (לא נבחן)` ("going further, not tested"). `quiz.md` skips it (changed in F) and CI lints it. It also carries the optional track (D6d).
- **1.2 core:**
  - install the CLI inside the Desktop terminal
  - first session
  - **the permission cycle, taught in the CLI part.** Per the reviewer (permission-modes.md), auto is the default for interactive CLI sessions. In Desktop the mode selector is remembered per folder and Shift+Tab doesn't apply, so the Desktop part explains the selector.
  - plan mode, `/rewind`, `/init`, `/usage`
  - Optional cards: voice (honestly marked as not supporting Hebrew), pricing, "levels".
- **1.3 core:** CLAUDE.md, auto memory via `/memory`, one SKILL.md, and one PreToolUse hook with a negative test.
  - **The hook lab has a non-destructive target.** Blocking deletion through a hook can go wrong in many ways (`/bin/rm`, `bash -c`, `python -c`, the PowerShell tool), and a failed guard in a delete lab destroys files. The 1a spec picks the target.
  - Optional card: **the repo itself as the worked example** (§2.3 C). By 1a, unit M has created Tov-learn's own `SKILL.md` for learners to inspect.
- **1.1:** the premature homework (`1.1_exercises.md:59-66`, which needs Claude Code, Python and FastAPI) is removed in 1a (§2.8).
- **Moved out of 1.3, each to where it's first used:**
  - `claude mcp add` → 1.6, using Supabase's hosted read-only MCP
  - the custom read-only subagent → 1.7, which already covers subagents and gets `reviewer.md` from §2.21
- Rules, imports, headless, plugins, agent teams, workflows and routines become optional cards.

**D4d: one app carried from 1.4 to 1.8, Next.js from 1.4 onward, no Prisma.**
- The app: a small lead/booking app for the fictional business already in 1.4's open exercise (the Sharon dog trainer, `1.4_exercises.md:48`).
  - 1.4: landing page, built with `create-next-app`; its generated AGENTS.md/CLAUDE.md ties back to 1.3.
  - 1.5: booking form plus an admin list, with no database yet.
  - 1.6: Supabase (DB, auth, RLS, publishable/secret keys, `@supabase/ssr`, hosted read-only MCP).
  - 1.7: review, security and the subagent.
  - 1.8: Vercel deploy plus the GitHub Actions CI lab (D6b), which installs the `gh` CLI.
- The deploy step comes out of 1.4. The 1.8 Workers AI exercise becomes an optional card.
- *Why:* plain HTML in 1.4 followed by a port to Next.js in 1.5 would recreate the cliff (§2.8).

### D5 — Capstones: three tracks; old B kept but unwired

**Until 1e, no capstones are offered.** `/learn project` shows "the final projects are being rebuilt" (D2 item 12). A, C and D stay in `projects.md` untouched, as raw material for 1e. With the gate (D10), no real learner reaches the capstones before 1e.

**After 1e, the tracks are lettered A, B and C:**

| Track | Capstone | From | Key changes |
|---|---|---|---|
| **A — Web product** | AI support assistant inside the learner's 1.4–1.8 app, on Vercel | old A | Web chat, with WhatsApp as an optional stretch. 20 Q&As in context, RAG as an optional stretch. "Practice data only" warning |
| **B — Automation** | Daily intelligence agent on GitHub Actions `schedule:`, delivered to Telegram | old C | `workflow_dispatch` for manual testing (replaces the fake `wrangler trigger cron`). Scheduled at an odd minute. The 60-day auto-disable is explained. No Python Workers. **Schema-constrained extraction is required**, scored by a golden set built with 2.4's method |
| **C — Agentic (advanced)** | PR-review bot on GitHub Actions | old D | `pull_request` only (never `pull_request_target`). Explicit `permissions:`. The job skips fork PRs. No push/merge tools. The diff is treated as data. Third-party actions are pinned by SHA (D7d). Requires 2.7 |

**Old B (Document Intelligence) → `old_B`**, kept in the repo but unwired. It is moved out of `projects.md` into its own file (e.g. `03-final-project/old_B-document-intelligence.md`), and CI lints skip it. **`old_B` is not the new track B.**

**Applies to all three tracks:**
- A map from each phase to the lessons it depends on.
- A leveled rubric that **requires** passing tests/CI, an eval score (§2.16) and the red-team step.
- **Red-team grading is based on containment, not resistance (R7).** The learner plants an injection, runs it, and **shows the damage is bounded even if the model obeys**. Whether the model obeyed is recorded but not graded (D6a: there is no complete defense).
  - A: output rendered as text, not HTML; key on the server; no tools that change data.
  - B: the extracted JSON is schema-validated before use; the agent can only send its Telegram message.
  - C: minimal `permissions:`, no push/merge tools, fork PRs skipped, output is a comment only.
- **Checkpoints the tutor verifies** instead of "mark as Done": the tutor runs checks in the learner's session. Examples:
  - `gh run list` is green (`gh` is installed in 1.8)
  - the deployed URL answers
  - tests pass
  - the workflow YAML has no `pull_request_target`
  - a key scan covers **git history** (`git log -p`), not just the working tree

*Verified facts (docs.github.com, fetched as markdown through the docs API):*
- **Fork PRs:** "With the exception of `GITHUB_TOKEN`, secrets are not passed to the runner when a workflow is triggered from a forked repository. The `GITHUB_TOKEN` has read-only permissions in pull requests from forked repositories."
- **`pull_request_target`:** the secure-use guide says to avoid it with untrusted PRs.
- **`schedule`:** "can be delayed during periods of high loads… start of every hour"; the shortest interval is 5 minutes; it runs on the default branch only; on public repos it is "automatically disabled when no repository activity has occurred in 60 days".
- **Actions minutes (reviewer):** free on public repos; 2,000 minutes a month for private repos on GitHub Free. A daily job fits either way.

### D6 — New content scope
**D6a: new lesson 2.7 "Securing LLM apps"**, after 2.6 and before the capstones.
- **Core idea:** prompt injection has no complete defense, so design the app so a successful injection can't do much harm.
- **Topics:**
  - direct and indirect injection
  - least-privilege tools (OWASP LLM06)
  - model output treated as untrusted
  - keys on the server, including the `NEXT_PUBLIC_` trap
  - cost and rate limits
- **Hands-on:** attack a tiny bot of your own, then show the damage is contained. This is the same containment framing the capstones grade (D5).
- The "LLM" phase for `/learn security` goes to the **backlog**, triggered after 1c.

**D6b: verify loop in 1.4–1.7 and a CI lab in 1.8.**
- **The loop:** commit → ask Claude for a failing test → implement → run → skim the diff (which files changed; was anything touched that you didn't ask for?) → `/rewind` if it breaks.
- **This explicitly changes 1.1's thesis** from "you don't read every line, you check that it works" to "vibe coding is for throwaway projects (Willison, 2025-03-19); anything you keep gets tests and a diff check."
- **The 1.8 lab:**
  - GitHub Actions runs the app's tests on push/PR, plus a small `schedule:` demo. It's the prerequisite for tracks B and C.
  - Workflows that learners write use **version tags**, with an optional card on SHA pinning (D7d).

**D6c: a core golden-set eval in 2.4.**
- 10–20 labeled inputs, schema-validity rate plus exact match on key fields, run as a script that prints a score.
- That score is the capstone's "eval score". LLM-as-judge is optional.
- 2.4 is renamed "JSON & Structured Outputs" and uses the Interactions API's `response_format` + Pydantic (§2.10 B, D3b).

**D6d: the optional advanced track.**
- **Written in Stage 1, as optional cards (D4c):** only material that's already there and being moved, i.e. the 1.2/1.3 overflow and the 1.8 Workers AI exercise.
- **Stays core:** the 429 retry/backoff snippet in 2.2/2.5.
- **Backlog:** new advanced lessons (see Non-goals).

### D7 — Perishable facts
**D7a: `courses/ai-dev/landscape.md`.**
- **Format:** fixed-column markdown tables (`fact | value | source URL | verified_on`), readable by people and parseable by the lint with the Python stdlib.
- **What goes in:**
  - model IDs by tier
  - context windows and prices
  - free-tier terms, including data use
  - plan costs (Pro $20/mo, $0 API)
  - pinned SDK versions and the Interactions call shape
  - the pinned Node.js version (D7d)
  - dated vendor changes (Supabase keys)
  - Israeli VAT (18%)
- **How it's used:**
  - Scripts refer to tiers ("frontier / balanced / fast-cheap"), not model names.
  - **The tutor reads the file at lesson time and says "as of <verified_on>".** The change to `teaching.md` that does this is in F.
  - `quiz.md` never tests anything in it.
  - Exercise code may contain literal model IDs only if they're listed in the file.
- Having the tutor fetch providers' live pages at lesson time is rejected: it isn't deterministic.

**D7b: citation policy, in a contributor skill (R11).**
- **It lives at `.claude/skills/content-authoring/SKILL.md`.** Its description covers only *editing or authoring* course content, so it loads while Claude drafts lessons.
- **Why not a path-scoped `.claude/rules/` file:** per the reviewer (memory.md), path-scoped rules trigger whenever Claude *reads* matching files, and the tutor reads `courses/**` in every learner session. As a skill, it costs learners one description line.
- CONTRIBUTING links to it. CI enforces the mechanical parts (D7c).
- **It contains:**
  - **Sourcing:** every number or statistic gets a source URL and a date; no income promises; no uncited "research".
  - **Verification method:**
    - code.claude.com and platform.claude.com: use the raw `.md` and grep it, because summaries drop table cells.
    - ai.google.dev: `.md.txt` exports can be stale, so the rendered page with the later "Last updated" date wins.
    - **Anything with a removal or deprecation date: check the vendor changelog**, because reference pages lag. For example, docs.github.com's metadata-syntax page still listed `node20` after GitHub retired it.
    - General rule: when two versions of the same page disagree, the one with the later update date wins.
  - The D11 authoring requirement (objectives, keys, rubrics).
  - **The Hebrew style guide (D9b).**

**D7c: CI lints fail on structure, only warn on age, and use a shrinking baseline for existing offenders (R3).** *(Amended: §8 A10.)*
- **Baseline:** F generates, once, a baseline file listing every existing (file, string) pair of **model strings and denylisted wrong facts**. The lint:
  - **fails** on any model string that isn't in `landscape.md` or the baseline, and on any denylist hit that isn't in the baseline, **in any file** (outside `_archive/` and `old_B`)
  - prints baseline hits as warnings
  - fails if a baseline entry no longer matches anything, so the baseline can't quietly go stale
- Each slice deletes its baseline entries as it fixes them. **The baseline must be empty at the first-cohort gate (D10).**
- **Also fails:** a malformed `landscape.md` row, or a missing source or date.
- **Warn only:** a `verified_on` older than about 90 days, so time passing alone never turns CI red.
- **Where each lint lands:**

| Lint | Unit |
|---|---|
| COURSE.md ↔ folders; slide-marker count; header numbers; course-name denylist | Stage 0 |
| Route + every `Read .claude/…` path resolves; no `powershell` in `settings.json`; relative links resolve | Stage 0 |
| CLAUDE.md module table ↔ files | M |
| Model strings and the full denylist (baseline); `node-version` ↔ `landscape.md` | F |
| No hard-coded `python3` in `.claude/` or GETTING-STARTED | G |
| Settings template ↔ schema | S2a |

- **Later, optional:** a weekly `schedule:` workflow that opens an issue listing stale rows.

**D7d: toolchain pins.**
- **The Node version actions run on (the source of the Actions log noise).**
  - GitHub **retired Node 20 on runners on 2026-09-23**, and JavaScript actions now run on Node 24 (GitHub changelog, "Node 20 is no longer available in GitHub Actions").
  - Every workflow uses action majors whose `action.yml` declares `node24`. The repo's own `validate.yml` is fixed in Stage 0 (item 15); the reviewer cites checkout v7.0.1 and setup-python v7.0.0, and the spec confirms.
  - **SHA pins** (full commit SHA plus a version comment, per the secure-use guide) are used in the repo's own CI and for third-party actions in track C. Workflows that learners write use version tags (R18).
  - *Optional:* Dependabot for the `github-actions` ecosystem.
- **The Node version for the learner's app and tests: 24 now, 26 once Vercel supports it.**
  - Vercel's Node versions page (the `.md` and the rendered page agree) lists **24.x (default), 22.x and 20.x**. Pinning 26 would split local/CI from the deploy target.
  - Node 24 is supported until 2028-04-30 (nodejs/Release `schedule.json`).
  - The version lives in one `landscape.md` row. The trigger to move to 26 is "Vercel lists 26.x". The F lint fails if any `node-version:` under `courses/ai-dev/` or `.github/` disagrees with the row.

### D8 — Platform
**D8a: dead code.** The Stop hook is deleted in Stage 0. Unit M doesn't carry over `auto-save-progress.ps1` or the roughly 530-line slide viewer (§2.21 A). `display.md` is folded into `teaching.md` as part of the mandatory header (§2.20, D8f).

**D8b: one stdlib Python CLI; Python 3 is an onboarding prerequisite; one resolved interpreter.**
- `tovlearn.py` lives in `.claude/skills/learn/scripts/`, with commands `save | due | status | export | import | course-path`:
  - `import` reads only this CLI's own exports. It makes an automatic backup before importing and merges by newest file. `export` writes outside the repo (ta-11).
  - No `migrate` command: fresh installs only (Assumptions).
  - `course-path` is the **only** place that knows where course content lives (repo now, `${CLAUDE_PLUGIN_ROOT}` later).
- **Interpreter resolution (R8), in G:**
  - `/learn setup` finds a working interpreter: `py -3` on Windows, `python3` elsewhere, and `python` only if it reports version 3.
  - Nothing hard-codes `python3`, and the G lint enforces that.
  - *Why:* per the reviewer (docs.python.org `using/windows`), the Windows install manager provides `python`, `py` and `pymanager` and discourages `python3`. A missing Python opens the Microsoft Store through the built-in alias.
- **Per-machine files:**
  - **`local.json`** (in `~/skill-tutor-tutorials/`, not exported) stores the interpreter. It is re-detected on every setup run and never trusted when stale. During the tester period the clean-slate step clears it along with the rest of the folder.
  - **`.claude/settings.local.json` is never deleted.** Every `/learn setup` run **rewrites only the entries it owns**, marked so they can be found reliably:
    - the resolved interpreter
    - the generated hooks (the shared `settings.json` can't hold a command that differs per OS)
    - if needed, the absolute data path (D8d)
  - Everything else in the file is left alone. Per code.claude.com `settings.md`, Claude Code itself writes the learner's standing permission approvals ("Yes, and don't ask again") there. The file is gitignored (`.gitignore:2`).
  - This rewrite runs permanently, not only until the gate.
- *Why Python:* per code.claude.com `setup.md`, native Windows needs "None; Git for Windows is optional" and falls back to PowerShell, so nothing guarantees Python, Node or bash. The alternative (the model writes files when Python is missing) brings back two writers and the drift.

**D8c: schemas and spaced repetition (§2.17 B), in S2a.**
- `settings.schema.json`; a machine-local `local.json` that isn't exported; a progress schema with ISO dates.
- **The schemas and the CLI land together (R12)**, so `save` never writes an undefined format.
- One mastery constant (8), which the skip-quiz pass mark also uses. Continuous score buckets.
- Reviews quiz first. Intervals expand on a pass (e.g. 1→3→7→14→30→60 days) and drop back on a fail; the spec sets the exact numbers. Every lesson you finish gets a review date. SM-2/FSRS comes later.
- No lesson versions, retake mechanism or `schema_version` detection (Assumptions). If a future schema change needs a version field, a missing field can simply mean version 0.
- The stdlib has no JSON-Schema validator. So the schema documents the format, the CLI does minimal checks itself, and CI does full validation with `jsonschema`, installed only in CI. *(Amended: §8 A11.)*

**D8d: the move to `.claude/skills/learn/` is its own small unit, M, straight after Stage 0 (R2).**
- **Scope is move-only:**
  - `SKILL.md` plus `modules/`, `scripts/` and `schema/`
  - `${CLAUDE_SKILL_DIR}` references and frontmatter
  - no dead code carried over (D8a)
  - the CLAUDE.md module table rewritten, with its lint
- Modules become supporting files, not skills, so the 15 `/learn:*` entry points go away.
- **Done when:** the Stage 0 reference lint proves every path resolves. *(Amended: §8 A13; M must first extend the lint to `${CLAUDE_SKILL_DIR}`.)*
- **In S2a, not M:**
  - `permissions.additionalDirectories` for `~/skill-tutor-tutorials`. `skills.md` confirms it "grants file access only".
    - *UNVERIFIED:* whether it accepts `~` or Windows paths. The S2a spec checks. Fallback: setup writes the absolute path into its owned entries in `settings.local.json`.
  - the 3-OS pytest CI (§2.15 B)
- Left to the spec: whether the `learn` skill itself stays model-invocable.

**D8e: plugin in Stage 3, once the first cohort has used the post-gate course.**
- *Verified, from code.claude.com `plugins-reference.md` (raw):*
  - `${CLAUDE_PLUGIN_ROOT}` "changes when the plugin updates, so don't write state there".
  - `${CLAUDE_PLUGIN_DATA}` is `~/.claude/plugins/data/<id>/`, kept across updates but **deleted on uninstall** unless `--keep-data` is passed.
- **Rule:** learner data stays in `~/skill-tutor-tutorials/` and never goes in `${CLAUDE_PLUGIN_DATA}`.
- **The entry point changes:** plugin skills are namespaced as `/<plugin>:<skill>`, so `/learn` becomes `/<plugin>:learn` (skills.md). The S3 spec picks the plugin name and the migration message.

**D8f: per-slide checkpoint (§2.20 B), in S2b.**
- A Stop hook parses `last_assistant_message` for the mandatory `### 📚 N / total` header and calls `tovlearn.py save` through the resolved interpreter (D8b).
- A SessionEnd hook does a final save. Per the reviewer (hooks.md), SessionEnd hooks have a 1.5 s default timeout, so the spec sets a per-hook timeout.
- The header becomes mandatory in `teaching.md` (D8a).

**D8g: TTS (ta-06), in S2b.** An opt-in async hook written into the owned entries of `settings.local.json`, Windows only. Drop TTS if nobody uses it.

**D8h: learner and cohort id (ta-10), in S2c.** `learner.id` and `cohort` go in the settings schema, plus `tovlearn.py export --summary`. The full cohort dashboard stays P2.

**D8i: dashboard accessibility and Hebrew labels (ta-16), in S2c.** The `status` dashboard is rendered from `tovlearn.py status` data, with Hebrew labels, status shown by more than color, AA contrast, and ARIA on the score bars.

### D9 — Onboarding
**D9a: Hebrew `GETTING-STARTED.md` using the Desktop app (unit G).** Contents, in order:
1. Costs and accounts table: Pro $20/mo, $0 API, the Gemini free tier and its data-use note.
2. Install **Claude Desktop, Python 3 and Git**. Git is needed from 1.4 (verify-loop commits) and 1.8 (Actions); on Windows it also gives Claude Code its Bash tool.
   - **Windows specifics (R8):**
     - check with `py --version`
     - name the Microsoft Store trap and what to do about it
     - **restart Claude Desktop after installing Python or Git**. Per the reviewer, Desktop reads its environment from the system at launch. This is UNVERIFIED, so the run-through confirms it.
3. Get the course with one copy-paste `git clone`, with ZIP as the fallback.
   - During the rollout, testers `git pull` each slice. After the gate, learners pull only to receive fixes.
   - Learner data lives outside the repo, so pulling is safe.
4. Open the folder in the Desktop Code tab, then run `/learn setup`.
5. **OS support matrix** (§2.13 B) and **what the tutor saves on your computer, and where** (P2).
6. Troubleshooting (`claude doctor`, "Python not found").

- **Acceptance:** one real run-through in the Desktop app on Windows and on macOS before merge. **The Windows run starts from a machine with no Python and no Git**, e.g. a fresh VM or Windows Sandbox.
- *Verified (code.claude.com `desktop.md` and `setup.md`, raw):*
  - Desktop runs on macOS, Windows (x64/ARM64) and Linux (beta).
  - The Code tab's `/` menu includes "project skills from your codebase".
  - It has an integrated terminal pane.
  - Claude Code "requires a Pro, Max, Team, Enterprise, or Console account".

**D9b: Hebrew authoring.**
- Claude drafts the Hebrew. Every Hebrew content PR needs one approval from a current contributor (all are currently approved), enforced with branch protection requiring one review. No `CODEOWNERS` for now.
- A repo admin turns on "require 1 approving review" on `master` in G, before the first Hebrew content PR. The repo is public, so this works on the free plan (reviewer).
- A short Hebrew style guide lives in the D7b skill. The main point: rewritten lessons use real identifiers in code fences (`CLAUDE.md`, `/rewind`), not Hebrew transliteration. The text-to-speech version can be generated later (P2).

### D10 — Sequencing, the first-cohort gate, and the first spec
See §3 for the order. **The first spec covers Stage 0 only.** The second covers M, then F + G.

**First-cohort gate (R1).** No real cohort starts until **all** of these hold:
- Stage 0, M, F, G, 1a–1e and S2a have landed.
- The D7c baseline is empty.
- The Windows and macOS run-throughs (D9a) pass.

At the gate, the README tester note (D2 item 13), the clean-slate step (D2 item 14) and its temporary `clean_slate_no_delete` check (§8 A10) are removed. After the gate, the data format is stable, so a fresh install stays valid.

**One-unit-per-file rule (R2).** Each spec lists the tutor files (`.claude/skills/learn/**`) it touches. Only one open unit may touch a given module file at a time. This is a working rule, not a guarantee: for example, S2a rewires `progress.md`/`quiz.md` to the CLI while F changes `quiz.md` to skip optional cards.

**Docs rule:** each doc is updated in the same unit that changes it, not in a separate docs pass.
- **README:**
  - the global-install mention is removed in Stage 0
  - the tester note is added in Stage 0 and removed at the gate
  - its entry points to GETTING-STARTED in G
- **CLAUDE.md:**
  - test command → Stage 0
  - module table → M
  - anything else affected → the unit that changes it
- **CONTRIBUTING:** its wrong script format is **fixed**, and it links to the D7b skill, in F.
- **`changes.md`:** switches to Keep-a-Changelog in F. Entries for slices that renumber lessons (1a, 1b) tell testers to reset.

### D11 — Assessment alignment (§2.19)
- **In each Stage 1 slice, as an authoring requirement in the D7b skill:** every lesson a slice touches (not only fully rewritten ones, e.g. 2.1 and 2.3 in 1c) gets 3–5 observable objectives, quiz items mapped to them, and tutor-only answer keys and rubrics for every exercise. The inline answer keys in Module 0 are removed in 1b.
- **In F:** `teaching.md:174` ("present each exercise exactly as written") changes so exercises are presented without the tutor-only keys.
- **In S2d:**
  - `quiz.md` gets a 3-point free-text rubric, with the free-text item weighted at most 25%.
  - The settings schema gets `delivery: solo|cohort`, chosen in setup. In solo mode the tutor adapts pair and classroom exercises ("פנו למדריך" = "ask the instructor", "שתפו בקבוצה" = "share with the group").

---

## 3. Phased rollout

Order: **0 → M → F → N → G → 1a → 1d → 1b → 1c → 1e → gate → S3** (N added by §8 A12). After M, S2a–S2d run alongside Stage 1 under the one-unit-per-file rule.

| # | Unit | Depends on | Scope | Done when |
|---|---|---|---|---|
| 0 | **Stage 0**: quick-win PR | — | D2's 16 items | Each new lint fails on a seeded regression and passes on the fixed tree. `resume` offers 2.1 after 1.8. 0.4 splits into slides. No hook error after replies. `validate.yml` runs with no Node deprecation warning. The clean-slate step backs up before any delete |
| M | **Skills move** | 0 | D8d move-only; dead code not carried over (D8a); CLAUDE.md module table + lint | The reference lint passes; `/learn` works from `.claude/skills/learn/`; no `/learn:*` entries remain |
| F | **Foundation** | M | `landscape.md` (D7a) with the Node 24 row; the tutor reads it at lesson time; the content-authoring skill (D7b, D9b, D11); the optional-card convention and `quiz.md` skip (D4c); `teaching.md:174` key hiding (D11); baseline, model-string, denylist and `node-version` lints (D7c, D7d); CONTRIBUTING fixed; `changes.md` → Keep-a-Changelog | CI green with the baseline in place; a new unlisted model string or denylist hit anywhere fails; a mismatched `node-version` fails |
| G | **GETTING-STARTED** | F | D9a including the OS matrix, "what's saved where" and Windows specifics; interpreter resolution and owned `settings.local.json` entries in `/learn setup` (D8b); the no-`python3` lint; README entry; branch protection (D9b) | Real run-through on Windows (from no Python and no Git) and on macOS |
| 1a | Claude Code basics | F, G | 1.0 terminal (Git Bash; checks the Desktop shell) plus the Node 24 install (D4b); 1.2 core plus cards, permission cycle in the CLI part (D4c); 1.3 core with the non-destructive hook lab and the repo-as-example card; 1.1 homework removed; D11; baseline entries for 1.1–1.3 cleared | Every graded exercise runs as written on a fresh machine |
| 1d | One app, 1.4→1.8 | 1a | D4d; `@supabase/ssr`/auth rewrite and Prisma removal; verify loop and 1.1 thesis change (D6b); 1.7 facts plus `reviewer.md` (§2.21); 1.8 Vercel + Actions lab with `gh`, node24 actions, version tags and `node-version: 24` (D7d); D11; baseline cleared | The app builds, tests pass in CI with no Node deprecation warnings, and it deploys to Vercel |
| 1b | Module 0 | F | D4a; 0.4 in Hebrew; tier narration; temperature advice replaced (§2.9); Cowork description fixed (novice-07); inline answer keys removed; D11; baseline cleared | No baseline entries left in Module 0; 0.x numbers match the new order |
| 1c | Module 02 | F | Rename, including the folder (D3a); 2.0 (D4b); Interactions migration with the `store` framing and the weekly smoke test (D3b); 2.4 structured outputs + golden set (D6c); 2.6 fixes (ai-engineer-15); 2.7 (D6a); 429 snippet; data warning; D11; baseline cleared | Every lab runs on the free tier at the pinned SDK version; the smoke test is green |
| 1e | Capstones | 1c, 1d | D5 tracks A/B/C, containment grading, rubric, checkpoints, prerequisite map; `/learn project` offers them again | A dry run of each track passes its checkpoints on free tiers; the baseline is empty |
| S2a | **Schemas + CLI** | M | D8b CLI and D8c schemas together; `additionalDirectories` (D8d); 3-OS pytest CI with SHA-pinned node24 actions; template ↔ schema lint | CI green on Ubuntu, Windows and macOS; export → import round-trips on a fresh install |
| S2b | Hooks | S2a | D8f checkpoint (with timeouts) and D8g TTS, both through the owned `settings.local.json` entries | Closing the terminal mid-lesson resumes at the last slide; TTS stays off unless opted in |
| S2c | Ids + dashboard | S2a | D8h learner/cohort id plus `export --summary`; D8i dashboard | The summary export works; the dashboard has Hebrew labels, status beyond color, and AA contrast |
| S2d | Assessment | S2a | D11 quiz rubric and `delivery` | Free-text weight ≤ 25% with a rubric; solo mode rewrites pair/class exercises |
| — | **First-cohort gate** | 0, M, F, G, 1a–1e, S2a | D10 | Baseline empty; run-throughs pass; README note and clean-slate step removed |
| S3 | **Plugin** | gate + one cohort | D8e; `claude plugin validate`/`eval` behaviour tests (§2.15 C) | Installs without a clone; learner data survives uninstall |

S2b–S2d are not gate conditions. Every unit is its own spec → plan → implementation cycle.

---

## 4. Risks

| Risk | Mitigation |
|---|---|
| Volunteer capacity; Stage 1 is large | Slices ship on their own; the advanced track is backlogged; S2b–S2d are off the gate path |
| Stage 0 has grown to 16 items; M is now on the critical path | Items stay independent and small; M is move-only, and the reference lint proves it |
| Supabase key deprecation (end of 2026) | The key and MCP swap ship in Stage 0 (item 16) |
| Interactions API churn (the May 2026 change was server-side) | Pinned SDK; call shape and "verified on" date in `landscape.md`; weekly free-tier smoke test (D3b) |
| Windows Python pitfalls (`python3`, the Store alias, PATH after install) | Interpreter resolution (D8b); Windows steps in GETTING-STARTED; a run-through from a clean machine |
| Hebrew review becomes a bottleneck | Any current contributor may approve; Claude drafts; the style guide reduces review churn |
| A tester's leftover old install quietly shadows or confuses the redesign | README tester note and the clean-slate step (D2 items 13–14), both removed at the gate |
| A tester's data from earlier in the redesign goes stale when a slice renumbers lessons (1a, 1b) | Accepted. The `changes.md` entry tells testers to reset, and the clean-slate step makes resetting easy |
| Content and platform units edit the same tutor files | M goes first; the one-unit-per-file rule (D10) |
| Doc pages mislead verification | The verification method, including the vendor-changelog rule, is in the D7b skill |

---

## 5. Change log

**Gaps G1–G10** (found after the first draft, agreed 2026-09-26):

| # | Gap | Resolved in |
|---|---|---|
| G1 | §2.19 assessment alignment | D11 |
| G2 | §2.20 B per-slide checkpoint | D8f |
| G3 | TTS (ta-06) | D8g |
| G4 | Learner and cohort id plus `export --summary` (ta-10) | D8h |
| G5 | Dashboard accessibility and Hebrew labels (ta-16) | D8i |
| G6 | Docs drift | D10 docs rule |
| G7 | Lesson `version` before S2 exists | Dropped: fresh installs only |
| G8 | Which shell 1.0 teaches on Windows | D4b |
| G9 | Stage 0 item 10 safety | D2 item 10 |
| G10 | Branch protection for D9b | D9b |

**Fresh-install-only (agreed 2026-09-26):** dropped `migrate`, lesson versions and detection, G7, the Module 0 retake rule and the old-B fallback. Added the Assumptions section and the README tester note.

**Independent review (2026-09-26):** a fresh Opus 5.5 agent, read-only, with no brainstorming context, raised 19 findings: R1–R10 major, R11–R19 minor, no blockers. All were resolved with the user:

| # | Finding | Resolution |
|---|---|---|
| R1 | "Fresh installs only" conflicted with learners pulling during the rollout | First-cohort gate (D10); clean-slate step (D2 item 14); per-machine file rules (D8b) |
| R2 | Content and platform units touch the same files; two tutor changes had no unit | Unit M first (D8d); one-unit-per-file rule (D10); orphans assigned to F (D7a, D11) |
| R3 | The model-string lint would turn CI red in F | Shrinking baseline, extended to the denylist, empty at the gate (D7c) |
| R4 | Vercel can't run Node 26 | Pin 24; move to 26 once Vercel lists it (D7d) |
| R5 | Node 20 was retired on runners; `validate.yml` was on `node20` actions | Stage 0 item 15; vendor-changelog rule (D7b) |
| R6 | The stop-gap targeted the wrong line and left a destructive test | D2 item 10: no destructive test; spec decides |
| R7 | The red-team criterion graded model resistance | Containment grading in all tracks (D5, D6a) |
| R8 | `python3` is wrong on Windows | Interpreter resolution (D8b); Windows onboarding steps (D9a) |
| R9 | Lints from review §2.15 A were dropped | Lint-to-unit table (D7c); success criterion 3 reworded |
| R10 | Stage 0 unwired B but kept broken C and D offered | No capstones offered until 1e (D2 item 12, D5); tracks relettered A/B/C |
| R11 | A path-scoped rule would load into learner sessions | Contributor skill (D7b) |
| R12 | S2 was monolithic, with the CLI before its schemas | S2a–S2d (§3); schemas + CLI together (D8c) |
| R13 | "Stateless" framing; `store=true` by default | `store=False` framing and the smoke test (D3b) |
| R14 | The Supabase fallback trigger was late | Key + MCP swap in Stage 0 (D2 item 16) |
| R15 | The denylist would flag the "AI Engineer" job title | Course-name patterns only (D2 items 5, 9) |
| R16 | Dropped or unowned review items | 1.1 homework and the repo-as-example card → 1a; OS matrix and "what's saved" → G; CONTRIBUTING fixed in F; `/learn security` LLM phase → backlog |
| R17 | Checkpoint details | `gh` in 1.8; key scan covers history; track B golden-set wording (D5) |
| R18 | SHA pins are opaque for learners | SHA pins in repo CI and track C; tags for learner workflows (D7d, D6b) |
| R19 | Factual slips | 15 sub-modules; `README.md:46`; 1.2 permission cycle in the CLI part; plugin entry point; two UNVERIFIED items moved to specs |

---

## 6. Deferred to specs

These choices are deliberately left to the spec for the unit named. Each needs a docs check first (D7b).

| Choice | Decided in | Refs |
|---|---|---|
| The safe replacement for the current 1.3 hook exercise | Stage 0 spec | D2 item 10 |
| How the clean-slate step finds, shows, backs up and confirms | Stage 0 spec | D2 item 14 |
| The exact node24 action versions for `validate.yml` | Stage 0 spec | D2 item 15, D7d |
| How owned entries in `settings.local.json` are marked and rewritten | G spec | D8b |
| The non-destructive target for the new 1.3 hook lab | 1a spec | D4c |
| How learners install Node 24 (official installer or a version manager) | 1a spec | D4b, D7d |
| Which shell the Desktop terminal opens on Windows (UNVERIFIED) | 1a spec | D4b |
| Python tooling for 2.0 (`venv` + python.org, or `uv`) | 1c spec | D4b |
| Next.js version, router and test tooling on Node 24 | 1d spec | D4d, D6b, D7d |
| Whether `additionalDirectories` accepts `~`/Windows paths (UNVERIFIED) | S2a spec | D8d |
| Spaced-repetition interval numbers and the drop-back rule | S2a spec | D8c |
| Whether the `learn` skill stays model-invocable | S2a spec | D8d |
| Hook timeouts for SessionEnd/Stop | S2b spec | D8f |
| Whether to adopt Dependabot for `github-actions` | any CI-touching spec | D7d |
| Plugin name and the `/learn` → `/<plugin>:learn` message | S3 spec | D8e |

**Not assigned:** no unit has a named owner. That may be fine for a volunteer team; each spec can name one.

## 7. Verified facts

Checked 2026-09-24 to 2026-09-26. "(reviewer)" marks facts verified by the independent reviewer and not re-checked in brainstorming.

| Claim | Result | Source |
|---|---|---|
| `timingSafeEqual` throws on unequal lengths | Confirmed | nodejs/node `doc/api/crypto.md` (raw) |
| Command files accept skill frontmatter (`disable-model-invocation`) | Confirmed | code.claude.com/docs/en/skills.md |
| Interactions API is GA and recommended; `generateContent` legacy | Confirmed (rendered page, updated 2026-09-23); `.md.txt` export is stale | ai.google.dev/gemini-api/docs/interactions |
| Automatic function calling (Python) is missing from Interactions | Confirmed; unused in the course | same |
| Interactions stores by default (`store=true`), kept 1 day on the free tier | Confirmed (reviewer) | same |
| "Only Gemini gives a free API key" | **False** as a blanket claim | developers.cloudflare.com/workers-ai/platform/pricing; platform.claude.com/docs/en/api/rate-limits |
| Gemini free tier uses content to improve products | Confirmed (updated 2026-09-24) | ai.google.dev/gemini-api/docs/pricing |
| Fork PRs get no secrets; `GITHUB_TOKEN` is read-only | Confirmed | docs.github.com …/events-that-trigger-workflows |
| `schedule` delays, 5-minute minimum, 60-day disable | Confirmed | same |
| Actions free on public repos; 2,000 min/month private on GitHub Free | Confirmed (reviewer) | docs.github.com billing |
| Node 20 retired on Actions runners on 2026-09-23; JS actions run on Node 24 | Confirmed | github.blog/changelog/2026-09-23-node-20-is-no-longer-available-in-github-actions |
| `checkout@v4` declares `node20` | Confirmed | actions/checkout `v4` `action.yml` |
| Vercel supports Node 24.x (default), 22.x, 20.x only | Confirmed | vercel.com/docs/functions/runtimes/node-js/node-js-versions |
| Node 24 supported until 2028-04-30; Node 26 becomes LTS on 2026-10-28 | Confirmed | nodejs/Release `schedule.json`; nodejs.org/dist/index.json |
| Supabase deprecates anon/service_role keys by end of 2026; publishable/secret env names; hosted MCP command | Confirmed (rendered, 2026-09-26) | supabase.com/docs/guides/api/api-keys; …/getting-started/mcp |
| Claude Code writes standing approvals to `.claude/settings.local.json` | Confirmed | code.claude.com/docs/en/settings.md |
| Path-scoped rules load when Claude reads matching files | Confirmed (reviewer) | code.claude.com/docs/en/memory.md |
| Native Windows guarantees no bash/Python/Node | Confirmed | code.claude.com/docs/en/setup.md |
| Windows Python provides `py`/`python`; `python3` discouraged; Store alias when missing | Confirmed (reviewer) | docs.python.org `using/windows` (cpython main) |
| Hooks have no terminal; SessionEnd default timeout 1.5 s; Stop hooks get `last_assistant_message` | Confirmed (reviewer) | code.claude.com/docs/en/hooks.md |
| Auto is the default permission mode for interactive CLI sessions; Desktop remembers mode per folder | Confirmed (reviewer) | code.claude.com/docs/en/permission-modes.md; desktop.md |
| `${CLAUDE_PLUGIN_ROOT}` / `${CLAUDE_PLUGIN_DATA}` / `${CLAUDE_SKILL_DIR}` behaviour; plugin skills namespaced | Confirmed | code.claude.com/docs/en/plugins-reference.md, skills.md |
| Personal skill beats project skill of the same name; personal *command* vs project *skill* undocumented | Confirmed / undocumented | code.claude.com/docs/en/skills.md |
| Desktop platforms, project skills, integrated terminal | Confirmed | code.claude.com/docs/en/desktop.md |

**Still UNVERIFIED:**
- `additionalDirectories` with `~`/Windows paths (→ S2a spec).
- The Desktop terminal's shell on Windows (→ 1a spec).
- Desktop picking up PATH changes only after a restart (→ G run-through).
- From review §5: `google-genai` on Python Workers (moot); a plan-level context cap (not relied on); a native-Windows run of the Stop hook (moot, the hook is deleted).

---

## 8. Amendments from the Stage 0 spec (2026-09-29)

The Stage 0 spec (`docs/superpowers/specs/2026-09-27-stage0-quick-wins-design.md`, revision 6, locked 2026-09-29) went through five independent reviews. It changes the decisions below. Where this section and the text above disagree, **this section wins**. The spec holds the detail and the evidence.

| # | Amends | Change |
|---|---|---|
| A1 | D2 item 5 | Also: the leaked preambles at `2.3`/`2.6_exercises.md:1`; stale lesson and module cross-references (e.g. `2.1:5`, `2.6:77`, `0.2:137,165`, `0.2_exercises:146-149`, `0.3:57,87`, `0.3_exercises:59`, `1.1:165`); and every spoken lesson number that names a nonexistent lesson (full inventory in the spec, §4.2) |
| A2 | D2 item 8 | Also `README.md:202`, `CONTRIBUTING.md:61` and `CLAUDE.md:14,75`; the add-a-module docs gain the `disable-model-invocation` frontmatter step |
| A3 | D2 item 12 | `resume.md` also stops offering the final project until 1e |
| A4 | D2 item 7 | Aliases: `עצור`/`סיום` = stop, `בוחן`/`בוחן מלא` = quiz me (full), `המשך` = continue. "בחן אותי" stays **diagnostic** (it already was) |
| A5 | D2 item 14 | "Backs up and deletes" becomes a **move** into a timestamped backup folder, with no delete command. Exact paths only (`~/skill-tutor-tutorials/`, `~/.claude/commands/learn.md`, `~/.claude/commands/learn/`), no `learn*` glob. Global installs from before 2026-05-25 never reach the step, so the README tester note gives a manual fallback |
| A6 | D2 item 15, D7d | `setup-python` is replaced by `astral-sh/setup-uv` (SHA-pinned, `node24`). The contributor toolchain is **uv + pytest + ruff**, and uv is a hard requirement for contributors only, never for learners. Python is pinned to 3.14 in `pyproject.toml` only, with **no** root `.python-version`. Dependabot is adopted for `github-actions` (resolves the §6 Dependabot row) |
| A7 | D2 item 16 | Also `1.6_script.txt:33`. The hosted MCP stays **read-only** and project-scoped, and gains the documented `claude /mcp` → Authenticate step. `1.6_exercises.md:103` is rewritten so nothing is written through MCP |
| A8 | D2 item 10 | A Claude Code floor of **2.1.176**: the hook `if` path matching for `Read(...)` was fixed in 2.1.176 (CHANGELOG). It's stated in the 1.3 exercise and script and in the README, and `/learn setup` warns below it |
| A9 | D2 item 3 | The "3 files" hold **seven** VAT occurrences (including `vat_rate = 0.17` and a spelled-out "שבעה עשר אחוז"); all seven change to 18% |
| A10 | D7c | Stage 0 also adds `spoken_lesson_refs` (spoken lesson numbers must name existing lessons, with a stale-checked phrase allowlist), one more denylist entry (`NEXT_PUBLIC_SUPABASE_ANON_KEY`), and the **temporary** `clean_slate_no_delete` check, removed at the gate |
| A11 | D8c | `jsonschema`, if needed, is a dev-group dependency used only by tests, so contributors install it locally too, not "only in CI" |
| A12 | D1, D10, §3 | **New unit N (numbering contract)** between F and G/1a: stable lesson ids, a manifest, a deterministic generator for derived numbers with CI `--check`, id references in prose, a thin renumber skill, and a CLAUDE.md "run the generator before any push" rule. It replaces Stage 0's `header_numbers` and `spoken_lesson_refs`. It needs its own spec |
| A13 | D8d, §3 row M | M's done-when ("the reference lint passes") is vacuous until M extends `tutor_refs` to resolve `${CLAUDE_SKILL_DIR}` against the nearest `SKILL.md`, with seeded tests |
