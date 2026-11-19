# Stage 0 — Quick-Win PR: Design Spec

**Date:** 2026-09-27 · **Revision:** 6.1 (2026-09-29), after five independent reviews and the plan review (§10) · **Status:** **locked** by the user (2026-09-29); rev 6.1 is editorial only (no decision changed). Plan: `docs/superpowers/plans/2026-09-29-stage0-quick-wins.md`
**Parent:** `docs/prds/project-redesign-2026-09-25.md` (the PRD). References such as "D2 item 5", "§3" and "R14" point there. "Review §2.x" points to `docs/reviews/project-review-2026-09-24.md`. "RV-…" through "RV5-…" point to the spec reviews (§10).
**Baseline:** `master` at `290af75` (= `origin/master`, after #12 and #13 were merged on 2026-09-28). Its tree is identical to the earlier local `d04ca2a` (tree `5bf8edb`), so every line number below refers to that tree.
**Scope:** Stage 0 only:
- D2's 16 items
- the Stage 0 rows of the D7c lint table
- the three §6 rows assigned to the Stage 0 spec, plus the Dependabot row ("any CI-touching spec")
- §3's Stage 0 "done when"
- the gaps and review findings absorbed in §2 and §10

`courses/_archive/` is out of scope throughout.

---

## 1. Outcome and constraints

**Outcome:** one PR against `master` that:
- fixes what testers hit now: wrong course name, missing lessons, a broken hook, an unsafe lab, deprecated Supabase keys, stale lesson cross-references
- adds the first CI lints, each proven by a seeded regression
- moves the repo's CI to `node24` actions, on uv + pytest + ruff

**Constraints:**
- Fresh installs only, and testers only until the first-cohort gate (PRD Assumptions, D10).
- **Contributor tooling:**
  - **uv is a hard requirement for contributors.** The only supported entry point is `uv run ruff check -q && uv run pytest -q`. Ruff runs first, so it runs even while pytest is expected to be red. When pytest is red, re-run it with `uv run pytest -v` to see the failing cases (S20).
  - **This does not apply to learners.**
    - Learner-facing docs (README) never mention uv. CLAUDE.md, which also loads into learner sessions, labels its test section "contributors only".
    - The PRD D8b learner CLI must not inherit uv.
    - The repo root carries **no `.python-version`** file, so nothing pins a learner's `python` (RV2-M5). §9 records this for G, S2a and 1c.
- Edits are minimal and mechanical. Every rewrite stays with its Stage 1 slice.
- **One-unit-per-file rule (D10).** Stage 0 touches `learn.md` and all 15 `learn/*.md` sub-modules. All 15 get frontmatter. Five also get body edits: `setup.md`, `security.md`, `project.md`, `resume.md`, and a two-line edit to `progress.md` (RV5-L7). `learn.md` gets body edits too. Cited line numbers in `learn/*.md` shift by +3 once the frontmatter lands, so edits are anchored on headings and quoted text, not line numbers alone (RV5-L9). No other unit is open on these files.
- **Workspace:**
  - **Baseline guard (RV2-H1, RV3-M6).** Before creating the worktree, run `git fetch origin`, then confirm `git rev-parse master` equals `git rev-parse origin/master`. Then:
    - **If local `master` lags `origin/master` (expected once the docs PR has merged), fast-forward it first:** `git switch master && git merge --ff-only origin/master`. A fast-forward that fails means local `master` has diverged: stop and ask the user (RV5-M4).
    - If `origin/master` is still `290af750671abf35342fc2c4ee131f0e0db89130`, proceed.
    - Otherwise, proceed only if `git diff --stat 290af75 origin/master -- . ':!docs'` is empty.
    - Otherwise, **stop** and re-verify every cited line against the new tip before editing.
  - Then create a manual worktree: `git worktree add ../Tov-learn-stage0 -b fix/stage0-quick-wins master`.
  - Never use `EnterWorktree`. uv creates the worktree's own `.venv`.
  - Commit or push only when the user asks.
- **Known, deferred: the docs aren't on `master` yet (RV4-M2; user decision).** This spec, the PRD and the review live only on `docs/project-review-2026-09-24`. Once the spec is locked, that branch goes up as its own PR, and the user merges it manually **before** Stage 0 implementation starts. The Stage 0 worktree (cut from `master` after that merge) then contains the docs, and the baseline guard tolerates the docs-only change. **Spec reviewers: ignore this issue.**

---

## 2. Decisions made in this spec

| # | Decision | Reason |
|---|---|---|
| S1 | **Three PRD gaps are absorbed** (user-approved):<br>• **G1:** leaked preambles also at `2.3`/`2.6_exercises.md:1`<br>• **G2:** global install also at `README.md:202`, `CONTRIBUTING.md:61` and `CLAUDE.md:14,75`<br>• **G4:** `resume.md:23,38,50,74` still offers the final project | Same defect class; the D10 docs rule |
| S2 | **Hebrew aliases:**<br>• `עצור`/`סיום` = stop<br>• `בוחן`/`בוחן מלא` = quiz me / quiz me full<br>• `המשך` = continue<br>"בחן אותי" **stays diagnostic** | "בחן אותי" already means diagnostic (`learn.md:102`, `teaching.md:144`, `setup.md:225`) |
| S3 | **The 1.3 hook exercise guards a fake secret against *reading*.**<br>• PreToolUse, `matcher: "Read"`, `if: "Read(secret-demo.txt)"`, exit 2<br>• a live `cat` bypass shows how fragile hooks are | Nothing is written or deleted even if the guard fails. The focus is hooks in general and their fragility |
| S4 | **Clean-slate moves, never deletes** | "Backs up before any delete" holds by construction (§8) |
| S5 | **Clean-slate checks three exact paths, with no globs** | `learn*` would match unrelated personal commands |
| S6 | **Lints are `check_*` functions in `tests/validate_structure.py`, tested with pytest; ruff lints the Python; everything runs through uv** | Permanent seeded regressions; a pinned toolchain (user decision) |
| S7 | **The route/reference lint scans only the tutor files** (`.claude/**/*.md`) | Exercises cite `.claude/…` paths in the learner's lab project |
| S8 | **Manual done-when checks are run by the user interactively and recorded in the PR** | Headless `claude -p` can't exercise `AskUserQuestion` or show hook-error notices reliably |
| S9 | **`validate.yml` gets `permissions: contents: read`** | Least privilege |
| S10 | **A new unit N (numbering contract) is proposed between F and 1a** (§9) | Renumbering churn comes before any later stage |
| S11 | **`changes.md` gets one final `# Changes — fix/stage0-quick-wins branch` section**, in the current format, written once. The branch is named `fix/stage0-quick-wins` | The D10 docs rule. It follows the typed names of the most recent merged PRs (#11–#13, all `fix/…`). F converts everything to Keep-a-Changelog |
| S12 | **uv is a hard requirement for contributors only** (§1). The validator is a library module; `test_real_repo_passes` reports the findings | One supported entry point (user decision) |
| S13 | **Python is pinned to 3.14 in `pyproject.toml`** (`requires-python = ">=3.14,<3.15"`), and CI passes `python-version: "3.14"` to setup-uv. **There's no `.python-version` file** | User decision. 3.14 has active support until 2027-10-01 and security fixes until 2030-10-31. 3.15.0 ships 2026-10-01 (PEP 790) and is deliberately not adopted at day zero; moving to it is a later, separate change. A root `.python-version` could pin learners' `python` through pyenv (RV2-M5) |
| S14 | **Claude Code minimum is 2.1.176**, a floor, not an exact pin. It's stated in `1.3_exercises.md:8`, `1.3_script.txt:15` (reworded as a lesson-wide requirement, RV3-L5) and README Prerequisites (`:25`) and Requirements (`:208`). `/learn setup` warns below it, comparing (major, minor, patch) as numbers | 2.1.176 fixed `if` path matching for `Read(...)`, which S3 depends on (user decision) |
| S15 | **Dependabot is adopted now for `github-actions` only**, weekly. The `uv` ecosystem is deferred | Keeps the SHA pins fresh. Dependabot's documented uv version is v0.11 |
| S16 | **The Supabase MCP stays read-only.** `1.6_exercises.md:103` is rewritten, and the documented `/mcp` → Authenticate step is added (RV-H2, RV2-M3) | A read-only boundary for beginners. The exercise must not fail as written |
| S17 | **A new check, `spoken_lesson_refs`:** every spelled "W נקודה W" and hyphenated ordinal ("חמישי-שלוש") in course content must name an existing lesson, apart from an explicit phrase allowlist (RV2-M6). It handles one-letter prefixes (ו/ב/ל/ש/ה/מ/כ) and every table form (RV3-H1–H3) | Makes the residue pass complete over every form it parses, and keeps it that way until N replaces it |
| S18 | **Stage 0's `changes.md` commit also adds the missing sections for #12 and #13** (user decision) | They were merged during this work without `changes.md` entries. Folding them in avoids a direct push to `master` and another conflict-prone edit. Earlier PRs without sections (#1, #5–#11; only `sean_changes` #2 and `yuval_ver` #3 have sections) are left for F's Keep-a-Changelog conversion (RV3-L12, RV4-L7). The docs PR (review, PRD, spec, plan) is planning material, not a behaviour change, so it gets no section (RV5-L9) |
| S19 | **One more denylist entry: `NEXT_PUBLIC_SUPABASE_ANON_KEY`** (RV3-L11). The exit-code phrase was tried twice and **dropped** (RV4-M1, RV5-M1): the wrong claim ("מחזיר קוד יציאה אחד" as a *block*) and the correct explanation ("exit code one does *not* block") share the same words, so no regex separates them. The wrong claim is fixed by hand in item 10; F's full denylist may revisit it with a baseline | Stage 0 fixes the only occurrence (`1.6_exercises.md:21`), and review §2.15 A lists it. PRD D2 item 9 allows entries Stage 0 fully fixes |
| S20 | **Dev loop:** `uv run ruff check -q && uv run pytest -q` routinely; `uv run pytest -v` when red; `uv run pytest --collect-only -q` for the PR's list of test IDs (RV3-L1, RV3-L6) | Cheap routine runs. Ruff is never skipped by an expected red test. The PR still gets IDs |

---

## 3. Verified facts (2026-09-27/28)

Checked per D7b. "(reviewer)" marks facts verified by a spec review that are not re-checked here.

| Claim | Result | Source / method |
|---|---|---|
| `master` = `origin/master` = `290af75`; #12 and #13 merged 2026-09-28; tree identical to the earlier local `d04ca2a` | Confirmed | `git fetch`; `gh pr list`; `git diff master origin/master` empty; equal tree hashes |
| `actions/checkout` latest is **v7.0.1** = `3d3c42e5aac5ba805825da76410c181273ba90b1`, `using: node24` | Confirmed | GitHub API; `action.yml` at that SHA |
| `astral-sh/setup-uv` latest is **v10.2.0** = `c18668ad3cf93ea998bef934396af7bb5c839dc7`, `using: "node24"`, with `version`/`python-version`/`version-file` inputs | Confirmed | same method |
| `checkout@v4` / `setup-python@v5` declare `node20`; Node 20 retired on runners 2026-09-23 | Confirmed | `action.yml`; github.blog changelog |
| uv **0.12.19**; pytest **9.1.1** (Python ≥3.10); ruff **0.16.9**; `ruff check -q` prints diagnostics only | Confirmed | GitHub API; PyPI JSON; `ruff check --help` |
| Python 3.14.7 is the latest 3.14; active support until 2027-10-01, security until 2030-10-31. 3.15.0 final is scheduled for 2026-10-01 | Confirmed | endoflife.date/api/python/3.14.json; PEP 790 (raw, status Active) |
| Claude Code sets `CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT` for its tools, but no version variable, so `claude --version` reports whichever `claude` is on PATH, which may not be the running binary | Confirmed in this session's environment (limitation, RV3-L4). There is also an **undocumented** `CLAUDE_CODE_EXECPATH` (the running binary's path; not in env-vars.md or the CHANGELOG). Stage 0 keeps the documented `claude --version`; preferring `$CLAUDE_CODE_EXECPATH` when set is a possible later improvement (RV4-L5) | `env` |
| Dependabot supports `github-actions` and `uv` (the uv row lists v0.11); it updates the version comment beside a SHA pin | Confirmed / (reviewer) | docs.github.com (article-body API) |
| Only exit 2 blocks PreToolUse; exit 1 is non-blocking | Confirmed | hooks.md (raw) |
| Hook `if` added in **2.1.85**; `Read(.env)`-style path patterns match from **2.1.176** | Confirmed | anthropics/claude-code `CHANGELOG.md` (raw) |
| Shell-form hooks run with `sh -c` on macOS/Linux, Git Bash on Windows, PowerShell when Git Bash is missing; no controlling terminal; `permissionDecision: "ask"` exists | Confirmed | hooks.md (raw), "Shell form", `shell` field |
| A bare filename in `Read(…)` matches at any depth; Read deny rules cover `cat`/`head`/`tail` but not `grep -r` or scripts | Confirmed | permissions.md (raw) |
| A "Yes, and don't ask again" approval is saved to `.claude/settings.local.json`, resolved through worktrees to the main checkout **from v2.1.211**; before that, it was saved in the starting directory | (reviewer; RV5-L8) | permissions.md |
| Sandbox is OS-enforced; not native Windows | Confirmed | sandboxing.md (raw) |
| Same-name skills/commands: "personal over project" | Confirmed | skills.md (raw) |
| Routers before `c25e73c` (2026-05-25), e.g. `1bdbd50`, `acbf16c`, contain setup and the global install **inline**. From `c25e73c` on, the router `Read`s `.claude/commands/learn/setup.md` | Confirmed | `git show <sha>:.claude/commands/learn.md` |
| Supabase: anon/service_role keys deprecated by the end of 2026; `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` / `SUPABASE_SECRET_KEY` | Confirmed (rendered) | supabase.com/docs/guides/api/api-keys |
| Supabase hosted MCP: the `claude mcp add --scope project --transport http supabase "https://mcp.supabase.com/mcp?…"` command; the `read_only=true` / `project_ref=` parameters; then "In a regular terminal (not the IDE extension) run: `claude /mcp`. Select the "supabase" server, then "Authenticate"", a browser login with no PAT | Confirmed (rendered, 2026-09-28) | supabase.com/docs/guides/getting-started/mcp |
| `chattr +i` can be set or cleared only by the superuser | Confirmed | `man chattr` |
| `timingSafeEqual` throws on unequal lengths; command files accept `disable-model-invocation` | PRD §7 | nodejs `crypto.md`; skills.md |

**UNVERIFIED, deliberately not relied on:**
- macOS/Windows equivalents of `chmod 000` + `chattr +i` (→ 1a)
- Dependabot with uv 0.12 lockfiles (→ S15)
- the native-PowerShell hook variant (no Windows machine available)
- the 1.6 MCP flow end to end (needs a Supabase project)

The last two are listed as untested in the PR (§6).

---

## 4. Design

### 4.1 Work groups

| Group | Items | Files |
|---|---|---|
| **P: Platform/CI** | 2, 9, 15, S6/S12/S13/S15/S17 | `.github/workflows/validate.yml`, **new** `.github/dependabot.yml`, **new** `pyproject.toml`, **new** `uv.lock`, `.gitignore`, `tests/validate_structure.py`, **new** `tests/test_validate_structure.py`, `.claude/settings.json` |
| **C: Course content** | 1, 3, 4, 5 (+G1, RV-M1, RV2-M6), 10 (+RV-L2, S14), 16 (+S16, RV-M6) | `COURSE.md`; scripts/exercises in 0.2–0.4, 1.1–1.8, 2.1–2.6 |
| **B: old_B** | 12 (content part) | `projects.md` → **new** `03-final-project/old_B-document-intelligence.md` |
| **T: Tutor** | 6, 7, 11, 12 (+G4), 14, S14 setup check | `learn.md`; all 15 `learn/*.md` (frontmatter); body edits in `setup.md`, `security.md`, `project.md`, `resume.md`; two trigger lines in `progress.md` |
| **D: Docs** | 8 (+G2), 13, test command, S11, S14, S18, RV-L6, RV3-M7 | `setup.md` §F, `README.md`, `CLAUDE.md`, `CONTRIBUTING.md` (lines 13–35, 57–61 and 65–69 only), `changes.md` |

### 4.2 Course content (groups C and B)

#### Item 1: `COURSE.md`
- Add `| 2.1 | מהו API | מעשי |` and `| 2.2 | עבודה עם API של Claude, OpenAI ו-Gemini | מעשי |` before 2.3.
- Change the module 02 range `2.3–2.6` → `2.1–2.6`.

#### Item 3: VAT 17% → 18% (RV-M2, RV2-M1)
There are seven occurrences:
- `1.3_exercises.md:36`
- `2.2_exercises.md:150` (scenario "כולל מע"מ (17%)")
- `2.2_exercises.md:153` (task "המחיר כולל 17% מע"מ")
- `2.2_exercises.md:175` (docstring)
- `2.2_exercises.md:176` (`vat_rate = 0.17` → `0.18`)
- `2.2_exercises.md:184` (tool description)
- `2.6_script.txt:53` ("שבעה עשר אחוז" → "שמונה עשר אחוז")

**Completion check (for the plan):** `grep -rnE "17%|0\.17|שבעה עשר" courses/ai-dev` returns nothing outside `_archive/`.

#### Item 4: 0.4 markers
All 19 `[SLIDE TRANSITION]` → `[מעבר שקף]`. No other *marker* change. Item 5 separately fixes 0.4's title, its "Lesson 0.3" mentions and its course line (RV3-L3).

#### Item 5 + G1 + RV-M1 + RV2-M6: archive residue
- **The course name.**
  - Change the course-name uses to "AI Dev":
    - "…קורס AI Engineer" in `0.2_script.txt:3`, `0.3_script.txt:3`, `2.1_script.txt:2`
    - `- **קורס:** AI Engineer` in `0.2/0.3/0.4_exercises.md:7`
  - **Keep** the job-title uses: `0.2_script.txt:9,41,83,123-129,161`, `0.3_script.txt:111`, and the English "AI engineer" in 0.4.
- **Headers:**
  - exercise H1 and `**שיעור:**` lines in 0.2, 0.3, 0.4, 1.7, 1.8 and 2.1–2.6
  - script title lines in 0.2, 0.3 and 0.4, including "Lesson 0.3" in both places in the opening
- **Spoken lesson numbers.** The full inventory, built with the S17 parser: every digit-table form (including שישה/שבעה/ארבעה…) and one-letter prefixes (RV3-H1, H2). Each is rewritten to the real lesson:

  | File:line | Now | Becomes |
  |---|---|---|
  | `1.1:1`, `1.2:1`, `1.3:1`, `1.4:1` (self), `1.5:1`, `1.6:1`, `1.8:2` | "שלוש נקודה X" (self) | "אחת נקודה X" |
  | `1.4:1` (previous-lesson clause) | "שלוש נקודה שלוש" | "אחת נקודה שלוש" |
  | `1.1:167-173` | 3.2/3.3/3.4/3.6/3.8, and `1.1:171` "**ושלוש** נקודה חמש" (3.5) | 1.2/1.3/1.4/1.6/1.8, and "ואחת נקודה חמש" |
  | `1.2:245`, `1.3:41`, `1.4:39`, `1.6:77` | 3.3/3.4/3.5/3.7 | 1.3/1.4/1.5/1.7 |
  | `2.1:2`, `2.2:2` (self and previous), `2.4:2`, `2.5:2`, `2.6:1` (self and previous) | "חמש נקודה X" | "שתיים נקודה X" |
  | `2.1:100`, `2.2:57`, `2.4:7`, `2.4:72` | 5.2/5.3/5.3/5.5 | 2.2/2.3/2.3/2.5 |
  | `2.1:5` | "ארבע נקודה שש" (a lesson that never existed) | cut (see the cross-reference list below) |
  | `2.6:77` | "שש נקודה אחת" | cut (see below) |

  **Not lesson numbers, so they stay** (and form the S17 allowlist, §5.1):
  - `0.3:39` "ושבע נקודה אחת אחוז"
  - `1.1:83` "ארבע נקודה שש" (Opus 4.6)
  - `1.1:123` "שש נקודה שש מיליארד"
  - `1.5:7` "שישה נקודה שישה מיליארד" (RV3-H2)
  - `2.1:85,90,100` "שתיים נקודה אפס" (OAuth 2.0)
  - `2.5:12` "שלוש נקודה שלוש/ארבע עשרה" (Python 3.13/3.14)
  - `2.5:42` "ארבע נקודה שבע" (Opus 4.7)

  `1.3:3,11,15` ("שתיים נקודה אחת נקודה…", Claude Code versions) parse as 2.1, an existing lesson, so they need no allowlist entry. `1.3:15` changes to the S14 floor (item 10).
- **Other ordinal and module forms:**
  - `2.3:2` "חמישי-שלוש" → "שתיים נקודה שלוש"
  - `2.3:72` "בשיעור הבא, חמישי-ארבע" → "שתיים נקודה ארבע" (RV3-H1)
  - `1.7` "המודול השלישי"
  - `1.8` "מודול שלוש" (twice)
  - `1.1:165` "בהמשך מודול שלוש"
  - `0.3` "לשיעור השני"
- **Cross-references to lessons or modules that don't exist or have moved:**
  - `1.1_script.txt:5`: Make/n8n/WhatsApp/Telegram → a one-sentence bridge from Module 0.
  - `0.2_script.txt:3` and `:13-15`: the 8-module / 156-hour description → the four modules from `COURSE.md`.
  - `0.2_script.txt:137,165`: "בשיעור 0.3" (prompt engineering) → "בשיעור 0.4".
  - `0.2_exercises.md:146-149`: map to the real modules (01, 02, 03); cut rows with no counterpart.
  - `0.3_script.txt:57`: cut "נלמד את זה לעומק במודול הראשון".
  - `0.3_script.txt:87`: "במודול חמש" → "במודול שתיים", spelled out to match the file's spoken voice (RV3-L9).
  - `0.3_exercises.md:59`: cut "נלמד בדיוק את זה במודולים 1 ו-2".
  - `1.2_script.txt:229-235`: "3.3" → "1.3", "3.7" → "1.7".
  - `1.8_script.txt`, the last slide: → a one-line bridge to Module 02.
  - `2.1_script.txt:5`: → a bridge from Module 01.
  - `2.6_script.txt:77`: cut the "module 6 / lesson 6.1" teaser. The closing summary stays. There's no bridge to the final project, because Stage 0 disables it (RV2-L12).
- **Leaked preambles (G1).** In `1.8`, `2.3` and `2.6_exercises.md`, delete line 1 and the blank/`---` lines that follow it, up to `<div dir="rtl" lang="he">`.
- **Voice:** replacement Hebrew matches the file. It's reviewed by a Hebrew-speaking contributor.
- **Known churn:** 1b renumbers 0.x again. `0.1_script.txt:125` ("next lesson: a practical tour of Claude Code, Cursor, Copilot") doesn't describe today's 0.2. It's left for 1b's reorder, which is expected to make it true again (RV3-L10).

#### Item 10: the 1.3 hook exercise
**Exercise 5** (`1.3_exercises.md:75-85`) is rewritten:
1. **Setup.** In `claude-advanced-lab`, create `secret-demo.txt` (`FAKE_API_KEY=not-a-real-key`) and `notes.txt`.
2. **The hook,** in project scope, `claude-advanced-lab/.claude/settings.json`:
   ```json
   {
     "hooks": {
       "PreToolUse": [
         {
           "matcher": "Read",
           "hooks": [
             {
               "type": "command",
               "if": "Read(secret-demo.txt)",
               "command": "echo 'Blocked by hook: secret-demo.txt is protected' >&2; exit 2"
             }
           ]
         }
       ]
     }
   }
   ```
   The native-Windows (no Git Bash) variant uses `"command": "[Console]::Error.WriteLine('Blocked by hook: secret-demo.txt is protected'); exit 2"`.
3. **Negative test.** Restart Claude Code in the folder and ask **in words** (not with an `@secret-demo.txt` mention) to read `secret-demo.txt`. It is blocked, and Claude repeats the reason. *If Claude immediately tries the terminal on its own, that's step 5 happening early. Note it.*
4. **Positive control.** Reading `notes.txt` works.
5. **The bypass.** Ask explicitly: "run `cat secret-demo.txt` in the terminal" (`Get-Content` without Git Bash). The content appears.
   - *If Claude declines,* the refusal is model behaviour, not enforcement. Record what happened.
6. **Takeaway (text), RV2-L5:**
   - A hook is a deterministic guardrail for the specific tool calls it matches. Other tools (Bash, PowerShell, Grep) still reach the file, and so, probably, does an `@file` mention, which isn't a Read tool call (unverified, RV4-L6). So a hook is not a security boundary.
   - Claude Code has stronger layers:
     - permission **deny rules**, which also cover `cat`/`head`/`tail`, though not scripts that open files themselves
     - the **sandbox**, which is OS-enforced (macOS, Linux, WSL2)
   - The strongest enforcement is outside Claude entirely: OS permissions that the agent's user can't undo.
   - Linux illustration, in a box explicitly marked "**להמחשה בלבד — לא להריץ**" (illustration only, don't run): `chmod 000 secret-demo.txt && sudo chattr +i secret-demo.txt`.
   - "Out of reach" means out of reach of every process the agent can start.
7. **Y/N note:** hooks have no terminal. `permissionDecision: "ask"` is the mechanism (optional reading).

**Related edits:**
- `1.3_exercises.md:8`: "v2.1.59+" → "v2.1.176+".
- `1.3_script.txt:15`: the sentence becomes a **lesson-wide** requirement ("לשיעור הזה צריך קלוד קוד בגרסה שתיים נקודה אחת נקודה מאה שבעים ושש ומעלה"), not an auto-memory one. The facts at `:3` and `:11` about when auto memory arrived stay (S14, RV3-L5).
- `1.3_script.txt:25`: soften "חוסם פעולה באופן מוחלט" to "deterministic for the tool call it matches".
- `1.3_script.txt:27`: the exit-2 vs exit-1 correction.
- `1.3_script.txt:29`: the read-guard demo. No deletion, and no Python-bypass suggestion.
- `1.3_exercises.md:60`: skills trigger through their `description`, not "via Hooks (exercise 5)".
- `1.3_exercises.md:114`: "סקריפט ה-Hook" → "the `.claude/settings.json` with the hook".
- **Rubric "יישום Hooks":** blocks the Read, explains exit 2 vs 1, and explains the `cat` bypass.

Nothing deletes a file or asks the learner to try.

#### Item 16 + S16 + RV-M6: Supabase in 1.6
- `1.6_exercises.md:17,21,30,168`: switch to the publishable key (`NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=sb_publishable_...`). `:168` adds: "`SUPABASE_SECRET_KEY` is server-only: never `NEXT_PUBLIC_`, never in git".
- `:99`: `claude mcp add --scope project --transport http supabase "https://mcp.supabase.com/mcp?project_ref=<your-project-ref>&read_only=true"`, followed by a new step (RV2-M3): "in a regular terminal run `claude /mcp`, select **supabase** → **Authenticate**, and log in to Supabase in the browser that opens".
- `:103`: "Using the Supabase MCP, describe the schema of the 'clients' table", then "insert the dummy client row in Supabase's Table Editor". It adds one line explaining that the MCP is read-only on purpose. Questions and rubric are adjusted wherever they assume an MCP insert.
- `1.6_script.txt:33`: "אנון קי" → the publishable key; "מפתח תפקיד השרת" → the secret key.
- The `@supabase/ssr`/auth rewrite and removing Prisma stay in 1d.

#### Item 12, content part: old B (RV-L7, RV2-L3)
- Move `projects.md:174-318` (from "## פרויקט ב" up to, but not including, the `---` at `:319`) verbatim to `03-final-project/old_B-document-intelligence.md`.
  - The new file gets its own `<div dir="rtl" lang="he">` … `</div>`, plus a one-line note: unwired, not the new track B (PRD D5).
  - In `projects.md`, delete the now-redundant `---` (formerly `:319`), so one separator remains between A and C.
- `projects.md:7` "מתוך ארבעה" is left stale on purpose until 1e.

### 4.3 Tutor (group T)

#### Item 11: frontmatter
All 15 `learn/*.md` files get a leading `---\ndisable-model-invocation: true\n---` block, with no other keys. `display.md` gets it too, but nothing else (its English-only command list at `:114` is unreferenced; D8a folds it later). `learn.md` gets **no frontmatter**; its body edits are item 7 and, for item 12, `learn.md:105`: "project — final project mode" → "project — final projects (until unit 1e: shows 'being rebuilt')". S2a decides invocability (RV3-L3, RV4-L3).

#### Item 7: Hebrew aliases (S2)
- **`learn.md` Learner Commands:**
  - `continue / המשך`
  - `quiz me / בוחן` → `quiz.md` (covered sections)
  - `quiz me full / בוחן מלא` → `quiz.md` in **`quiz me full`** mode
  - `stop / עצור / סיום`
- **`learn.md` Route table (79–80):** the same words, naming the `quiz.md` mode. `quiz.md`'s **body** is untouched (it gets only item 11's frontmatter); it's F's (RV3-L3).
- **`progress.md` (RV5-L7):** the two trigger mentions, `:3` ("on the \"stop\" command") and `:99` ("## Session End (on \"stop\" command)"), name `stop / עצור / סיום`, so the Hebrew stop reaches the session-end section. Nothing else in `progress.md` changes.
- `teaching.md:144` and `setup.md:225` are unchanged.

#### Item 12 + G4: no capstones until 1e
- **`project.md`:** a new first section, `## Step 0 — TEMPORARY (until unit 1e)`. It shows "the final projects are being rebuilt; meanwhile, continue with the lessons (`/learn`)" in `session.language`, then stops without reading `projects.md`.
- **`resume.md`:** `:23`, `:38` and `:50` → one TEMPORARY rule, "Do not offer the final project until unit 1e". The route row `:74` stays.

#### Item 6: `security.md`
- **Ownership gate.**
  - A new Pre-flight step runs after `target_url` is known and before Phase A, on every entry path (`deploy` handoff, `security http…`).
  - It asks with `AskUserQuestion`: "Is this app yours, or do you have explicit permission to test it?" Only the affirmative option continues.
  - **On any other answer (RV2-L10):**
    - no network request of any kind is made, and no Phase (A–E) runs
    - the module shows a short explanation (testing without permission can cause harm and may be illegal)
    - it suggests rerunning `/learn security` with the URL of an app the learner owns, and then **ends**
- **`timingSafeEqual` (`:128-136`):**
  ```js
  const { createHash, timingSafeEqual } = require('node:crypto')
  const digest = (s) => createHash('sha256').update(String(s)).digest()

  const secret = process.env.SYNC_SECRET
  if (!secret) return res.status(503).json({ error: 'Service unavailable' })

  const provided = req.headers['x-sync-key']
  if (!provided || !timingSafeEqual(digest(provided), digest(secret))) {
    return res.status(401).json({ error: 'Unauthorized' })
  }
  ```
  Plus one sentence on why digests avoid the 500 and hide the key's length.

#### Item 14: the clean-slate step (S4, S5)
- **Placement:** `setup.md` gets a new **`## 0. Clean slate`**, before "## A. Show Current Settings" (RV2-L12).
- **Markers:** it sits between `<!-- CLEAN-SLATE:BEGIN — TEMPORARY, remove at first-cohort gate (PRD D10) -->` and `<!-- CLEAN-SLATE:END -->`.

**Behaviour:**
1. **Find.** Check exactly these paths, with no globs:
   - `$HOME/skill-tutor-tutorials/`
   - `$HOME/.claude/commands/learn.md`
   - `$HOME/.claude/commands/learn/`

   Relative paths are forbidden, because the repo has its own `skill-tutor-tutorials/`. If none exists, print one Hebrew line ("no leftovers from an earlier install were found") and continue to 0.1 (RV4-L1).
2. **Show.** Each path found, with its file count and newest modification date. Counts **never follow symlinks**: a symlink counts as one entry, and its target is shown next to it (RV2-L11, RV4-L4). The bash variant uses only **portable** commands that work on both GNU (Linux/WSL) and BSD (macOS) userlands, e.g. `find "$p" | wc -l` (no `-L`, no `-printf`) and `ls -ld`; never `stat -c` or `find -printf` (RV5-L3).
3. **Ask.** One `AskUserQuestion`, in Hebrew:
   - `להשאיר הכל` (listed first): nothing is touched.
   - `להעביר לגיבוי ולהתחיל מחדש`: everything moves to `~/skill-tutor-tutorials-backup-<date>`; nothing is lost.

   Only the second option is a yes.
4. **Move.** A bash variant and a PowerShell variant. Reference shape (bash):
   ```bash
   : "${HOME:?HOME is not set}"
   ts=$(date +%Y%m%d-%H%M%S)
   dest="$HOME/skill-tutor-tutorials-backup-$ts"
   : "${dest:?dest is not set}"
   mkdir "$dest" && mkdir "$dest/commands" || exit 1
   if [ -e "$HOME/skill-tutor-tutorials" ] || [ -L "$HOME/skill-tutor-tutorials" ]; then mv "$HOME/skill-tutor-tutorials" "$dest/" || exit 1; fi
   if [ -e "$HOME/.claude/commands/learn.md" ] || [ -L "$HOME/.claude/commands/learn.md" ]; then mv "$HOME/.claude/commands/learn.md" "$dest/commands/" || exit 1; fi
   if [ -e "$HOME/.claude/commands/learn" ] || [ -L "$HOME/.claude/commands/learn" ]; then mv "$HOME/.claude/commands/learn" "$dest/commands/" || exit 1; fi
   ```
   - **The whole move runs as one single Bash (or PowerShell) tool invocation**, never split across calls, because shell variables don't survive between tool calls. The block guards `: "${dest:?}"` right after computing `dest`, before the first `mv` (RV5-M5).
   - `mv` moves a symlink as a link and never follows it. PowerShell uses `Move-Item -LiteralPath … -ErrorAction Stop`, after checking `$HOME` and `$dest` are non-empty.
   - On any error: stop and report. Never retry with force, and never delete.
   - **Across filesystems (RV3-M4).** If a source sits on another filesystem (e.g. `~/.claude/commands` symlinked to `/mnt/c/…`), `mv` copies and then removes the original. An interruption leaves the original intact, or both copies, but never neither. The step claims "nothing is lost", not "nothing is unlinked".
5. **Verify and report.** Each original path is gone and present in the backup. The backup's **entry counts, taken the same no-follow way, equal the counts shown in step 2** (RV3-M4, RV4-L4). Print the backup path.
6. **Continue or stop.** If a global command was moved, stop and ask the tester to reopen Claude Code and run `/learn setup` again. Otherwise continue to 0.1.

**Hard rules, stated in the section:**
- only the three paths
- never anything inside the repo (the local settings file and the repo's `skill-tutor-tutorials/` are named explicitly; the settings file is written **without** backticks, RV-H4)
- never an earlier backup
- no delete command
- when in doubt, keep

**Reach (RV-H5, RV2-M2).** A personal `~/.claude/commands/learn.md` shadows the repo's `/learn` (skills.md). If it's a router from `c25e73c` or later, `/learn setup` still reaches this step, because such a router `Read`s the repo's `setup.md`. **Older global installs (before 2026-05-25) run their own inline setup, and this step never appears.** The README tester note therefore gives the manual fallback (§4.4).

#### S14: Claude Code version check (permanent)
- **Placement:** `setup.md` gets a new **`## 0.1 Claude Code version`**, directly after the CLEAN-SLATE end marker and before "## A". Every run reaches it, including a first run with no `settings.json`, because A says "skip directly to section B" (`setup.md:13`) (RV3-M1).
- **Behaviour:**
  - Run `claude --version` and take the first `X.Y.Z`.
  - Compare it with 2.1.176 **numerically, component by component (major, then minor, then patch), never as text** (RV2-L2).
  - If it's lower, show a short Hebrew warning and the update command (`claude update`), then continue.
  - If `claude` isn't on PATH (e.g. Desktop-bundled installs, the PRD D9a route), skip silently.
  - **Limitation (RV3-L4):** `claude --version` reports whichever `claude` is on PATH, which may not be the running binary; no version variable is exposed (§3). The PR notes both limitations.

### 4.4 Docs (group D)

#### Item 8 + G2: remove the global install
- **`setup.md`:** delete §F through its trailing separator (`:279-311`), so a single `---` (`:277`) remains before the re-lettered section. Re-letter "G. Setup Complete" → **F** (RV3-L2).
- **`README.md`:** delete `:46` and `:202`.
- **`CLAUDE.md`:** drop "global install" from `:14`, and delete step 4 at `:75`.
- **`CONTRIBUTING.md`:** delete `:61`.
- The existing `changes.md` sections are unchanged.

#### RV-L6: document the new frontmatter
The "add a module" steps in `README.md:196-202`, `CONTRIBUTING.md:57-61` and CLAUDE.md "הוספת מודול חדש" each gain one step: "start the file with the `disable-model-invocation: true` frontmatter block".

#### Item 13: README tester note
- **Placement:** under the title/banner, between `<!-- TEMPORARY: remove at first-cohort gate (PRD D10) -->` and `<!-- /TEMPORARY -->`.
- **Text:** the PRD's wording, then: "…or run `/learn setup`, which offers to move them into a backup for you. **If `~/.claude/commands/learn.md` exists and `/learn setup` doesn't offer to move it, you have an older global install: move or delete `~/.claude/commands/learn.md` and `~/.claude/commands/learn/` by hand, then restart Claude Code**" (RV2-M2, RV4-L1).

#### README version floor (S14, RV2-L6)
- "Step 1 — Prerequisites" (`:25`): "Claude Code 2.1.176 or later installed (Pro plan or higher)".
- "Requirements" (`:208`): the same.
- uv is not mentioned (learner-facing).

#### Contributor test command (S12, RV2-L7)
- **`CLAUDE.md`:** a new "## בדיקות (למפתחי הקורס בלבד — contributors only)" section. It says uv is required for contributors (install: https://docs.astral.sh/uv/getting-started/installation/), that learners don't need it, and gives:
  ```
  uv run ruff check -q && uv run pytest -q
  ```
  It adds: if pytest is red, re-run it with `uv run pytest -v`.
- **`CONTRIBUTING.md` "Pull Requests" (`:65-69`):** add one line, "run `uv run ruff check -q && uv run pytest -q` before opening a PR" (RV3-L2).

#### RV3-M7: document what CI now enforces, and the aliases
- **`CONTRIBUTING.md` "Adding a Lesson" (`:13-35`):** one line. CI requires ≥ 5 `[מעבר שקף]` markers per script, an exercise H1 with `שיעור X.Y` (and, where present, a matching `**שיעור:**` line), a `COURSE.md` row with a correct module range, and spoken lesson references that name existing lessons. "See `tests/validate_structure.py`. The example below predates these rules; F rewrites it." (RV4-L9)
- **`README.md` command table (`:113-124`) and `:72`:** add the Hebrew aliases: `continue / המשך`, `quiz me / בוחן`, `stop / עצור / סיום`.

#### `changes.md` (S11, S18)
Written once, as the last commit of group D, appended after the existing sections in the same style (an Overview, numbered `##` entries with Before/After, and a File Map):
1. `# Changes — fix/lesson-1.8-workers-ai-exercise branch` (#12, merged 2026-09-28), summarised from its merged diff
2. `# Changes — fix/lesson-2.5-2.6-content-corrections branch` (#13, merged 2026-09-28), likewise
3. `# Changes — fix/stage0-quick-wins branch`, with one entry per learner- or contributor-visible change, and a **Testers** note ("reset your data, or run `/learn setup` and choose the backup option")

---

## 5. Toolchain, lints, tests and CI (group P)

### 5.1 `tests/validate_structure.py` (library module)
- Pure functions, `check_<name>(root: Path) -> list[str]`, with findings formatted `path:line: [check] message`.
- A `CHECKS` tuple lists them all. No `main()`, no printing, no import-time work.
- **Course scope:** `courses/*/` except `courses/_archive/`, skipping `old_B*` files.
- **File discovery (RV2-L8):** a helper `repo_files(root, pattern)`:
  - uses `git ls-files -z` when `root/.git` exists, **as a file or a directory** (in a worktree `.git` is a file; RV5-L4), so local results match CI, and non-ASCII paths come out unquoted. Entries missing on disk (deleted in the working tree) are skipped (RV4-L10)
  - otherwise walks the filesystem (the pytest fixture trees)

| Check | Rule |
|---|---|
| `course_md` | For each course with a `COURSE.md`:<br>(a) the lesson numbers in "רשימת שיעורים" **equal** the lesson folders `lessons/*/<X.Y>-*`<br>(b) the table order equals numeric folder order<br>(c) each module row's folder exists, and its range equals `<min>–<max>` (or `—`; `–`/`-` both accepted) |
| `slide_markers` | Every `*_script.txt` has ≥ 5 `[מעבר שקף]` and zero `[SLIDE TRANSITION]` |
| `header_numbers` | **Exercises:** the first `# ` heading contains `שיעור X.Y`, and any `**שיעור:**` line contains `X.Y`, both equal to the folder.<br>**Scripts:** in the first 3 non-empty lines, every `(שיעור\|Lesson)\s+(\d+\.\d+)` and every `שיעור\s+([א-ת]+)\s+נקודה\s+([א-ת]+)` equals the folder. `W` is `[א-ת]+`, mapped by the digit-word table (אפס; אחת/אחד; שתיים/שניים/שתים; שלוש/שלושה; ארבע/ארבעה; חמש/חמישה; שש/שישה; שבע/שבעה; שמונה; תשע/תשעה); an unmapped word is a finding |
| `spoken_lesson_refs` (S17) | Signature `check_spoken_lesson_refs(root, allowlist=SPOKEN_ALLOWLIST)`, so tests pass their own allowlist (RV3-H3).<br>In every course-scope `*_script.txt` and `*_exercises.md`:<br>(a) every match of `(?<![א-ת])([א-ת]+)\s+נקודה\s+([א-ת]+)` whose words map through the digit-word table, after stripping **at most one** leading prefix letter from `ובלשהמכ` if the bare word isn't in the table, must form an `X.Y` that's an **existing lesson folder number** in that course<br>(b) every hyphenated ordinal `(ראשון|שני|שלישי|רביעי|חמישי|שישי|שביעי|שמיני)-([א-ת]+)`, mapped to X and Y the same way, must likewise name an existing lesson<br>A match inside an allowlisted phrase is skipped. `SPOKEN_ALLOWLIST` is a tuple of (file-name glob, exact phrase), seeded from §4.2's stay list:<br>• `0.3_script.txt`, "ושבע נקודה אחת אחוז"<br>• `1.1_script.txt`, "ארבע נקודה שש" and "שש נקודה שש מיליארד"<br>• `1.5_script.txt`, "שישה נקודה שישה מיליארד"<br>• `2.1_script.txt`, "שתיים נקודה אפס"<br>• `2.5_script.txt`, "שלוש נקודה שלוש עשרה", "שלוש נקודה ארבע עשרה" and "ארבע נקודה שבע"<br>**Stale entry (a finding):** the glob matches at least one course-scope file, and the exact phrase occurs in none of them (RV3-H3). N replaces this check |
| `course_name_denylist` | No `קורס\s+(ה-)?AI Engineer`, `\*\*קורס:\*\*\s*AI Engineer` or `AI Engineer course` (case-insensitive) in course scope. The job title passes. **Plus (S19):** `NEXT_PUBLIC_SUPABASE_ANON_KEY`. The check keeps its name, since F renames it into the full denylist |
| `tutor_refs` | In `.claude/**/*.md`:<br>(a) backticked paths starting with `.claude/` or `courses/` exist, except `LOCAL_ONLY = {".claude/settings.local.json"}`<br>(b) a backticked bare `name.md` directly after a word-bounded `Read`/`Load` (any case) exists in the referring file's folder<br>Skips `~/…` and placeholders (`[`, `{`, `*`, `X.Y`). **`${CLAUDE_SKILL_DIR}` resolution is M's extension (§9; RV2-M4)** |
| `settings_json` | `.claude/settings.json`, if present, parses, and contains no `powershell` (case-insensitive) |
| `relative_links` | In every tracked `*.md`, after removing fenced blocks and inline code spans, every `[text](target)` that isn't `http:`/`https:`/`mailto:`/`#…` resolves (after stripping `#fragment`). Skips `_archive/` and `old_B*` |
| `clean_slate_no_delete` | *Temporary.* Between the CLEAN-SLATE markers in `setup.md`, matched **case-insensitively** (PowerShell ignores case; RV5-L2): no `\brm\b`, `\brmdir\b`, `\bdel\b`, `\berase\b`, `\brd\b`, `\bri\b`, `Remove-Item`, `\bunlink\b`, `-delete\b`, `rmtree`, `::Delete\(`. **Both markers must be present in `setup.md`; a missing marker is a finding** (RV3-M5). The check is deleted together with the section at the gate |
| `lesson_files` *(existing)* | Every lesson folder has `*_script.txt` and `*_exercises.md`; course-scoped |
| `teaching_step5` *(existing)* | `teaching.md` contains "Step 5" |

### 5.2 `tests/test_validate_structure.py` (pytest)
- **Fixture:** a `good_tree` fixture in `tmp_path`, deliberately **not** a git repo, so it exercises the filesystem path of `repo_files`. It contains:
  - one course with modules `00-…` (lessons 0.1, 0.2) and `02-…` (lesson 2.1), valid scripts and exercises, and `COURSE.md`
  - `.claude/commands/learn.md` routing to `teaching.md` ("Step 5" plus `Read \`quiz.md\``), `quiz.md`, and `setup.md` (with CLEAN-SLATE markers)
  - `.claude/settings.json`
  - a README with a relative link
  - a script with a spoken reference to an existing lesson, and one phrase in the **fixture's own** allowlist (passed to the check explicitly)
  - between the CLEAN-SLATE markers, a bash block **and a PowerShell block** (`New-Item`, `Move-Item -LiteralPath`) with no delete verbs (RV3-M3)
- **`test_good_tree_passes`:** every check returns `[]`.
- **A separate `git_tree` test:** `git init` + `git add` on a copy of the good tree, plus one **untracked** broken-link file. `relative_links` ignores the untracked file.
- **One way to call checks on fixtures (RV4-H1):** a `fixture_checks()` helper returns `CHECKS` with `spoken_lesson_refs` bound to `allowlist=FIXTURE_ALLOWLIST` (e.g. `functools.partial`). **Every** fixture test (good tree, seeds and negatives) uses it. The default `SPOKEN_ALLOWLIST` is used only by `test_real_repo_passes`. Seeds for `spoken_lesson_refs` sit after line 3, so `header_numbers` never sees them.
- **Seeded regressions,** parametrized. Each asserts the named check fails and all others pass. At minimum:
  - `course_md`: a missing row; an extra row; a swap; a wrong range
  - `slide_markers`: 4 markers; `[SLIDE TRANSITION]`
  - `header_numbers`: `שיעור 5.1` in 2.1; a mismatched `**שיעור:**`; `שיעור 0.1` in 0.2; spelled "שיעור אפס נקודה אחת" in the 2.1 script (an existing but wrong lesson, so `spoken_lesson_refs` stays green, RV4-H1); an unmapped word
  - `spoken_lesson_refs`: "שלוש נקודה שתיים" (no lesson 3.2); prefixed "ושלוש נקודה חמש"; a gendered form "שישה נקודה שבעה"; a hyphenated "חמישי-ארבע"; a stale allowlist entry (the fixture's own allowlist names a phrase absent from its file)
  - `course_name_denylist`: `בקורס AI Engineer`; `- **קורס:** AI Engineer`; `NEXT_PUBLIC_SUPABASE_ANON_KEY`
  - `tutor_refs`: a missing `.claude/…` route; `Read \`missing.md\``
  - `settings_json`: `powershell`; invalid JSON
  - `relative_links`: a missing target
  - `clean_slate_no_delete`: `rm -rf`; `Remove-Item`; lower-case `remove-item`; `[IO.Directory]::Delete(`; the END marker missing
  - `lesson_files`: missing exercises
  - `teaching_step5`: "Step 5" removed
- **Must-pass negatives,** parametrized:
  - the job title
  - denied strings in `_archive/` and `old_B-x.md`
  - `~/…`; `.claude/settings.local.json`; `${CLAUDE_SKILL_DIR}/x.md`
  - "already … `x.md`"; "load … from `projects.md`"
  - `http(s)` and `#anchor` links; a broken link in a code fence and in inline code
  - spelled numbers followed by `,` `:` `.`
  - an allowlisted phrase; a spoken reference to an existing lesson
  - "Confirm", "model" and "perform" between the markers; `rm` outside them
  - a missing `settings.json`
- **`test_real_repo_passes`:** every check on the real repo, with the findings in the assertion message. Red until groups C and T land: it turns green at the T5 (clean-slate) commit, and group D must keep it green.

### 5.3 Toolchain files
- **`pyproject.toml`:**
  ```toml
  [project]
  name = "tov-learn"
  version = "0.0.0"
  requires-python = ">=3.14,<3.15"

  [dependency-groups]
  dev = ["pytest>=9.1.1", "ruff>=0.16.9"]

  [tool.uv]
  package = false
  required-version = ">=0.12"

  [tool.pytest.ini_options]
  testpaths = ["tests"]

  [tool.ruff]
  target-version = "py314"
  ```
- **No `.python-version`** (S13).
- **`uv.lock`:** generated **with the CI-pinned uv 0.12.19** (e.g. `uvx --from uv==0.12.19 uv lock`), so `uv sync --locked` can't drift between the local 0.12.1 and CI (RV2-L9). Committed.
- **`.gitignore`:** add `.venv/`, `__pycache__/`, `.pytest_cache/` and `.ruff_cache/`.

### 5.4 CI
**`.github/workflows/validate.yml`:**
```yaml
name: Validate Skill Structure

on:
  pull_request:
    branches: [master]
  push:
    branches: [master]

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
      - uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
        with:
          version: "0.12.19"
          python-version: "3.14"
      - name: Sync (locked)
        run: uv sync --locked
      - name: Ruff
        run: uv run ruff check -q
      - name: Tests (seeded regressions + real repo)
        run: uv run pytest -q
```

**`.github/dependabot.yml`:**
```yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

Ruff runs before the tests, matching S20, so a red test never hides a lint result (RV4-L2).

### 5.5 Item 2
`.claude/settings.json` becomes `{}`. `auto-save-progress.ps1` stays for M.

### 5.6 Forward compatibility
F and G add checks as `check_*` functions plus test cases. `jsonschema`, if needed (D8c), goes in the dev group, used only by tests. That means contributors install it locally too, which diverges from D8c's "installed only in CI" (§8, RV3-L8).

---

## 6. Verification and the PR

### 6.1 Commit order
On `fix/stage0-quick-wins`, only when the user asks:
1. **P1:** `pyproject.toml`, `uv.lock`, `.gitignore`, the validator, the tests, `validate.yml` and `dependabot.yml`. They land together because CI needs the tests. The message lists the red findings.
2. **P2:** `settings.json` → `{}`.
3. **C:** COURSE.md → VAT → 0.4 markers → residue → 1.3 → 1.6 → old_B, one commit each.
4. **T:** frontmatter → aliases → project/resume → security → clean-slate → version check.
5. **D:** global install → frontmatter docs → tester note → version floor → test command → CI-rules line + README aliases (RV3-M7; RV5-L5) → `changes.md` (last).

Each commit runs `uv run ruff check -q && uv run pytest -q` (S20). Only `test_real_repo_passes` may be red before the end, and the last commit is fully green.

### 6.2 PR description (required sections)
- **Summary:** every item, G*, and RV-* through RV5-* fix, each mapped to a commit; links to the three new `changes.md` sections.
- **Automated verification:**
  - the `uv run pytest -q` result, plus the test IDs from `uv run pytest --collect-only -q` (S20)
  - ruff clean
  - the Actions run, plus the pasted `gh run view` / check-run annotations output. **Pass condition (RV4-M3): no annotation mentions `Node.js 20` or `node20`.** The notice "The ubuntu-latest label will migrate to Ubuntu 26 beginning October 19, 2026" is **expected** and doesn't fail the check (`runs-on: ubuntu-latest` is kept by user decision)
  - the item-3 VAT grep returning nothing
  - two more greps (RV5-L6): all 15 `.claude/commands/learn/*.md` start with the `disable-model-invocation: true` block (`for f in .claude/commands/learn/*.md; do head -3 "$f"; done`), and `grep -n "Global Install" .claude/commands/learn/setup.md` returns nothing
- **Manual verification.** The user runs these interactively in the worktree. Each records steps, date, OS/shell, Claude Code version, who ran it, result and cleanup.
  **Order and isolation (RV4-M4a):** run the checks in the order **0 → 2a → 2b → 1 → 3 → 2 → 4 → 5 → 6**. At the end of every check that touches `$HOME`, remove exactly the fixtures it created (and any learner data it caused, e.g. check 6's progress files), so the next check starts from the precondition state.
  0. **Precondition (RV3-M2).** Before **every** check that touches `$HOME` (1, 2a, 2b, 3, 5 and 6; RV5-M3):
     - Confirm `$HOME/skill-tutor-tutorials`, `$HOME/.claude/commands/learn.md` and `$HOME/.claude/commands/learn` **don't exist**.
     - If any does, move it aside to `$HOME/stage0-manual-check-aside-<ts>/` first, and restore it afterwards.
     - Run the checks from WSL/Linux only. The Windows-side `/mnt/c/Users/…/skill-tutor-tutorials` holds real data and is never touched.
     - Cleanup steps delete only what the check itself created.
  1. **Resume:** fake `progress/lesson-0.1…1.8.md`, `settings.json` and `learner_profile.md` under `~/skill-tutor-tutorials/`. `/learn` offers 2.1, with **no** 🏗️ line.
  2. **Hook error:** two replies in a worktree session. No "hook error" notice.
  2a. **Version check on a first run (RV3-M1):** with no `~/skill-tutor-tutorials/settings.json`, `/learn setup` reaches step 0.1, with no warning at the current version.
  2b. **Version-check warning branch (RV4-M4b, RV5-M2):**
     - A PATH shim doesn't work on this machine: `~/.bashrc:118` and `~/.profile:26` put `~/.local/bin` first again in every tool shell.
     - Instead, temporarily change the floor in the worktree's `setup.md` step 0.1 from `2.1.176` to **`2.1.1000`**. It's numerically above the installed version (e.g. 2.1.283) but sorts *below* it as text.
     - Run `/learn setup`. Step 0.1 shows the Hebrew warning and then continues. That proves the comparison is numeric.
     - Restore it with `git checkout -- .claude/commands/learn/setup.md`, and confirm `git diff` is empty.
  3. **Clean-slate:**
     - Hash the main checkout's local settings file first.
     - Fixtures: `~/skill-tutor-tutorials/` (one file), `~/.claude/commands/learn/` (one file), and `~/.claude/commands/learn.md` as a **copy of the worktree's `learn.md`**.
     - Run `/learn setup`. The step-0 prompt appears.
     - Keep → nothing moved. **Abort setup right after answering the step-0 prompt** (Esc), so no `settings.json` or `learner_profile.md` is written into the fixture folder (RV5-L1).
     - Rerun, move → all three are in the backup, originals gone, `git status` clean, restart message shown, no local settings file created in the worktree.
     - **At every permission prompt, answer "Yes" (once), never "Yes, and don't ask again"**, which would write an approval into the hashed file (RV2-L1). The hash must then be unchanged. Record the prompts.
     - Remove the backup only after confirming it contains nothing but the fixtures.
  4. **1.3 exercise 5** (Linux/bash): steps 1–5 in a throwaway lab created **outside the repo** (e.g. `~/stage0-lab-<ts>/`), so no repo `CLAUDE.md` or settings load (RV5-L9). Record the step-5 outcome.
  5. **Security gate:** first create fixture `~/skill-tutor-tutorials/settings.json` and `learner_profile.md` (as in check 1), so `/learn` doesn't route into setup. Then `/learn security https://example.com` → "no". No `curl` runs, and the module ends. Remove the fixtures (RV5-M3).
  6. **Aliases and project:** create the same fixtures, then start `/learn 0.1` (RV5-M3):
     - `בוחן` starts a quiz.
     - `עצור` saves progress.
     - `בחן אותי` still switches to **diagnostic** mode (RV2-L12).
     - `/learn project` shows the rebuilt message.
     - Afterwards, remove the fixtures and any progress/tutorial files the session wrote.
- **Untested (stated explicitly):**
  - the native-PowerShell hook variant
  - the 1.6 MCP add + Authenticate flow, unless a contributor with a Supabase project runs it
  - the version check on Desktop-bundled installs (it skips), and the PATH-binary limitation (RV3-L4)
  - the **bash variant on macOS** (portable commands required, but only run on Linux/WSL; RV5-L3)
  - the **PowerShell variant of the clean-slate move** (RV3-M3). It follows the bash variant's rules and is lint-checked for delete verbs, but has never run on Windows
- **Future concerns:** §9.
- **Reviewer note:** Hebrew changes need a Hebrew-speaking contributor's approval.

### 6.3 Done-when (§3) → proof

| Done when | Proof |
|---|---|
| Each new lint fails on a seeded regression and passes on the fixed tree | §5.2, `test_real_repo_passes`, and the P1 message |
| `resume` offers 2.1 after 1.8 | `course_md` (a) rows = folders, and (b) order; plus manual check 1 (RV5-L9) |
| 0.4 splits into slides | `slide_markers` |
| No hook error after replies | `settings_json` plus manual check 2 |
| `validate.yml` has no Node deprecation warning | the annotations evidence: nothing mentions Node.js 20 / node20; the ubuntu-latest notice is expected (RV4-M3) |
| The clean-slate step backs up before any delete | S4, `clean_slate_no_delete`, and manual check 3 |

Manual checks 4–6, the VAT grep and `spoken_lesson_refs` cover changes that §3 doesn't name.

---

## 7. Risks

| Risk | Mitigation |
|---|---|
| The heuristics miss a spoken form | §4.2 inventory; `spoken_lesson_refs`; N replaces both |
| The replacement Hebrew reads badly | Minimal edits; a Hebrew reviewer |
| A clean-slate move fails part-way, or crosses filesystems | It stops at the first error; the original survives until its copy is complete; file counts are verified (RV3-M4) |
| A tester with a pre-2026-05-25 global install never sees the step | The README fallback instructions (§4.4) |
| Pins go stale | SHA pins plus Dependabot (S15) |
| Contributors without uv | Install link in CLAUDE.md and CONTRIBUTING; learners unaffected |
| The Windows hook variant or the MCP flow is wrong | Flagged untested; 1a and 1d rewrite them |

---

## 8. Proposed PRD amendments

**Applied to the PRD on the docs branch on 2026-09-29, before the docs PR** (RV5-L5; user-approved), as the PRD's new "§8 Amendments from the Stage 0 spec" plus inline pointers:
1. **D2 item 5:** G1 preambles; the RV-M1 cross-references; the full spoken-number inventory (RV2-M6).
2. **D2 item 8:** G2 locations; the frontmatter step in the add-a-module docs.
3. **D2 item 12:** `resume.md` too (G4).
4. **D2 item 7:** aliases per S2.
5. **D2 item 14:** a move, exact paths, and the README fallback for pre-`c25e73c` installs.
6. **D2 item 15:** `setup-python` → `setup-uv`; the contributor toolchain uv + pytest + ruff; Python 3.14 in `pyproject.toml` only.
7. **D2 item 16:** `1.6_script.txt:33`; the read-only MCP with the `/mcp` Authenticate step; the `:103` rewrite.
8. **D2 item 10:** the Claude Code floor 2.1.176 (S14), in `1.3_exercises.md:8`, `1.3_script.txt:15` and README; the CHANGELOG facts go into §7.
9. **D2 item 3:** seven VAT occurrences.
10. **D7c:** Stage 0 also adds `spoken_lesson_refs` (S17), with its stale-allowlist rule; one denylist entry (S19); and the **temporary** `clean_slate_no_delete` check, which the gate removes together with the CLEAN-SLATE section (D10 gate list) (RV5-L5).
10a. **D8c:** `jsonschema` would be a dev-group dependency, installed locally as well as in CI (RV3-L8).
11. **§6 Dependabot row:** decided (S15).
12. **New unit N** between F and 1a (S10).
13. **D8d / §3 row M:** M's done-when ("the reference lint passes") is vacuous until M extends `tutor_refs` to resolve `${CLAUDE_SKILL_DIR}` (§9) (RV5-L5).

---

## 9. Out of scope: future concerns

| Unit | Concern carried forward |
|---|---|
| M | Drop `auto-save-progress.ps1` and the slide viewer; the CLAUDE.md module table and its lint. **Before `tutor_refs` can serve as M's done-when (PRD D8d), M must extend it to resolve `${CLAUDE_SKILL_DIR}/…` against the folder of the nearest `SKILL.md`, with seeded tests (RV2-M4).** Otherwise the lint passes vacuously |
| F | `landscape.md` (including the Claude Code floor and the Node row); baseline/model-string/full denylist; the rest of CONTRIBUTING; the style guide; `changes.md` → Keep-a-Changelog; `quiz.md:14` Hebrew triggers; `jsonschema` in the dev group if needed |
| **N (proposed)** | Numbering contract:<br>• stable lesson ids as the contract; numbers derived<br>• a manifest<br>• a deterministic generator (COURSE.md tables, exercise and script headers, inside `<!-- generated -->` markers)<br>• CI `--check`<br>• id references in prose<br>• a thin `renumber`/`add-lesson` skill<br>• a CLAUDE.md rule to run the generator before any push (convenience; CI enforces)<br>Replaces `header_numbers` and `spoken_lesson_refs` |
| G | Interpreter resolution; owned `settings.local.json` entries; the no-`python3` lint; branch protection. **Constraints: learner tooling must not require uv; no `.python-version` at the repo root** |
| 1a | The full 1.3 lab; macOS/Windows OS-lock equivalents (UNVERIFIED); 1.2 fixes; 1.1 homework |
| 1b | Module 0 reorder, renumbering 0.x again (update `SPOKEN_ALLOWLIST` accordingly) |
| 1c | Module 02 rename. `2.5_script.txt:97` expands MCP as "Multi-Claude-Pipeline" (RV3-L12). **If 2.0 teaches uv, learner projects live outside the repo folder** (uv project discovery would otherwise attach to `tov-learn`) |
| 1d | `@supabase/ssr`/auth rewrite; Prisma removal; an end-to-end check of the MCP flow |
| 1e | Restore `/learn project` and the resume offer; delete the TEMPORARY blocks; `projects.md:7` |
| Gate | Remove the README tester note, the CLEAN-SLATE section and `clean_slate_no_delete` |
| S2a | Whether `learn.md` stays model-invocable; 3-OS pytest CI (already on uv); learner CLI without uv; Dependabot `uv` once 0.12 support is confirmed |

---

## 10. Change log

### First independent review (2026-09-27)
A fresh Opus 5.5 Plan agent (single, read-only, no context) raised 22 findings: 5 High, 8 Medium, 9 Low. All were accepted.

| # | Finding | Resolution |
|---|---|---|
| RV-H1 | `tutor_refs` (b) flagged 5 real lines | Directly-after-Read/Load regex |
| RV-H2 | The read-only MCP broke `:103` | S16 |
| RV-H3 | Delete-command substrings hit "Confirm"/"model" | Word-bounded regexes |
| RV-H4 | `settings.local.json` is absent in CI | `LOCAL_ONLY`; no backticks |
| RV-H5 | A personal `learn.md` fixture shadows the project command | Fixture = copy of the worktree router |
| RV-M1 | Missed cross-references | §4.2 |
| RV-M2 | VAT `0.17` missed | §4.2 (now seven, RV2-M1) |
| RV-M3 | `python` missing; the unittest exit-5 trap | uv + pytest + ruff (S6, S12, S13) |
| RV-M4 | `relative_links` flagged inline code | Strip inline code |
| RV-M5 | `if` needs a newer Claude Code | S14 |
| RV-M6 | `1.6_script.txt:33` | Item 16 |
| RV-M7 | Tokenizing unspecified | `[א-ת]+` |
| RV-M8 | Behaviours without evidence | Manual checks 4–6 |
| RV-L1…L9 | Worktree settings assertion; 1.3 leftovers; counts; S11 reason; Dependabot; frontmatter docs; old_B tidy; `quiz.md:14`; `0.2:9` | §6.2, §4.2, §1, S11, S15, §4.4, §4.2, §4.3, §4.2 |

### Second independent review (2026-09-28)
A fresh Opus 5.5 Plan agent (single, read-only, no context) raised 19 findings: 1 High, 6 Medium, 12 Low. All were accepted.

| # | Finding | Resolution |
|---|---|---|
| RV2-H1 | Local `master` was 4 commits ahead of `origin/master` (#12/#13 open), and S11 said they were merged | The user merged #12 and #13 on 2026-09-28. Local `master` was moved to `origin/master` after proving identical trees, and the docs branch was rebased. Baseline and S11 corrected; §1 adds a pre-worktree check |
| RV2-M1 | VAT had seven occurrences | §4.2, plus a completion grep in the PR |
| RV2-M2 | Pre-`c25e73c` routers set up inline, so the step never runs | The reach note is corrected; the README fallback |
| RV2-M3 | The MCP authentication step was missing | The `/mcp` → Authenticate step (S16) |
| RV2-M4 | `tutor_refs` can't prove M | Recorded as M's extension (§9) |
| RV2-M5 | A root `.python-version` could pin learners' Python | Dropped; `requires-python` plus setup-uv's `python-version` (S13) |
| RV2-M6 | Out-of-window spoken numbers had no completion check | Full inventory (§4.2) plus `spoken_lesson_refs` (S17) |
| RV2-L1 | "Don't ask again" writes to the hashed file | Answer "Yes" once only |
| RV2-L2 | Version compare unspecified | Numeric by component; the Desktop skip is noted |
| RV2-L3 | The old_B range carried a `---` | Move 174–318 |
| RV2-L4 | "Hooks run via bash" | §3 wording |
| RV2-L5 | Takeaway imprecise; `sudo` line risky | Deny rules and sandbox named; "illustration only, don't run" box |
| RV2-L6 | README Prerequisites missed the floor | `:25` added |
| RV2-L7 | CLAUDE.md loads for learners | "contributors only" heading |
| RV2-L8 | Filesystem walk ≠ CI | `git ls-files` via `repo_files` |
| RV2-L9 | Lock generated with a different uv | Lock with 0.12.19 |
| RV2-L10 | Refusal path unclear | No network, no phases; the module ends |
| RV2-L11 | `HOME` and symlink guards | `: "${HOME:?}"`; links moved, not followed |
| RV2-L12 | A.1 ordering; `2.6:77` bridge; alias mix-up; `display.md` | `0.` / `A.1` placement (A.1 later moved to `0.1`, RV3-M1); teaser cut; manual check for `בחן אותי`; noted |

### Third independent review (2026-09-28)
A fresh Opus 5.5 Plan agent (single, read-only, no context) raised 22 findings: 3 High, 7 Medium, 12 Low. All were accepted.

| # | Finding | Resolution |
|---|---|---|
| RV3-H1 | Missed `1.1:171` "ושלוש נקודה חמש" and `2.3:72` "חמישי-ארבע"; the S17 regex skipped prefixed words and hyphen ordinals | Inventory rebuilt with the S17 parser (§4.2); one-letter prefix stripping and hyphen ordinals in S17; seeded cases |
| RV3-H2 | `1.5:7` "שישה נקודה שישה" wasn't allowlisted, so the fixed tree would stay red | Added to the stay list and `SPOKEN_ALLOWLIST`; the inventory covers every table form |
| RV3-H3 | A fixed allowlist contradicted the fixture; "stale" was undefined; the 1.3 entry was redundant | Allowlist passed as a parameter; stale = glob matches a file and the phrase occurs in none; 1.3 entry dropped (it parses as 2.1) |
| RV3-M1 | A.1 was skipped on first runs (`setup.md:13`) | Moved to `## 0.1`, before A; manual check 2a |
| RV3-M2 | Manual checks could clobber real data (`/mnt/c/…/skill-tutor-tutorials` exists) | Step-0 precondition, move-aside and restore, WSL only, cleanup limited to fixtures |
| RV3-M3 | The PowerShell clean-slate variant was untested and unflagged | Listed as untested; a PowerShell block added to the fixture |
| RV3-M4 | `mv` across filesystems copies, then unlinks | "Nothing is lost" wording; file-count verification |
| RV3-M5 | `clean_slate_no_delete` passed vacuously without markers | Markers required; seeded case |
| RV3-M6 | The baseline guard didn't pin `290af75` | `git fetch`; compare to `290af75`, or require an empty non-docs diff, or stop |
| RV3-M7 | Aliases and CI-enforced lesson rules undocumented | README command table and `:72`; CONTRIBUTING "Adding a Lesson" |
| RV3-L1 | `pytest -q` shows no passing IDs | `--collect-only -q` for the PR; `-v` on red (S20; the user's `-q`-first proposal) |
| RV3-L2 | `setup.md` §F range; CONTRIBUTING range | `:279-311`; `:65-69` |
| RV3-L3 | "No other change" / "untouched" / "unchanged" wording | Scoped to markers, body, frontmatter |
| RV3-L4 | `claude --version` may read another binary | Stated as a limitation; no version env var exists |
| RV3-L5 | `1.3:15` is the auto-memory sentence | Reworded as a lesson-wide requirement |
| RV3-L6 | Ruff skipped while pytest is red | Ruff first (S20) |
| RV3-L7 | Python 3.15.0 on 2026-10-01; support dates | S13 reason and §3 updated; 3.14 kept |
| RV3-L8 | `jsonschema` vs D8c "CI only" | §5.6 note and amendment 10a |
| RV3-L9 | "במודול 02" in spoken text | "במודול שתיים" |
| RV3-L10 | `0.1:125` bridge | Known churn (1b) |
| RV3-L11 | Optional denylist entries | Added (S19) |
| RV3-L12 | `2.5:97` MCP expansion (1c); S18 rationale selective | 1c's concern; S18 rationale scoped |

### Fourth independent review (2026-09-28)
A fresh Opus 5.5 Plan agent (single, read-only, no context) raised 15 findings: 1 High, 4 Medium, 10 Low. It re-derived the full spoken-number inventory, the VAT list and every line number independently and found no new content gaps. All were accepted. M2 was resolved as a known, deferred item by user decision.

| # | Finding | Resolution |
|---|---|---|
| RV4-H1 | "Named check fails, all others pass" was unsatisfiable: the header seed tripped `spoken_lesson_refs`, and the default allowlist went stale on fixture files | `fixture_checks()` binds `FIXTURE_ALLOWLIST` for every fixture test; the header seed uses an existing but wrong lesson; spoken seeds sit after line 3 |
| RV4-M1 | Denying "קוד יציאה אחד" would block the required correction | The entry is narrowed to the wrong claim `מחזיר(ה\|ים)? קוד יציאה אחד`; a must-pass case for the correction |
| RV4-M2 | The docs aren't on `master`, so the Stage 0 worktree lacks the spec | **Deferred (user decision):** a docs PR is merged manually after the spec is locked, before implementation. Reviewers ignore this (§1) |
| RV4-M3 | "No deprecation annotation" is ambiguous given the ubuntu-latest notice | Pass = no Node.js 20 / node20 annotation; the Ubuntu 26 notice is expected; `ubuntu-latest` kept (user decision) |
| RV4-M4 | Manual checks shared state; the version-warning branch was never exercised | Fixed order plus per-check cleanup; the precondition applies to every `$HOME` check; new check 2b with a `claude` shim printing 2.1.99 |
| RV4-L1 | The README fallback misdiagnosed "no leftovers" | Step 0 prints "no leftovers found"; the README fallback is conditioned on `learn.md` existing |
| RV4-L2 | CI ran pytest before ruff | Ruff first |
| RV4-L3 | Item 12's `learn.md` edit was undefined | `learn.md:105` wording specified |
| RV4-L4 | Symlink counts were ambiguous | No-follow counting, a link = one entry |
| RV4-L5 | Undocumented `CLAUDE_CODE_EXECPATH` | Noted in §3; the documented mechanism is kept |
| RV4-L6 | `@file` may bypass the Read hook (unverified) | "Ask in words" in step 3; mentioned in the takeaway |
| RV4-L7 | S18's list of PRs without sections was short | "#1, #5–#11" |
| RV4-L8 | The PR summary omitted RV3 | "RV-* through RV4-*" |
| RV4-L9 | The new CONTRIBUTING line sits beside a non-compliant example | Note that F rewrites the example |
| RV4-L10 | `git ls-files` quoting, and deleted files | `-z`; skip entries missing on disk |

### Fifth independent review (2026-09-29)
A fresh Opus 5.5 Plan agent (single, read-only, no context; told to ignore the deferred docs-on-`master` item) raised 14 findings: **0 High**, 5 Medium, 9 Low. It re-derived the inventories, pins and line numbers and found no content gaps. All recommendations were accepted, and the user locked the spec.

| # | Finding | Resolution |
|---|---|---|
| RV5-M1 | The narrowed exit-code regex still matched the natural correction | Entry **dropped** (S19); only `NEXT_PUBLIC_SUPABASE_ANON_KEY` is added |
| RV5-M2 | The PATH shim is shadowed (`~/.bashrc:118`, `~/.profile:26`) | Check 2b uses a temporary floor of `2.1.1000` in the worktree's `setup.md`, then `git checkout` |
| RV5-M3 | Checks 5 and 6 routed into setup and weren't isolated | Both get fixtures, are in the `$HOME` list, and clean up; check 6 starts `/learn 0.1` |
| RV5-M4 | No remedy when local `master` lags | `git merge --ff-only origin/master`; stop if it diverges |
| RV5-M5 | The move split across tool calls would lose `$dest` | One invocation; `: "${dest:?}"` guard |
| RV5-L1 | The Keep run wrote setup files into the fixtures | Abort after the step-0 answer |
| RV5-L2 | Delete-verb match was case-sensitive | Case-insensitive; `::Delete(` added |
| RV5-L3 | macOS bash variant untested; GNU-only commands | Portable commands required; listed untested |
| RV5-L4 | `.git` is a file in a worktree | "file or directory" |
| RV5-L5 | RV3-M7 had no commit slot; two amendments missing; amendment timing | Commit slot; amendments 10 and 13; applied to the PRD before the docs PR |
| RV5-L6 | Frontmatter and global-install removal had no check | Two greps in the PR evidence |
| RV5-L7 | `progress.md` keys on "stop" only | Two trigger lines edited |
| RV5-L8 | Approval location is version-dependent | "from v2.1.211" |
| RV5-L9 | Small inconsistencies (CONTRIBUTING wording, done-when mapping, S18 and docs PR, line shifts, lab location) | Each fixed in place |

### Plan review (2026-09-29, rev 6.1)
A fresh single-agent review of the implementation plan also reported four editorial inconsistencies in this spec. All were fixed in place, and no decision changed. Its plan findings were fixed in the plan.

| # | Finding | Resolution |
|---|---|---|
| PR-S1 | §5.2 said `test_real_repo_passes` stays red "until groups C, T and D land", but the tree is clean after T5 | "Red until groups C and T land"; D keeps it green |
| PR-S2 | §1 called the `progress.md` change "a one-line edit"; §4.1 and §4.3 edit two trigger lines | "a two-line edit" |
| PR-S3 | In §4.3 item 14's bash reference shape, the `: "${dest:?}"` guard sat after `mkdir` (and was unindented), contradicting the bullet below it | Guard moved to right after `dest` is computed, before `mkdir` |
| PR-S4 | §6.2's Summary listed fixes "RV-* through RV4-*", omitting RV5 fixes that change behaviour | "RV-* through RV5-*" |
