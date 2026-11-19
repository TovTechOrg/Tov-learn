# Stage 0 Quick-Win PR Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task, **inline** in your own session (the user's choice, 2026-09-29). At the end, one fresh Opus 5.5 subagent reviews the whole branch (Task 23 Step 4). Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** One PR against `master`, on branch `fix/stage0-quick-wins`, that fixes what testers hit now, adds the first CI lints (each proven by a seeded regression), and moves CI to `node24` actions on uv + pytest + ruff.

**Architecture:** The lints are pure `check_*` functions in a library module (`tests/validate_structure.py`), exercised by pytest against small fixture trees and against the real repo. Every content change is an exact text edit driven by a small helper; each helper run either applies completely or writes nothing, and the recovery rule under Conventions returns a half-done task to the last commit. Commits follow the spec's §6.1 order (P1 → P2 → C → T → D, with `changes.md` last). The real-repo test is red from P1 and turns green at T5.

**Tech Stack:** uv 0.12.19 (CI pin; local ≥ 0.12), Python 3.14, pytest ≥ 9.1.1, ruff ≥ 0.16.9, GitHub Actions (`actions/checkout` v7.0.1, `astral-sh/setup-uv` v10.2.0, SHA-pinned), Claude Code slash-command markdown (the tutor), Hebrew course content.

**Spec:** `docs/superpowers/specs/2026-09-27-stage0-quick-wins-design.md` (revision 6.1, locked 2026-09-29; rev 6.1 is editorial only). Parent PRD: `docs/prds/project-redesign-2026-09-25.md`, whose §8 amendments A1–A13 win over the text above them. Read the spec before starting. This plan argues from it and does not repeat its reasons.

**How this plan was checked (2026-09-29):** the validator and the tests below were run with uv 0.12.19, pytest 9.1.1 and ruff 0.16.9 against a clone of the docs branch. Every edit block in Tasks 2–22 was then applied in order to a second clone, and the real-repo finding count after each task matched the **Expected** line of that task. The fixed tree ended with 0 findings, `ruff check` clean, and 58 tests passing. This plan file itself passes `relative_links`. A fresh single-agent review of this plan (2026-09-29) found no High issues. Its 2 Medium and 6 Low findings are fixed here: sentinel-guarded cleanup and a settings hash at every manual check, the Task 1 Step 5 expectation, abort recovery, commit authorization in Task 0, the CI-run race, and PowerShell dangling links. Its 4 spec findings are fixed in spec rev 6.1 (§10, PR-S1–S4). The dry run above was repeated after the fixes.

## Global Constraints

- **Baseline:** `master` at `290af750671abf35342fc2c4ee131f0e0db89130` (after #12 and #13). Line numbers here refer to that tree, and edits anchor on quoted text, not line numbers (spec §1, RV5-L9).
- **Workspace:** a manual worktree made with plain `git worktree add ../Tov-learn-stage0 -b fix/stage0-quick-wins master`. **Never use `EnterWorktree`**: it conflicts with the user's redaction wrapper. uv creates the worktree's own `.venv`.
- **Commits and pushes happen only when the user asks.** In Task 0 Step 6, the session running this plan asks the user once whether they authorize its 22 commits. Without that yes, stop at each Commit step and ask. A subagent never commits or pushes. Pushing and opening the PR need a separate ask (Task 25). End every commit message with the attribution lines your session's system reminder specifies.
- **Dev loop (S20):** `uv run ruff check -q && uv run pytest -q`. When pytest is red, re-run `uv run pytest -v`. Use `uv run pytest --collect-only -q` for the PR's test IDs.
- **uv is required for contributors only (S12).** Learner-facing docs (README) never mention uv. CLAUDE.md's test section is labelled "contributors only".
- **Python:** `requires-python = ">=3.14,<3.15"` in `pyproject.toml`. CI passes `python-version: "3.14"` to setup-uv. **No `.python-version` file** anywhere (S13).
- **Lockfile:** generated with the CI-pinned uv: `uvx --from uv==0.12.19 uv lock` (RV2-L9).
- **Claude Code floor:** 2.1.176, a floor, not a pin (S14).
- **Scope:** `courses/_archive/` is out of scope throughout. Lints skip `_archive/` and `old_B*`.
- **One unit per file (D10):** this PR touches `learn.md` and all 15 `learn/*.md`. No other unit is open on them.
- **Hebrew:** replacement Hebrew matches the surrounding file's voice. A Hebrew-speaking contributor must approve it before merge (spec §4.2, §6.2).
- **Real learner data:** `/mnt/c/Users/Home/skill-tutor-tutorials` holds real Windows-side data. Never touch it. Manual checks run from WSL/Linux only.
- **Machine quirks:** `~/.bashrc:118` and `~/.profile:26` put `~/.local/bin` first on PATH in every tool shell, so PATH shims don't work. `~/.claude/settings.json` and `~/.claude/skills` are symlinks into `/mnt/c`. `~/.claude/commands` does not exist on this machine.
- **Memory:** this is a memory-constrained WSL2 VM that has OOM-crashed before. Run `free -h` at the start and before any subagent. If `available` drops below about 1.5 GB, tell the user it's time to wrap up and continue in a fresh session.

## Review Focus

These inputs are implied by the spec but not exercised by its seeds. Each has a pinned test in Task 1 (`REVIEW_FOCUS`, `test_git_tree_hebrew_file_name`, `test_worktree_git_file`), and each test was checked to fail when its protection is removed.

1. **Files saved by a Windows editor (UTF-8 BOM + CRLF).** A contributor on Windows saves an exercise whose first line is the `# ` heading. Expect no false `header_numbers` finding. `read()` uses `utf-8-sig`, and `splitlines()` handles CRLF.
2. **A module range typed with an ASCII hyphen (`0.1-0.2`).** Expect it to pass, as §5.1 says (`–`/`-` both accepted).
3. **A link to a file with a space, written `my%20notes.md`.** Expect it to resolve. The target is URL-decoded before the existence check.
4. **A tracked file with a Hebrew name.** Expect `git ls-files -z` to list it unquoted, and links to it to resolve.
5. **Running the suite from a git worktree, where `.git` is a file.** This is exactly how this plan is implemented. Expect `repo_files` to take the git path and ignore untracked files (RV5-L4).

---

## Conventions for every task

**Paths.** Run every command from the worktree root, `/home/emanresu/Tov-learn-stage0`, unless a step says otherwise. `SCRATCH` means your session's scratchpad directory (it's in your system prompt). Set it at the start of each Bash call that uses it, e.g. `SCRATCH=/tmp/claude-…/scratchpad` (shell variables don't survive between tool calls).

**The edit helper.** Content tasks run their edits through this helper. Each entry `(path, old, new)` or `(path, old, new, count)` must match `old` exactly `count` times (default 1). If any entry fails, **nothing is written** and the helper prints `ABORT, nothing written: …`. On an abort, stop and re-read the file. Don't loosen the entry. Create it once, in Task 0:

````python
"""All-or-nothing exact text edits for the Stage 0 plan.

Reads a Python literal list from stdin. Each entry is (path, old, new) or
(path, old, new, count): ``old`` must occur exactly ``count`` times (default 1)
at the moment the entry runs. Entries run in order, in memory; files are
written only if every entry matched. Line endings and a missing final
newline are preserved.
"""

import ast
import sys
from pathlib import Path

edits = ast.literal_eval(sys.stdin.read())
texts: dict[str, str] = {}
for entry in edits:
    path, old, new = entry[:3]
    count = entry[3] if len(entry) > 3 else 1
    if path not in texts:
        with open(path, encoding="utf-8", newline="") as f:
            texts[path] = f.read()
    found = texts[path].count(old)
    if found != count:
        sys.exit(f"ABORT, nothing written: {path}: want {count}x {old[:70]!r}, found {found}")
    texts[path] = texts[path].replace(old, new)
for path, text in texts.items():
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
print(f"OK: {len(edits)} edit(s) applied to {len(texts)} file(s)")
````

**Recovery (any failure mid-task).** The previous task is committed, so return this task's files to that commit, then rerun the task from Step 1. Run `git status --short`, then `git restore -- <each modified path it lists>`. Delete any file this task **created** (its `Create:` list) only after checking `git status` shows it as untracked (`??`). Never restore or delete a path outside the task's `Files:` list; if one shows up, stop and ask the user.

**The findings script.** After each task, count what the real-repo test would report. Create it once, in Task 0:

````python
"""Print every real-repo finding, then the count (run from the repo root)."""

import sys
from pathlib import Path

sys.path.insert(0, "tests")
import validate_structure as v  # noqa: E402

found = [f for check in v.CHECKS for f in check(Path("."))]
print("\n".join(found))
print(f"{len(found)} finding(s)")
````

Run it as `uv run python "$SCRATCH/findings.py"`. The last line is `N finding(s)`.

**Per-task loop.** Each task ends with the dev loop, `uv run ruff check -q && uv run pytest -q`. Until Task 14 (T5), the only allowed failure is `test_real_repo_passes`, and the findings count must equal the task's **Expected** line exactly. From Task 14 on, everything is green.

---

### Task 0: Workspace

**Files:** none in the repo. Creates the worktree, `$SCRATCH/apply_edits.py` and `$SCRATCH/findings.py`.

**Interfaces:**
- Produces: the worktree at `/home/emanresu/Tov-learn-stage0` on `fix/stage0-quick-wins`, and the two scratch scripts every later task uses.

- [ ] **Step 1: Check memory and the main checkout.**

```bash
free -h
cd /home/emanresu/Tov-learn && git status --short && git branch --show-current
```
Expected: `available` well above 1.5 GB, and a clean status. If the status isn't clean, stop and ask the user.

- [ ] **Step 2: Baseline guard (spec §1, RV2-H1, RV3-M6, RV5-M4).**

```bash
cd /home/emanresu/Tov-learn
git fetch origin
git rev-parse master origin/master
```
If the two SHAs differ, local `master` lags (expected once the docs PR has merged). Fast-forward it:
```bash
git switch master && git merge --ff-only origin/master
git rev-parse master origin/master
```
If `--ff-only` fails, local `master` has diverged. **Stop and ask the user.** Otherwise, the two SHAs must now be equal. Then:
```bash
if [ "$(git rev-parse origin/master)" = 290af750671abf35342fc2c4ee131f0e0db89130 ]; then
  echo "BASELINE EXACT"
else
  git diff --stat 290af75 origin/master -- . ':!docs'
fi
```
Expected: `BASELINE EXACT`, or **empty** output (only `docs/` changed, e.g. the docs PR). If the diff lists any file outside `docs/`, **stop**: re-verify every cited line and every `old` string in this plan against the new tip before editing, and tell the user.

- [ ] **Step 3: Create the worktree.** Plain git, never `EnterWorktree`.

```bash
cd /home/emanresu/Tov-learn
git worktree add ../Tov-learn-stage0 -b fix/stage0-quick-wins master
cd ../Tov-learn-stage0 && git status --short && git log --oneline -1
ls docs/superpowers/specs/2026-09-27-stage0-quick-wins-design.md docs/superpowers/plans/2026-09-29-stage0-quick-wins.md
```
Expected: clean status, and both docs present (the docs PR merged before this session).

- [ ] **Step 4: Create the two scratch scripts.** Write `$SCRATCH/apply_edits.py` and `$SCRATCH/findings.py` with exactly the contents under "Conventions" above.

- [ ] **Step 5: Check the toolchain.**

```bash
uv --version && uvx --from uv==0.12.19 uv --version && git --version
```
Expected: `uv 0.12.x` (local), then `uv 0.12.19`.

- [ ] **Step 6: Get commit authorization.** Ask the user once: "Do you authorize the plan's 22 commits on `fix/stage0-quick-wins` (no push)?" Record the answer. With a yes, every Commit step runs as written. Without one, stop at each Commit step and ask.

---

### Task 1 (P1): Toolchain, validator, tests, CI

**Files:**
- Create: `pyproject.toml`, `uv.lock`, `tests/test_validate_structure.py`, `.github/dependabot.yml`
- Rewrite: `tests/validate_structure.py` (the current file does its work at import time and calls `sys.exit`)
- Modify: `.gitignore`, `.github/workflows/validate.yml`

**Interfaces:**
- Produces: `validate_structure.CHECKS` (a tuple of 11 `check_<name>(root: Path) -> list[str]`), `check_spoken_lesson_refs(root, allowlist=SPOKEN_ALLOWLIST)`, `repo_files(root, pattern) -> list[Path]`, and finding strings shaped `path:line: [name] message`. Later tasks don't call these directly. They only watch the finding count.

- [ ] **Step 1: Write `pyproject.toml`** (spec §5.3, verbatim):

````toml
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
````

- [ ] **Step 2: Append to `.gitignore`:**

```bash
cat >> .gitignore <<'EOF'

# Contributor toolchain (uv / pytest / ruff)
.venv/
__pycache__/
.pytest_cache/
.ruff_cache/
EOF
```

- [ ] **Step 3: Lock with the CI-pinned uv, then sync.**

```bash
uvx --from uv==0.12.19 uv lock
uv sync --locked
grep -A1 -E '^name = "(pytest|ruff)"' uv.lock
```
Expected: `Resolved 8 packages`; `pytest` `9.1.1` and `ruff` `0.16.9`, or newer (the dev group sets floors, not pins; `uv.lock` pins what CI installs); `.venv/` created in the worktree. Confirm `ls .python-version` fails (no such file).

- [ ] **Step 4: Write the failing tests** to `tests/test_validate_structure.py`:

````python
"""Seeded regressions and must-pass negatives for validate_structure.

Every fixture test calls the checks through ``fixture_checks()``, which binds
``spoken_lesson_refs`` to the fixture's own allowlist. Only
``test_real_repo_passes`` uses the default ``SPOKEN_ALLOWLIST``.
"""

import shutil
import subprocess
from functools import partial
from pathlib import Path

import pytest
import validate_structure as vs

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURE_ALLOWLIST = (("0.1_script.txt", "גרסה שש נקודה שש"),)
M = "[מעבר שקף]"


def fixture_checks() -> dict:
    """Every check by short name, with spoken_lesson_refs bound to FIXTURE_ALLOWLIST."""
    checks = {}
    for check in vs.CHECKS:
        name = check.__name__.removeprefix("check_")
        if name == "spoken_lesson_refs":
            check = partial(check, allowlist=FIXTURE_ALLOWLIST)
        checks[name] = check
    return checks


def run_all(root: Path) -> dict[str, list[str]]:
    return {name: check(root) for name, check in fixture_checks().items()}


def script(first_line: str, extra: str = "") -> str:
    body = "\n".join(f"{M}\nקטע {n}." for n in range(1, 6))
    return f"{first_line}\nשלום וברוכים הבאים.\n\n{body}\n{extra}"


def exercises(number: str) -> str:
    return (
        '<div dir="rtl" lang="he">\n\n'
        f"# תרגילים - שיעור {number}: נושא\n\n"
        "## פרטי השיעור\n"
        f"- **שיעור:** {number} - נושא\n"
        "- **קורס:** Demo\n\n"
        "</div>\n"
    )


COURSE_MD = """\
# Demo

## מודולים

| מודול | תיקייה | שיעורים |
|-------|--------|---------|
| 00 — Basics | `00-basics/` | 0.1–0.2 |
| 02 — API | `02-api/` | 2.1–2.1 |
| 03 — Final | `03-final/` | — |

## רשימת שיעורים

| מספר | שם | סוג |
|------|----|-----|
| 0.1 | First | תיאורטי |
| 0.2 | Second | תיאורטי |
| 2.1 | API | מעשי |
"""

SETUP_MD = """\
# Setup Module

<!-- CLEAN-SLATE:BEGIN — TEMPORARY, remove at first-cohort gate (PRD D10) -->
## 0. Clean slate

```bash
: "${HOME:?HOME is not set}"
dest="$HOME/skill-tutor-tutorials-backup-$(date +%Y%m%d-%H%M%S)"
mkdir "$dest" || exit 1
mv "$HOME/skill-tutor-tutorials" "$dest/" || exit 1
```

```powershell
$dest = Join-Path $HOME "skill-tutor-tutorials-backup"
New-Item -ItemType Directory -Path $dest -ErrorAction Stop | Out-Null
Move-Item -LiteralPath (Join-Path $HOME "skill-tutor-tutorials") -Destination $dest -ErrorAction Stop
```
<!-- CLEAN-SLATE:END -->

## A. Show Current Settings
"""

LESSONS = "courses/demo/lessons"
S01 = f"{LESSONS}/00-basics/0.1-first/0.1_script.txt"
S02 = f"{LESSONS}/00-basics/0.2-second/0.2_script.txt"
S21 = f"{LESSONS}/02-api/2.1-api/2.1_script.txt"
E01 = f"{LESSONS}/00-basics/0.1-first/0.1_exercises.md"
E02 = f"{LESSONS}/00-basics/0.2-second/0.2_exercises.md"
E21 = f"{LESSONS}/02-api/2.1-api/2.1_exercises.md"
LEARN = ".claude/commands/learn.md"
TEACHING = ".claude/commands/learn/teaching.md"
SETUP = ".claude/commands/learn/setup.md"
SETTINGS = ".claude/settings.json"
COURSE = "courses/demo/COURSE.md"

GOOD_TREE = {
    COURSE: COURSE_MD,
    S01: script("שיעור 0.1 - הראשון", "גרסה שש נקודה שש יצאה השנה.\n"),
    E01: exercises("0.1"),
    S02: script("שיעור 0.2 - השני"),
    E02: exercises("0.2"),
    S21: script(
        "שיעור שתיים נקודה אחת - API", "בשיעור הקודם, אפס נקודה שתיים, ראינו.\n"
    ),
    E21: exercises("2.1"),
    f"{LESSONS}/03-final/projects.md": "# Projects\n",
    LEARN: (
        "# /learn\n\n"
        "| lesson | Read `.claude/commands/learn/teaching.md` |\n"
        "| quiz me | Read `.claude/commands/learn/quiz.md` |\n"
        "| setup | Read `.claude/commands/learn/setup.md` |\n"
    ),
    TEACHING: "# Teaching\n\n## Step 5 — End of Lesson\n\nRead `quiz.md` when asked.\n",
    ".claude/commands/learn/quiz.md": "# Quiz\n",
    SETUP: SETUP_MD,
    SETTINGS: "{}\n",
    "README.md": "# Demo\n\nSee the [course](courses/demo/COURSE.md).\n",
}


def write_tree(root: Path, files: dict[str, str]) -> None:
    for rel, text in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


@pytest.fixture
def good_tree(tmp_path: Path) -> Path:
    """A small valid repo on disk. Deliberately not a git repo."""
    write_tree(tmp_path, GOOD_TREE)
    return tmp_path


def replace(rel: str, old: str, new: str):
    def mutate(root: Path) -> None:
        path = root / rel
        text = path.read_text(encoding="utf-8")
        assert old in text, f"seed anchor {old!r} not in {rel}"
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    return mutate


def append(rel: str, text: str):
    def mutate(root: Path) -> None:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as f:
            f.write(text)

    return mutate


def overwrite(rel: str, text: str):
    def mutate(root: Path) -> None:
        (root / rel).write_text(text, encoding="utf-8")

    return mutate


def chain(*mutations):
    def mutate(root: Path) -> None:
        for m in mutations:
            m(root)

    return mutate


def delete(rel: str):
    def mutate(root: Path) -> None:
        (root / rel).unlink()

    return mutate


def test_good_tree_passes(good_tree: Path) -> None:
    assert run_all(good_tree) == {name: [] for name in fixture_checks()}


SEEDS = [
    # course_md
    ("course_md", "missing-row", replace(COURSE, "| 0.2 | Second | תיאורטי |\n", "")),
    (
        "course_md",
        "extra-row",
        replace(
            COURSE,
            "| 2.1 | API | מעשי |\n",
            "| 2.1 | API | מעשי |\n| 2.2 | Ghost | מעשי |\n",
        ),
    ),
    (
        "course_md",
        "swap",
        replace(
            COURSE,
            "| 0.1 | First | תיאורטי |\n| 0.2 | Second | תיאורטי |",
            "| 0.2 | Second | תיאורטי |\n| 0.1 | First | תיאורטי |",
        ),
    ),
    ("course_md", "wrong-range", replace(COURSE, "| 0.1–0.2 |", "| 0.1–0.3 |")),
    # slide_markers
    ("slide_markers", "four-markers", replace(S02, M, "")),
    ("slide_markers", "english-marker", append(S02, "[SLIDE TRANSITION]\n")),
    # header_numbers
    ("header_numbers", "numeric-5.1-in-2.1", replace(E21, "שיעור 2.1:", "שיעור 5.1:")),
    (
        "header_numbers",
        "bold-line-mismatch",
        replace(E21, "**שיעור:** 2.1", "**שיעור:** 2.2"),
    ),
    ("header_numbers", "script-0.1-in-0.2", replace(S02, "שיעור 0.2 -", "שיעור 0.1 -")),
    (
        "header_numbers",
        "spelled-existing-wrong-lesson",
        replace(S21, "שיעור שתיים נקודה אחת", "שיעור אפס נקודה אחת"),
    ),
    (
        "header_numbers",
        "unmapped-word",
        replace(S21, "שיעור שתיים נקודה אחת", "שיעור שתיים נקודה מאה"),
    ),
    # spoken_lesson_refs (seeds sit after line 3, so header_numbers never sees them)
    (
        "spoken_lesson_refs",
        "no-lesson-3.2",
        append(S01, "בשיעור שלוש נקודה שתיים נמשיך.\n"),
    ),
    ("spoken_lesson_refs", "prefixed", append(S01, "ראינו בשיעור ושלוש נקודה חמש.\n")),
    ("spoken_lesson_refs", "gendered", append(S01, "ראו שישה נקודה שבעה.\n")),
    ("spoken_lesson_refs", "hyphen-ordinal", append(S01, "בשיעור הבא, חמישי-ארבע.\n")),
    (
        "spoken_lesson_refs",
        "punctuation-does-not-hide",
        append(S01, "ראו שלוש נקודה שתיים, ואז נמשיך.\n"),
    ),
    (
        "spoken_lesson_refs",
        "stale-allowlist",
        replace(S01, "גרסה שש נקודה שש יצאה השנה.\n", ""),
    ),
    # course_name_denylist
    (
        "course_name_denylist",
        "course-name",
        append(S01, "ברוכים הבאים בקורס AI Engineer.\n"),
    ),
    (
        "course_name_denylist",
        "bold-course-line",
        replace(E01, "**קורס:** Demo", "**קורס:** AI Engineer"),
    ),
    (
        "course_name_denylist",
        "anon-key",
        append(E01, "NEXT_PUBLIC_SUPABASE_ANON_KEY=xyz\n"),
    ),
    # tutor_refs
    (
        "tutor_refs",
        "missing-route",
        append(LEARN, "| gone | Read `.claude/commands/learn/missing.md` |\n"),
    ),
    ("tutor_refs", "missing-bare-read", append(TEACHING, "Then Read `missing.md`.\n")),
    # settings_json
    (
        "settings_json",
        "powershell",
        overwrite(
            SETTINGS, '{"hooks": {"Stop": [{"command": "PowerShell -File x.ps1"}]}}\n'
        ),
    ),
    ("settings_json", "invalid-json", overwrite(SETTINGS, "{\n")),
    # relative_links
    (
        "relative_links",
        "missing-target",
        append("README.md", "\nSee [missing](docs/missing.md).\n"),
    ),
    # clean_slate_no_delete
    (
        "clean_slate_no_delete",
        "rm-rf",
        replace(
            SETUP, 'mkdir "$dest" || exit 1', 'rm -rf "$dest"; mkdir "$dest" || exit 1'
        ),
    ),
    (
        "clean_slate_no_delete",
        "remove-item",
        replace(SETUP, "Move-Item -LiteralPath", "Remove-Item -LiteralPath"),
    ),
    (
        "clean_slate_no_delete",
        "remove-item-lower",
        replace(SETUP, "Move-Item -LiteralPath", "remove-item -LiteralPath"),
    ),
    (
        "clean_slate_no_delete",
        "dotnet-delete",
        replace(
            SETUP,
            "New-Item -ItemType",
            "[IO.Directory]::Delete($dest); New-Item -ItemType",
        ),
    ),
    (
        "clean_slate_no_delete",
        "end-marker-missing",
        replace(SETUP, "<!-- CLEAN-SLATE:END -->\n", ""),
    ),
    # lesson_files
    ("lesson_files", "missing-exercises", delete(E02)),
    # teaching_step5
    ("teaching_step5", "step5-removed", replace(TEACHING, "Step 5", "Step 4")),
]


@pytest.mark.parametrize(
    ("check", "mutate"),
    [(c, m) for c, _, m in SEEDS],
    ids=[f"{c}-{i}" for c, i, _ in SEEDS],
)
def test_seeded_regression_fails_only_its_check(
    good_tree: Path, check: str, mutate
) -> None:
    mutate(good_tree)
    results = run_all(good_tree)
    assert results[check], f"{check} did not catch the seed"
    others = {name: found for name, found in results.items() if name != check and found}
    assert not others, f"other checks fired: {others}"


NEGATIVES = [
    ("job-title", append(S01, "תפקיד ה-AI Engineer מבוקש. AI Engineer הוא תפקיד.\n")),
    (
        "archive-denied",
        append(
            "courses/_archive/old/lessons/00-x/0.1-x/0.1_script.txt",
            "בקורס AI Engineer\n[x](missing.md)\n",
        ),
    ),
    (
        "old-b-denied",
        append(
            f"{LESSONS}/03-final/old_B-x.md",
            "בקורס AI Engineer\nNEXT_PUBLIC_SUPABASE_ANON_KEY\n[x](missing.md)\n",
        ),
    ),
    ("home-path", append(TEACHING, "Save to `~/skill-tutor-tutorials/progress/`.\n")),
    ("local-only", append(TEACHING, "Never touch `.claude/settings.local.json`.\n")),
    ("skill-dir", append(TEACHING, "Read `${CLAUDE_SKILL_DIR}/x.md` later.\n")),
    ("already", append(TEACHING, "If it was already `x.md`, skip it.\n")),
    ("load-from", append(TEACHING, "Load the list from `projects.md`.\n")),
    (
        "http-and-anchor",
        append(
            "README.md",
            "[a](https://example.com) [b](http://example.com) [c](#usage) [d](mailto:a@b.c)\n",
        ),
    ),
    (
        "fenced-link",
        append(
            "README.md",
            "\n```\n[x](missing.md)\n```\n\n````md\n```\n[y](missing.md)\n```\n````\n",
        ),
    ),
    ("inline-code-link", append("README.md", "Write `[x](missing.md)` to link.\n")),
    (
        "punctuation",
        append(S02, "ראינו אפס נקודה אחת, אפס נקודה אחת: ואפס נקודה אחת.\n"),
    ),
    (
        "allowlisted-and-existing",
        append(S01, "שוב גרסה שש נקודה שש, ובשיעור אפס נקודה שתיים.\n"),
    ),
    (
        "verbs-inside-words",
        replace(
            SETUP,
            "## 0. Clean slate\n",
            "## 0. Clean slate\n\nConfirm the model, then perform the move.\n",
        ),
    ),
    ("rm-outside-markers", append(SETUP, "\nThe old flow ran `rm -rf` here.\n")),
    ("missing-settings", delete(SETTINGS)),
]


@pytest.mark.parametrize(
    "mutate", [m for _, m in NEGATIVES], ids=[i for i, _ in NEGATIVES]
)
def test_must_pass_negative(good_tree: Path, mutate) -> None:
    mutate(good_tree)
    assert run_all(good_tree) == {name: [] for name in fixture_checks()}


def git_repo(path: Path):
    return partial(subprocess.run, cwd=path, check=True, capture_output=True)


@pytest.mark.skipif(shutil.which("git") is None, reason="git not installed")
def test_git_tree_ignores_untracked_files(good_tree: Path, tmp_path_factory) -> None:
    root = tmp_path_factory.mktemp("git") / "repo"
    shutil.copytree(good_tree, root)
    git = git_repo(root)
    git(["git", "init", "-q"])
    git(["git", "add", "-A"])
    (root / "broken.md").write_text("[x](missing.md)\n", encoding="utf-8")
    assert vs.check_relative_links(root) == []
    git(["git", "add", "broken.md"])
    assert vs.check_relative_links(root) == [
        "broken.md:1: [relative_links] link target 'missing.md' does not exist"
    ]


def windows_saved(rel: str):
    """Rewrite ``rel`` the way a Windows editor may save it: BOM + CRLF."""

    def mutate(root: Path) -> None:
        path = root / rel
        text = path.read_text(encoding="utf-8").replace("\n", "\r\n")
        path.write_bytes(b"\xef\xbb\xbf" + text.encode("utf-8"))

    return mutate


# Review Focus: inputs the spec implies but its seeds never exercise.
H1_FIRST = "# תרגילים - שיעור 2.1: נושא\n\n- **שיעור:** 2.1 - נושא\n"
REVIEW_FOCUS = [
    ("bom-crlf-h1-on-line-1", chain(overwrite(E21, H1_FIRST), windows_saved(E21))),
    ("bom-crlf-script", windows_saved(S21)),
    ("bom-crlf-course-md", windows_saved(COURSE)),
    ("ascii-hyphen-range", replace(COURSE, "| 0.1–0.2 |", "| 0.1-0.2 |")),
    (
        "percent-encoded-link",
        chain(
            append("docs/my notes.md", "# Notes\n"),
            append("README.md", "[notes](docs/my%20notes.md)\n"),
        ),
    ),
]


@pytest.mark.parametrize(
    "mutate", [m for _, m in REVIEW_FOCUS], ids=[i for i, _ in REVIEW_FOCUS]
)
def test_review_focus_passes(good_tree: Path, mutate) -> None:
    mutate(good_tree)
    assert run_all(good_tree) == {name: [] for name in fixture_checks()}


@pytest.mark.skipif(shutil.which("git") is None, reason="git not installed")
def test_git_tree_hebrew_file_name(good_tree: Path, tmp_path_factory) -> None:
    root = tmp_path_factory.mktemp("heb") / "repo"
    shutil.copytree(good_tree, root)
    append("docs/מדריך.md", "[back](../README.md)\n")(root)
    append("README.md", "[guide](docs/מדריך.md)\n")(root)
    git = git_repo(root)
    git(["git", "init", "-q"])
    git(["git", "add", "-A"])
    assert Path("docs/מדריך.md") in vs.repo_files(root, "**/*.md")
    assert run_all(root) == {name: [] for name in fixture_checks()}


@pytest.mark.skipif(shutil.which("git") is None, reason="git not installed")
def test_worktree_git_file(good_tree: Path, tmp_path_factory) -> None:
    base = tmp_path_factory.mktemp("wt")
    main = base / "main"
    shutil.copytree(good_tree, main)
    git = git_repo(main)
    git(["git", "init", "-q"])
    git(["git", "add", "-A"])
    ident = ["-c", "user.name=t", "-c", "user.email=t@example.com"]
    git(["git", *ident, "commit", "-q", "-m", "init"])
    git(["git", "worktree", "add", "-q", str(base / "wt")])
    wt = base / "wt"
    assert (wt / ".git").is_file()
    (wt / "untracked.md").write_text("[x](missing.md)\n", encoding="utf-8")
    assert run_all(wt) == {name: [] for name in fixture_checks()}


def test_real_repo_passes() -> None:
    findings = [f for check in vs.CHECKS for f in check(REPO_ROOT)]
    assert not findings, f"{len(findings)} finding(s):\n" + "\n".join(findings)
````

- [ ] **Step 5: Run them and watch them fail.**

```bash
uv run pytest -q
```
Expected: `58 failed`, every one with `AttributeError: module 'validate_structure' has no attribute …` (`CHECKS` or a `check_*` name). The old script passes on this tree, so importing it runs its checks and prints `PASSED`, but doesn't exit. This proves the tests exercise the new module.

- [ ] **Step 6: Replace `tests/validate_structure.py`** with:

````python
"""Structural checks for Tov-learn, run through pytest.

Each check is ``check_<name>(root: Path) -> list[str]`` and returns findings
formatted ``path:line: [name] message``. An empty list means the check passes.
``CHECKS`` lists every check. This module does no work at import time.

Contributors run: ``uv run ruff check -q && uv run pytest -q``
"""

import json
import re
import subprocess
from fnmatch import fnmatch
from pathlib import Path, PurePosixPath
from urllib.parse import unquote

# --- shared helpers ---------------------------------------------------------

SKIP_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache"}


def repo_files(root: Path, pattern: str) -> list[Path]:
    """Repo-relative paths matching ``pattern`` (``PurePath.full_match`` syntax).

    Uses ``git ls-files -z`` when ``root/.git`` exists (a directory in a clone,
    a file in a worktree), so local runs see what CI sees. Tracked entries
    missing on disk are skipped. Otherwise walks the filesystem.
    """
    if (root / ".git").exists():
        cmd = ["git", "-C", str(root), "ls-files", "-z"]
        out = subprocess.run(cmd, capture_output=True, check=True).stdout
        rels = [PurePosixPath(p) for p in out.decode("utf-8").split("\0") if p]
        rels = [r for r in rels if (root / r).is_file()]
    else:
        rels = []
        for p in root.rglob("*"):
            rel = p.relative_to(root)
            if p.is_file() and not SKIP_DIRS.intersection(rel.parts):
                rels.append(PurePosixPath(rel.as_posix()))
    return sorted(Path(r) for r in rels if r.full_match(pattern))


def finding(check: str, rel: Path, line: int, message: str) -> str:
    return f"{rel.as_posix()}:{line}: [{check}] {message}"


def read(root: Path, rel: Path) -> str:
    """Read UTF-8 text; ``utf-8-sig`` drops a BOM that Windows editors add."""
    return (root / rel).read_text(encoding="utf-8-sig")


def in_course_scope(rel: Path) -> bool:
    """Under ``courses/<course>/``, but not ``courses/_archive/`` or ``old_B*``."""
    parts = rel.parts
    return (
        len(parts) >= 3
        and parts[0] == "courses"
        and parts[1] != "_archive"
        and not rel.name.startswith("old_B")
    )


def course_files(root: Path, suffix: str) -> list[Path]:
    files = repo_files(root, f"courses/**/*{suffix}")
    return [r for r in files if in_course_scope(r)]


def course_dirs(root: Path) -> list[Path]:
    courses = root / "courses"
    if not courses.is_dir():
        return []
    return sorted(d for d in courses.iterdir() if d.is_dir() and d.name != "_archive")


LESSON_DIR = re.compile(r"^(\d+)\.(\d+)-")


def lesson_key(number: str) -> tuple[int, int]:
    major, minor = number.split(".")
    return int(major), int(minor)


def lesson_dirs(course: Path) -> list[Path]:
    """Every folder at ``lessons/<module>/<lesson>/``."""
    lessons = course / "lessons"
    if not lessons.is_dir():
        return []
    modules = sorted(p for p in lessons.iterdir() if p.is_dir())
    return [d for m in modules for d in sorted(m.iterdir()) if d.is_dir()]


def lesson_folders(course: Path) -> dict[str, Path]:
    """Lesson number ("2.1") -> folder, for folders named ``<X.Y>-*``."""
    found = {}
    for d in lesson_dirs(course):
        if m := LESSON_DIR.match(d.name):
            found[f"{m[1]}.{m[2]}"] = d
    return found


def folder_number(rel: Path) -> str | None:
    m = LESSON_DIR.match(rel.parent.name)
    return f"{m[1]}.{m[2]}" if m else None


# Spoken Hebrew digits, as the scripts use them ("שתיים נקודה אחת" = 2.1).
DIGIT_WORDS = {
    "אפס": 0,
    "אחת": 1, "אחד": 1,
    "שתיים": 2, "שניים": 2, "שתים": 2,
    "שלוש": 3, "שלושה": 3,
    "ארבע": 4, "ארבעה": 4,
    "חמש": 5, "חמישה": 5,
    "שש": 6, "שישה": 6,
    "שבע": 7, "שבעה": 7,
    "שמונה": 8,
    "תשע": 9, "תשעה": 9,
}  # fmt: skip
ORDINALS = {
    "ראשון": 1, "שני": 2, "שלישי": 3, "רביעי": 4,
    "חמישי": 5, "שישי": 6, "שביעי": 7, "שמיני": 8,
}  # fmt: skip
PREFIXES = "ובלשהמכ"


def digit_value(word: str) -> int | None:
    """Map a spoken digit, stripping at most one leading prefix letter."""
    if word in DIGIT_WORDS:
        return DIGIT_WORDS[word]
    if len(word) > 1 and word[0] in PREFIXES:
        return DIGIT_WORDS.get(word[1:])
    return None


# --- checks -----------------------------------------------------------------

ROW = re.compile(r"^\|(.+)\|$")


def table_rows(lines: list[str], heading: str) -> list[tuple[int, list[str]]]:
    """Data rows (1-based line, cells) of the table under the ``heading`` title."""
    rows, inside = [], False
    for i, line in enumerate(lines, 1):
        if line.startswith("#"):
            if inside:
                break
            inside = line.lstrip("#").strip() == heading
        elif inside and (m := ROW.match(line.strip())):
            cells = [c.strip() for c in m[1].split("|")]
            if not all(set(c) <= set("-: ") for c in cells):
                rows.append((i, cells))
    return rows


def module_range(folders: dict[str, Path], module: Path) -> str:
    nums = sorted((n for n, d in folders.items() if d.parent == module), key=lesson_key)
    return f"{nums[0]}–{nums[-1]}" if nums else "—"


def check_course_md(root: Path) -> list[str]:
    out = []
    for course in course_dirs(root):
        rel = (course / "COURSE.md").relative_to(root)
        if not (root / rel).is_file():
            continue
        lines = read(root, rel).splitlines()
        folders = lesson_folders(course)
        rows = [
            (i, cells[0])
            for i, cells in table_rows(lines, "רשימת שיעורים")
            if re.fullmatch(r"\d+\.\d+", cells[0])
        ]
        listed = [n for _, n in rows]
        head = next((i for i, ln in enumerate(lines, 1) if "רשימת שיעורים" in ln), 1)
        for n in sorted(set(folders) - set(listed), key=lesson_key):
            out.append(finding("course_md", rel, head, f"lesson {n} has no row"))
        for i, n in rows:
            if n not in folders:
                out.append(finding("course_md", rel, i, f"row {n} has no folder"))
        if listed != sorted(listed, key=lesson_key):
            msg = f"rows out of numeric order: {', '.join(listed)}"
            out.append(finding("course_md", rel, head, msg))
        for i, cells in table_rows(lines, "מודולים"):
            m = re.search(r"`([^`]+)`", cells[1]) if len(cells) >= 3 else None
            if not m:
                continue
            module = course / "lessons" / m[1].rstrip("/")
            if not module.is_dir():
                out.append(finding("course_md", rel, i, f"no folder {m[1]}"))
            elif cells[2].replace("-", "–") != (want := module_range(folders, module)):
                msg = f"range {cells[2]!r} for {m[1]}, expected {want!r}"
                out.append(finding("course_md", rel, i, msg))
    return out


def check_slide_markers(root: Path) -> list[str]:
    out = []
    for rel in course_files(root, "_script.txt"):
        lines = read(root, rel).splitlines()
        count = sum(ln.count("[מעבר שקף]") for ln in lines)
        if count < 5:
            msg = f"{count} [מעבר שקף] markers, need at least 5"
            out.append(finding("slide_markers", rel, 1, msg))
        english = [i for i, ln in enumerate(lines, 1) if "[SLIDE TRANSITION]" in ln]
        if english:
            msg = f"{len(english)} [SLIDE TRANSITION] line(s); use [מעבר שקף]"
            out.append(finding("slide_markers", rel, english[0], msg))
    return out


NUMERIC_LESSON = re.compile(r"(?:שיעור|Lesson)\s+(\d+\.\d+)")
SPELLED_LESSON = re.compile(r"שיעור\s+([א-ת]+)\s+נקודה\s+([א-ת]+)")
BOLD_LESSON = re.compile(r"\*\*שיעור:\*\*\s*(\d+\.\d+)?")


def exercise_headers(rel: Path, lines: list[str], want: str) -> list[str]:
    out = []
    h1 = next(((i, ln) for i, ln in enumerate(lines, 1) if ln.startswith("# ")), None)
    m = re.search(r"שיעור\s+(\d+\.\d+)", h1[1]) if h1 else None
    if not m or m[1] != want:
        msg = f"first heading names {m[1] if m else 'no lesson'}, folder is {want}"
        out.append(finding("header_numbers", rel, h1[0] if h1 else 1, msg))
    for i, ln in enumerate(lines, 1):
        if (b := BOLD_LESSON.search(ln)) and b[1] != want:
            msg = f"**שיעור:** names {b[1] or 'no lesson'}, folder is {want}"
            out.append(finding("header_numbers", rel, i, msg))
    return out


def script_opening(rel: Path, lines: list[str], want: str) -> list[str]:
    out = []
    opening = [(i, ln) for i, ln in enumerate(lines, 1) if ln.strip()][:3]
    for i, ln in opening:
        for m in NUMERIC_LESSON.finditer(ln):
            if m[1] != want:
                msg = f"opening names {m[1]}, folder is {want}"
                out.append(finding("header_numbers", rel, i, msg))
        for m in SPELLED_LESSON.finditer(ln):
            x, y = DIGIT_WORDS.get(m[1]), DIGIT_WORDS.get(m[2])
            if x is None or y is None:
                msg = f"unmapped spoken number {m[0]!r}"
                out.append(finding("header_numbers", rel, i, msg))
            elif f"{x}.{y}" != want:
                msg = f"opening names {x}.{y}, folder is {want}"
                out.append(finding("header_numbers", rel, i, msg))
    return out


def check_header_numbers(root: Path) -> list[str]:
    out = []
    for rel in course_files(root, "_exercises.md"):
        if want := folder_number(rel):
            out += exercise_headers(rel, read(root, rel).splitlines(), want)
    for rel in course_files(root, "_script.txt"):
        if want := folder_number(rel):
            out += script_opening(rel, read(root, rel).splitlines(), want)
    return out


# (file-name glob, exact phrase): spelled numbers that are not lesson numbers.
SPOKEN_ALLOWLIST = (
    ("0.3_script.txt", "ושבע נקודה אחת אחוז"),
    ("1.1_script.txt", "ארבע נקודה שש"),
    ("1.1_script.txt", "שש נקודה שש מיליארד"),
    ("1.5_script.txt", "שישה נקודה שישה מיליארד"),
    ("2.1_script.txt", "שתיים נקודה אפס"),
    ("2.5_script.txt", "שלוש נקודה שלוש עשרה"),
    ("2.5_script.txt", "שלוש נקודה ארבע עשרה"),
    ("2.5_script.txt", "ארבע נקודה שבע"),
)
SPOKEN_DOT = re.compile(r"(?<![א-ת])([א-ת]+)\s+נקודה\s+([א-ת]+)")
HYPHEN_ORDINAL = re.compile(r"(" + "|".join(ORDINALS) + r")-([א-ת]+)")


def spoken_refs(line: str) -> list[tuple[re.Match, str]]:
    """Every spelled lesson-number form in ``line``, with its ``X.Y``."""
    refs = []
    for m in SPOKEN_DOT.finditer(line):
        x, y = digit_value(m[1]), digit_value(m[2])
        if x is not None and y is not None:
            refs.append((m, f"{x}.{y}"))
    for m in HYPHEN_ORDINAL.finditer(line):
        if (y := digit_value(m[2])) is not None:
            refs.append((m, f"{ORDINALS[m[1]]}.{y}"))
    return refs


def check_spoken_lesson_refs(root: Path, allowlist=SPOKEN_ALLOWLIST) -> list[str]:
    out = []
    files = course_files(root, "_script.txt") + course_files(root, "_exercises.md")
    texts = {rel: read(root, rel) for rel in files}
    for glob, phrase in allowlist:
        matching = [rel for rel in files if fnmatch(rel.name, glob)]
        if matching and not any(phrase in texts[rel] for rel in matching):
            msg = f"stale allowlist entry ({glob!r}, {phrase!r})"
            out.append(finding("spoken_lesson_refs", matching[0], 1, msg))
    lessons = {c.name: set(lesson_folders(c)) for c in course_dirs(root)}
    for rel in files:
        existing = lessons.get(rel.parts[1], set())
        phrases = [p for g, p in allowlist if fnmatch(rel.name, g)]
        for i, ln in enumerate(texts[rel].splitlines(), 1):
            spans = [
                (a.start(), a.end())
                for p in phrases
                for a in re.finditer(re.escape(p), ln)
            ]
            for m, number in spoken_refs(ln):
                allowed = any(s <= m.start() and m.end() <= e for s, e in spans)
                if number not in existing and not allowed:
                    msg = f"{m[0]!r} names lesson {number}, which does not exist"
                    out.append(finding("spoken_lesson_refs", rel, i, msg))
    return out


DENYLIST = (
    re.compile(r"קורס\s+(ה-)?AI Engineer", re.IGNORECASE),
    re.compile(r"\*\*קורס:\*\*\s*AI Engineer", re.IGNORECASE),
    re.compile(r"AI Engineer course", re.IGNORECASE),
    re.compile(r"NEXT_PUBLIC_SUPABASE_ANON_KEY"),
)


def check_course_name_denylist(root: Path) -> list[str]:
    out = []
    for rel in course_files(root, ".md") + course_files(root, ".txt"):
        for i, ln in enumerate(read(root, rel).splitlines(), 1):
            for pattern in DENYLIST:
                if m := pattern.search(ln):
                    msg = f"denied string {m[0]!r}"
                    out.append(finding("course_name_denylist", rel, i, msg))
    return out


LOCAL_ONLY = {".claude/settings.local.json"}
BACKTICKED = re.compile(r"`([^`\n]+)`")
READ_BARE = re.compile(r"\b(?:read|load)\b\s+`([^`/\s]+\.md)`", re.IGNORECASE)
PLACEHOLDER = re.compile(r"[\[{*]|X\.Y")


def check_tutor_refs(root: Path) -> list[str]:
    out = []
    for rel in repo_files(root, ".claude/**/*.md"):
        for i, ln in enumerate(read(root, rel).splitlines(), 1):
            for m in BACKTICKED.finditer(ln):
                path = m[1].strip()
                if not path.startswith((".claude/", "courses/")):
                    continue
                if PLACEHOLDER.search(path) or path in LOCAL_ONLY:
                    continue
                if not (root / path).exists():
                    out.append(
                        finding("tutor_refs", rel, i, f"`{path}` does not exist")
                    )
            for m in READ_BARE.finditer(ln):
                if PLACEHOLDER.search(m[1]) or (root / rel.parent / m[1]).exists():
                    continue
                msg = f"`{m[1]}` not found next to {rel.name}"
                out.append(finding("tutor_refs", rel, i, msg))
    return out


def check_settings_json(root: Path) -> list[str]:
    rel = Path(".claude/settings.json")
    if not (root / rel).is_file():
        return []
    text = read(root, rel)
    try:
        json.loads(text)
    except json.JSONDecodeError as e:
        return [finding("settings_json", rel, e.lineno, f"invalid JSON: {e.msg}")]
    msg = "mentions powershell; hooks must run on every OS"
    lines = enumerate(text.splitlines(), 1)
    return [
        finding("settings_json", rel, i, msg)
        for i, ln in lines
        if "powershell" in ln.lower()
    ]


FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
INLINE_CODE = re.compile(r"(`+)(?!`).*?(?<!`)\1(?!`)")
MD_LINK = re.compile(r"\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+[\"'][^)]*[\"'])?\s*\)")


def prose_lines(text: str) -> list[str]:
    """Lines with fenced blocks blanked and inline code spans removed.

    A fence closes only on a line of the same character, at least as long as
    the opener, with nothing after it (CommonMark), so ```` blocks can hold ```.
    """
    out, fence = [], None
    for ln in text.splitlines():
        m = FENCE.match(ln)
        if fence is None and not m:
            out.append(INLINE_CODE.sub("", ln))
            continue
        if fence is None:
            fence = m[1]
        elif m and m[1][0] == fence[0] and len(m[1]) >= len(fence) and not m[2].strip():
            fence = None
        out.append("")
    return out


def check_relative_links(root: Path) -> list[str]:
    out = []
    for rel in repo_files(root, "**/*.md"):
        if "_archive" in rel.parts or rel.name.startswith("old_B"):
            continue
        for i, ln in enumerate(prose_lines(read(root, rel)), 1):
            for m in MD_LINK.finditer(ln):
                target = m[1]
                if target.startswith(("http:", "https:", "mailto:", "#")):
                    continue
                path = unquote(target.split("#", 1)[0])
                if path and not (root / rel.parent / path).exists():
                    msg = f"link target {target!r} does not exist"
                    out.append(finding("relative_links", rel, i, msg))
    return out


CLEAN_BEGIN = "<!-- CLEAN-SLATE:BEGIN"
CLEAN_END = "<!-- CLEAN-SLATE:END -->"
DELETE_VERBS = re.compile(
    r"\brm\b|\brmdir\b|\bdel\b|\berase\b|\brd\b|\bri\b|Remove-Item|\bunlink\b"
    r"|-delete\b|rmtree|::Delete\(",
    re.IGNORECASE,
)


def check_clean_slate_no_delete(root: Path) -> list[str]:
    """TEMPORARY: removed with the CLEAN-SLATE section at the gate (PRD D10)."""
    rel = Path(".claude/commands/learn/setup.md")
    lines = read(root, rel).splitlines() if (root / rel).is_file() else []
    begin = next((i for i, ln in enumerate(lines) if CLEAN_BEGIN in ln), None)
    end = next((i for i, ln in enumerate(lines) if CLEAN_END in ln), None)
    if begin is None or end is None or end < begin:
        msg = "CLEAN-SLATE:BEGIN/END markers missing or out of order"
        return [finding("clean_slate_no_delete", rel, 1, msg)]
    return [
        finding("clean_slate_no_delete", rel, i + 1, f"delete command {m[0]!r}")
        for i in range(begin + 1, end)
        for m in DELETE_VERBS.finditer(lines[i])
    ]


def check_lesson_files(root: Path) -> list[str]:
    out = []
    for course in course_dirs(root):
        for d in lesson_dirs(course):
            for pattern in ("*_script.txt", "*_exercises.md"):
                if not list(d.glob(pattern)):
                    rel = d.relative_to(root)
                    out.append(finding("lesson_files", rel, 1, f"missing {pattern}"))
    return out


def check_teaching_step5(root: Path) -> list[str]:
    rel = Path(".claude/commands/learn/teaching.md")
    if (root / rel).is_file() and "Step 5" in read(root, rel):
        return []
    return [finding("teaching_step5", rel, 1, "missing 'Step 5 — End of Lesson'")]


CHECKS = (
    check_course_md,
    check_slide_markers,
    check_header_numbers,
    check_spoken_lesson_refs,
    check_course_name_denylist,
    check_tutor_refs,
    check_settings_json,
    check_relative_links,
    check_clean_slate_no_delete,
    check_lesson_files,
    check_teaching_step5,
)
````

- [ ] **Step 7: Run the dev loop.**

```bash
uv run ruff check -q && uv run pytest -q
```
Expected: ruff prints nothing (exit 0); pytest reports `1 failed, 57 passed`, and the one failure is `test_real_repo_passes`. Then:
```bash
uv run python "$SCRATCH/findings.py" | tail -1
uv run pytest --collect-only -q | tail -1
```
Expected: `85 finding(s)` and `58 tests collected`. The 85 are: `header_numbers` 38, `spoken_lesson_refs` 33, `course_name_denylist` 7, `course_md` 3, `slide_markers` 2, `settings_json` 1, `clean_slate_no_delete` 1. The 38 + 33 + 6 header, spoken and course-name findings are exactly the spec's §4.2 inventory. The other 8 are items 1 (`course_md`), 2 (`settings_json`), 4 (`slide_markers`), 14 (`clean_slate_no_delete`) and 16 (the `NEXT_PUBLIC_SUPABASE_ANON_KEY` denylist line). If the count differs, stop and compare against the inventory before going on.

- [ ] **Step 8: Replace `.github/workflows/validate.yml`** (spec §5.4, verbatim):

````yaml
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
````

- [ ] **Step 9: Create `.github/dependabot.yml`** (spec §5.4, verbatim):

````yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
````

- [ ] **Step 10: Commit.** The message lists the red findings (spec §6.1).

```bash
SCRATCH=…  # your scratchpad
uv run python "$SCRATCH/findings.py" > "$SCRATCH/p1-findings.txt"
{
  echo "ci: uv + pytest + ruff toolchain and Stage 0 structural lints"
  echo
  echo "Rewrites tests/validate_structure.py as a library of check_* functions,"
  echo "tested by tests/test_validate_structure.py (seeded regressions, must-pass"
  echo "negatives, and the real repo). validate.yml moves to SHA-pinned node24"
  echo "actions (checkout v7.0.1, setup-uv v10.2.0) with contents: read; Dependabot"
  echo "tracks github-actions weekly."
  echo
  echo "test_real_repo_passes is red until groups C, T and D land. Red findings:"
  echo
  cat "$SCRATCH/p1-findings.txt"
  echo
  # then the attribution lines from your session's system reminder
} > "$SCRATCH/p1-msg.txt"
git add pyproject.toml uv.lock .gitignore tests/validate_structure.py tests/test_validate_structure.py .github/workflows/validate.yml .github/dependabot.yml
git commit -F "$SCRATCH/p1-msg.txt"
```

---

### Task 2 (P2): Drop the PowerShell Stop hook (item 2)

**Files:** Modify `.claude/settings.json`. Keep `.claude/scripts/auto-save-progress.ps1`; unit M removes it.

- [ ] **Step 1: Replace the file:**

````bash
printf '{}\n' > .claude/settings.json
cat .claude/settings.json
````

- [ ] **Step 2: Verify.** Run the dev loop, then `uv run python "$SCRATCH/findings.py" | tail -1`. **Expected: `84 finding(s)`**, with no `settings_json` line.

- [ ] **Step 3: Commit.** `git add .claude/settings.json && git commit -m "fix(settings): remove the PowerShell Stop hook"` (plus attribution).

---

### Task 3 (C): `COURSE.md` lists 2.1 and 2.2 (item 1)

**Files:** Modify `courses/ai-dev/COURSE.md`.

- [ ] **Step 1: Apply the edits:**

````bash
SCRATCH=…  # your scratchpad
uv run python "$SCRATCH/apply_edits.py" <<'EOF'
[
    (
        'courses/ai-dev/COURSE.md',
        '| 02 — Claude API | `02-claude-api/` | 2.3–2.6 |',
        '| 02 — Claude API | `02-claude-api/` | 2.1–2.6 |',
    ),
    (
        'courses/ai-dev/COURSE.md',
        '| 2.3 | Webhooks | מעשי |',
        '''| 2.1 | מהו API | מעשי |
| 2.2 | עבודה עם API של Claude, OpenAI ו-Gemini | מעשי |
| 2.3 | Webhooks | מעשי |''',
    ),
]
EOF
````

- [ ] **Step 2: Verify.** Dev loop, then findings. **Expected: `81 finding(s)`**, with no `course_md` line.

- [ ] **Step 3: Commit.** `git add courses/ai-dev/COURSE.md && git commit -m "fix(course): list lessons 2.1 and 2.2 in COURSE.md"`

---

### Task 4 (C): VAT 17% → 18% (item 3; seven occurrences, RV-M2, RV2-M1)

**Files:** Modify `1.3_exercises.md`, `2.2_exercises.md` and `2.6_script.txt`.

- [ ] **Step 1: Apply the edits:**

````bash
SCRATCH=…  # your scratchpad
uv run python "$SCRATCH/apply_edits.py" <<'EOF'
[
    (
        'courses/ai-dev/lessons/01-claude-code/1.3-claude-md-memory-skills/1.3_exercises.md',
        'המע"מ הוא כרגע 17%.',
        'המע"מ הוא כרגע 18%.',
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.2-claude-openai-gemini-api/2.2_exercises.md',
        'כולל מע"מ (17%).',
        'כולל מע"מ (18%).',
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.2-claude-openai-gemini-api/2.2_exercises.md',
        'המחיר כולל 17% מע"מ.',
        'המחיר כולל 18% מע"מ.',
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.2-claude-openai-gemini-api/2.2_exercises.md',
        'including 17% VAT.',
        'including 18% VAT.',
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.2-claude-openai-gemini-api/2.2_exercises.md',
        'vat_rate = 0.17',
        'vat_rate = 0.18',
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.2-claude-openai-gemini-api/2.2_exercises.md',
        'מעמ בשיעור 17%.',
        'מעמ בשיעור 18%.',
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.6-mcp/2.6_script.txt',
        'שבעה עשר אחוז',
        'שמונה עשר אחוז',
    ),
]
EOF
````

- [ ] **Step 2: Completion grep (spec §4.2).**

```bash
grep -rnE "17%|0\.17|שבעה עשר" courses/ai-dev
```
Expected: no output. `courses/ai-dev` contains no `_archive/`.

- [ ] **Step 3: Verify.** Dev loop and findings. **Expected: `81 finding(s)`** (VAT isn't linted).

- [ ] **Step 4: Commit.** `git add -u courses/ai-dev && git commit -m "fix(content): Israeli VAT is 18%, not 17%"`

---

### Task 5 (C): 0.4 slide markers (item 4)

**Files:** Modify `0.4_script.txt`. Only the markers change here. Task 6 fixes 0.4's title, "Lesson 0.3" and the course line.

- [ ] **Step 1: Apply the edits:**

````bash
SCRATCH=…  # your scratchpad
uv run python "$SCRATCH/apply_edits.py" <<'EOF'
[
    (
        'courses/ai-dev/lessons/00-ai-fundamentals/0.4-prompt-engineering/0.4_script.txt',
        '[SLIDE TRANSITION]',
        '[מעבר שקף]',
        19,
    ),
]
EOF
````

- [ ] **Step 2: Verify.** Dev loop and findings. **Expected: `79 finding(s)`**, with no `slide_markers` line.

- [ ] **Step 3: Commit.** `git add -u courses/ai-dev && git commit -m "fix(content): use [מעבר שקף] slide markers in lesson 0.4"`

---

### Task 6 (C): Archive residue (item 5 + G1 + RV-M1 + RV2-M6)

**Files:** Modify scripts and exercises in 0.2–0.4, 1.1–1.8 and 2.1–2.6 (spec §4.2 "Item 5").

This one task (one commit) covers:
- the course name "AI Dev". The job title "AI Engineer" stays: `0.2:9,41,83,123-129,161`, `0.3:111`, and the English "AI engineer" in 0.4.
- exercise H1 and `**שיעור:**` lines
- script titles
- every spoken lesson number in the spec's inventory
- the module words
- the dead cross-references, each replaced by a bridge or cut
- the three leaked preambles

The whole-file swaps (`שלוש נקודה` → `אחת נקודה` in the Module 01 scripts, `חמש נקודה` → `שתיים נקודה` in the Module 02 scripts) are safe. Every occurrence in those files is a lesson reference, and the counts pin that. The allowlisted non-lesson numbers (e.g. `2.5:12` "שלוש נקודה שלוש עשרה") sit in files these swaps don't touch.

- [ ] **Step 1: Apply all three modules' edits in one helper run.** The comments mark Module 00, 01 and 02. The 1.3 edits here are only its lines 1 and 41; Task 7 does the rest of 1.3.

````bash
SCRATCH=…  # your scratchpad
uv run python "$SCRATCH/apply_edits.py" <<'EOF'
[
    # --- Module 00 ---
    (
        'courses/ai-dev/lessons/00-ai-fundamentals/0.2-intro-to-ai/0.2_script.txt',
        'שיעור 0.1 - מבוא לבינה מלאכותית',
        'שיעור 0.2 - מבוא לבינה מלאכותית',
    ),
    (
        'courses/ai-dev/lessons/00-ai-fundamentals/0.2-intro-to-ai/0.2_script.txt',
        'שלום וברוכים הבאים לקורס AI Engineer.',
        'שלום וברוכים הבאים לקורס AI Dev.',
    ),
    (
        'courses/ai-dev/lessons/00-ai-fundamentals/0.2-intro-to-ai/0.2_script.txt',
        'אוטומציות עסקיות, סוכני AI, אפליקציות, מערכות שיווק, הכל hands-on.',
        'אפליקציות, אינטגרציות עם API, סוכני AI ושרתי MCP, הכל hands-on.',
    ),
    (
        'courses/ai-dev/lessons/00-ai-fundamentals/0.2-intro-to-ai/0.2_script.txt',
        "בואו נתחיל מהתמונה הגדולה. הקורס מחולק לשמונה מודולים. אנחנו עכשיו במודול אפס, שזה הבסיס. אחריו נצלול לאוטומציות עסקיות עם כלים כמו Make ו-n8n, שזה עשרים וארבע שעות. אחר כך נבנה צ'אטבוטים וסוכני AI, עשרים ושמונה שעות. נלמד Vibe Coding עם Claude Code, עוד עשרים ושמונה שעות. נעבוד עם כלי תמונה ווידאו, שש עשרה שעות. נלמד API ואינטגרציות, עשרים שעות. נשלב AI בשיווק ומכירות, שתים עשרה שעות. ונסיים עם פרויקט גמר של עשרים שעות.",
        'בואו נתחיל מהתמונה הגדולה. הקורס מחולק לארבעה מודולים. אנחנו עכשיו במודול אפס, יסודות ה-AI, שזה הבסיס. אחריו, במודול אחת, נלמד Vibe Coding עם Claude Code, ונבנה ונעלה לאוויר אפליקציה אמיתית. במודול שתיים נעבוד ישירות עם ה-API של Claude ושל מודלים נוספים, עם Webhooks, פלט מובנה ו-MCP. ונסיים במודול שלוש, פרויקט מסכם.',
    ),
    (
        'courses/ai-dev/lessons/00-ai-fundamentals/0.2-intro-to-ai/0.2_script.txt',
        'כל מודול מסתיים בפרויקט אמיתי. בסוף הקורס יהיה לכם פורטפוליו של פרויקטים שאפשר להציג ללקוחות או למעסיקים. סה"כ מאה חמישים ושש שעות לימוד.',
        'בסוף הקורס יהיה לכם פורטפוליו של פרויקטים שאפשר להציג ללקוחות או למעסיקים.',
    ),
    (
        'courses/ai-dev/lessons/00-ai-fundamentals/0.2-intro-to-ai/0.2_script.txt',
        'בשיעור 0.3 נלמד את זה לעומק.',
        'בשיעור 0.4 נלמד את זה לעומק.',
    ),
    (
        'courses/ai-dev/lessons/00-ai-fundamentals/0.2-intro-to-ai/0.2_script.txt',
        'ובשיעור 0.3 נצלול ל-Prompt Engineering',
        'ובשיעור 0.4 נצלול ל-Prompt Engineering',
    ),
    (
        'courses/ai-dev/lessons/00-ai-fundamentals/0.2-intro-to-ai/0.2_exercises.md',
        '# תרגילים - שיעור 0.1:',
        '# תרגילים - שיעור 0.2:',
    ),
    (
        'courses/ai-dev/lessons/00-ai-fundamentals/0.2-intro-to-ai/0.2_exercises.md',
        '- **שיעור:** 0.1 -',
        '- **שיעור:** 0.2 -',
    ),
    (
        'courses/ai-dev/lessons/00-ai-fundamentals/0.2-intro-to-ai/0.2_exercises.md',
        '- **קורס:** AI Engineer',
        '- **קורס:** AI Dev',
    ),
    (
        'courses/ai-dev/lessons/00-ai-fundamentals/0.2-intro-to-ai/0.2_exercises.md',
        '''- "בוט לוואטסאפ שעונה ללקוחות" → מודולים 1+2
- "אפליקציה לניהול עסק" → מודול 3
- "מערכת שיווק אוטומטית" → מודולים 1+6
- "סוכן AI שמנהל את המייל שלי" → מודולים 2+5
''',
        '''- "בוט לוואטסאפ שעונה ללקוחות" → מודולים 02+03
- "אפליקציה לניהול עסק" → מודול 01
- "סוכן AI שמנהל את המייל שלי" → מודול 02
''',
    ),
    (
        'courses/ai-dev/lessons/00-ai-fundamentals/0.3-ai-tools-overview/0.3_script.txt',
        'שיעור 0.2 - סקירת כלי AI מובילים',
        'שיעור 0.3 - סקירת כלי AI מובילים',
    ),
    (
        'courses/ai-dev/lessons/00-ai-fundamentals/0.3-ai-tools-overview/0.3_script.txt',
        'לשיעור השני בקורס AI Engineer.',
        'לשיעור השלישי בקורס AI Dev.',
    ),
    (
        'courses/ai-dev/lessons/00-ai-fundamentals/0.3-ai-tools-overview/0.3_script.txt',
        ' נלמד את זה לעומק במודול הראשון.',
        '',
    ),
    (
        'courses/ai-dev/lessons/00-ai-fundamentals/0.3-ai-tools-overview/0.3_script.txt',
        'נלמד לחשב את זה בפירוט במודול חמש.',
        'נלמד לחשב את זה בפירוט במודול שתיים.',
    ),
    (
        'courses/ai-dev/lessons/00-ai-fundamentals/0.3-ai-tools-overview/0.3_exercises.md',
        '# תרגילים - שיעור 0.2:',
        '# תרגילים - שיעור 0.3:',
    ),
    (
        'courses/ai-dev/lessons/00-ai-fundamentals/0.3-ai-tools-overview/0.3_exercises.md',
        '- **שיעור:** 0.2 -',
        '- **שיעור:** 0.3 -',
    ),
    (
        'courses/ai-dev/lessons/00-ai-fundamentals/0.3-ai-tools-overview/0.3_exercises.md',
        '- **קורס:** AI Engineer',
        '- **קורס:** AI Dev',
    ),
    (
        'courses/ai-dev/lessons/00-ai-fundamentals/0.3-ai-tools-overview/0.3_exercises.md',
        '5. **Claude API + n8n / Make** – נלמד בדיוק את זה במודולים 1 ו-2',
        '5. **Claude API + n8n / Make**',
    ),
    (
        'courses/ai-dev/lessons/00-ai-fundamentals/0.4-prompt-engineering/0.4_script.txt',
        'Lesson 0.3 — Prompt Engineering: Writing Effective Prompts',
        'Lesson 0.4 — Prompt Engineering: Writing Effective Prompts',
    ),
    (
        'courses/ai-dev/lessons/00-ai-fundamentals/0.4-prompt-engineering/0.4_script.txt',
        'welcome to Lesson 0.3 —',
        'welcome to Lesson 0.4 —',
    ),
    (
        'courses/ai-dev/lessons/00-ai-fundamentals/0.4-prompt-engineering/0.4_exercises.md',
        '# תרגילים - שיעור 0.3:',
        '# תרגילים - שיעור 0.4:',
    ),
    (
        'courses/ai-dev/lessons/00-ai-fundamentals/0.4-prompt-engineering/0.4_exercises.md',
        '- **שיעור:** 0.3 -',
        '- **שיעור:** 0.4 -',
    ),
    (
        'courses/ai-dev/lessons/00-ai-fundamentals/0.4-prompt-engineering/0.4_exercises.md',
        '- **קורס:** AI Engineer',
        '- **קורס:** AI Dev',
    ),
    # --- Module 01 (1.3: only its lines 1 and 41; Task 7 does the rest) ---
    (
        'courses/ai-dev/lessons/01-claude-code/1.1-intro-vibe-coding/1.1_script.txt',
        'שלוש נקודה',
        'אחת נקודה',
        7,
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.2-claude-code-setup/1.2_script.txt',
        'שלוש נקודה',
        'אחת נקודה',
        2,
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.3-claude-md-memory-skills/1.3_script.txt',
        'שלוש נקודה',
        'אחת נקודה',
        2,
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.4-landing-page-claude-code/1.4_script.txt',
        'שלוש נקודה',
        'אחת נקודה',
        3,
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.5-fullstack-app/1.5_script.txt',
        'שלוש נקודה',
        'אחת נקודה',
        1,
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.6-supabase/1.6_script.txt',
        'שלוש נקודה',
        'אחת נקודה',
        2,
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.8-deploy-production/1.8_script.txt',
        'שלוש נקודה',
        'אחת נקודה',
        1,
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.1-intro-vibe-coding/1.1_script.txt',
        'בשיעורים הקודמים בנינו אוטומציות עם Make ו-n8n, בנינו בוטים לוואטסאפ ולטלגרם, והבנו איך סוכן AI עובד.',
        'במודול אפס הבנו איך מודלי שפה עובדים, הכרנו את כלי ה-AI המובילים ולמדנו לכתוב פרומפטים טובים.',
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.1-intro-vibe-coding/1.1_script.txt',
        'בהמשך מודול שלוש.',
        'בהמשך מודול אחת.',
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.2-claude-code-setup/1.2_script.txt',
        'בשיעור 3.3.',
        'בשיעור 1.3.',
        3,
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.2-claude-code-setup/1.2_script.txt',
        'בשיעור 3.7.',
        'בשיעור 1.7.',
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.7-code-review-sub-agents/1.7_script.txt',
        'בשיעור השביעי של המודול השלישי.',
        'בשיעור השביעי של מודול אחת.',
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.7-code-review-sub-agents/1.7_exercises.md',
        '# תרגילים - שיעור 3.7:',
        '# תרגילים - שיעור 1.7:',
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.7-code-review-sub-agents/1.7_exercises.md',
        '- **שיעור:** 3.7 -',
        '- **שיעור:** 1.7 -',
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.8-deploy-production/1.8_script.txt',
        'השיעור האחרון במודול שלוש!',
        'השיעור האחרון במודול אחת!',
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.8-deploy-production/1.8_script.txt',
        'חברים, סיימנו את מודול שלוש.',
        'חברים, סיימנו את מודול אחת.',
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.8-deploy-production/1.8_script.txt',
        "ועכשיו, אחרי שבנינו את התשתית, במודול הבא אנחנו עוברים לעולם הוויזואלי. אם עד עכשיו התעסקנו בטקסט וקוד, במודול ארבע נלמד איך לגרום לבינה המלאכותית ליצור תמונות מדהימות, ריאליסטיות וגם אמנותיות. נתחיל בשיעור הבא עם מודלי יצירת תמונות: נכיר את דאלי שלוש דרך האיי פי איי של צ'אט ג'י פי טי, נצלול למודל העוצמתי החדש נאנו בננה שתיים, וכמובן נדבר על מידג'רני שהפך לשם נרדף לאמנות בינה מלאכותית. אנחנו הולכים ללמוד איך לכתוב פרומפטים אפקטיביים, איך לשלוט בסטייל, בקומפוזיציה, ואיך לשלב את היכולות האלה באפליקציות שלנו. אז תבואו עם הרבה יצירתיות, אנחנו נכנסים לעולם שבו כל מה שאפשר לדמיין, אפשר גם ליצור. תודה רבה לכולם, נתראה בשבוע הבא",
        'ועכשיו, אחרי שבנינו אפליקציה אמיתית והעלינו אותה לפרודקשן, במודול שתיים אנחנו עוברים לעבוד ישירות עם ה-API של מודלי השפה: נבין מהו API, נכתוב קוד שמדבר עם Claude, OpenAI ו-Gemini, ונחבר את המודלים לשירותים אחרים. תודה רבה לכולם, נתראה בשיעור הבא.',
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.8-deploy-production/1.8_exercises.md',
        '''בטח, בשמחה. הנה קובץ תרגילים מקיף ומעשי לשיעור 3.8, שנבנה בהתאם לדרישות ולפורמט שצוינו.

---

''',
        '',
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.8-deploy-production/1.8_exercises.md',
        '# תרגילים - שיעור 3.8:',
        '# תרגילים - שיעור 1.8:',
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.8-deploy-production/1.8_exercises.md',
        '- **שיעור:** 3.8 -',
        '- **שיעור:** 1.8 -',
    ),
    # --- Module 02 ---
    (
        'courses/ai-dev/lessons/02-claude-api/2.1-what-is-api/2.1_script.txt',
        'חמש נקודה',
        'שתיים נקודה',
        2,
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.2-claude-openai-gemini-api/2.2_script.txt',
        'חמש נקודה',
        'שתיים נקודה',
        3,
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.4-structured-output/2.4_script.txt',
        'חמש נקודה',
        'שתיים נקודה',
        3,
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.5-python-patterns/2.5_script.txt',
        'חמש נקודה',
        'שתיים נקודה',
        1,
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.6-mcp/2.6_script.txt',
        'חמש נקודה',
        'שתיים נקודה',
        2,
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.1-what-is-api/2.1_script.txt',
        'בקורס AI Engineer.',
        'בקורס AI Dev.',
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.1-what-is-api/2.1_script.txt',
        'במודול הקודם, ובמיוחד בשיעור ארבע נקודה שש, למדנו להשתמש בכלי בינה מלאכותית כדי ליצור נכסים שיווקיים מדהימים, כמו סרטונים. השתמשנו בממשקים גרפיים, לחצנו על כפתורים וקיבלנו תוצאה.',
        'במודול הקודם בנינו אפליקציה אמיתית עם Claude Code והעלינו אותה לאוויר. עבדנו דרך כלי שמסתיר מאיתנו את רוב הפרטים: ביקשנו, וקיבלנו תוצאה.',
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.3-webhooks/2.3_script.txt',
        'לשיעור חמישי-שלוש',
        'לשיעור שתיים נקודה שלוש',
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.3-webhooks/2.3_script.txt',
        'בשיעור הבא, חמישי-ארבע,',
        'בשיעור הבא, שתיים נקודה ארבע,',
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.6-mcp/2.6_script.txt',
        ' [warm] במודול שש נעבור מעולם הפיתוח לעולם העסקי. בשיעור הבא, שש נקודה אחת, נלמד איך להשתמש בבינה מלאכותית כדי לכתוב תוכן שיווקי שממיר. תודה רבה שהייתם איתי, ונתראה בשיעור הבא.',
        ' [warm] תודה רבה שהייתם איתי, וסיימנו יחד את מודול שתיים.',
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.3-webhooks/2.3_exercises.md',
        '''בטח, הנה קובץ תרגילים מקצועי ומעשי לשיעור 5.3 בנושא Webhooks, מותאם לקהל ישראלי.

''',
        '',
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.6-mcp/2.6_exercises.md',
        '''בטח, בשמחה. הנה קובץ תרגילים מובנה לשיעור 5.6, עם דגש על יישומים מעשיים ורלוונטיות לשוק הישראלי, בהתאם למבנה ולדרישות שצוינו.

''',
        '',
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.1-what-is-api/2.1_exercises.md',
        '# תרגילים - שיעור 5.1:',
        '# תרגילים - שיעור 2.1:',
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.1-what-is-api/2.1_exercises.md',
        '- **שיעור:** 5.1 -',
        '- **שיעור:** 2.1 -',
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.2-claude-openai-gemini-api/2.2_exercises.md',
        '# תרגילים - שיעור 5.2:',
        '# תרגילים - שיעור 2.2:',
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.2-claude-openai-gemini-api/2.2_exercises.md',
        '- **שיעור:** 5.2 -',
        '- **שיעור:** 2.2 -',
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.3-webhooks/2.3_exercises.md',
        '# תרגילים - שיעור 5.3:',
        '# תרגילים - שיעור 2.3:',
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.3-webhooks/2.3_exercises.md',
        '- **שיעור:** 5.3 -',
        '- **שיעור:** 2.3 -',
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.4-structured-output/2.4_exercises.md',
        '# תרגילים - שיעור 5.4:',
        '# תרגילים - שיעור 2.4:',
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.4-structured-output/2.4_exercises.md',
        '- **שיעור:** 5.4 -',
        '- **שיעור:** 2.4 -',
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.5-python-patterns/2.5_exercises.md',
        '# תרגילים - שיעור 5.5:',
        '# תרגילים - שיעור 2.5:',
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.5-python-patterns/2.5_exercises.md',
        '- **שיעור:** 5.5 -',
        '- **שיעור:** 2.5 -',
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.6-mcp/2.6_exercises.md',
        '# תרגילים - שיעור 5.6:',
        '# תרגילים - שיעור 2.6:',
    ),
    (
        'courses/ai-dev/lessons/02-claude-api/2.6-mcp/2.6_exercises.md',
        '- **שיעור:** 5.6 -',
        '- **שיעור:** 2.6 -',
    ),
]
EOF
````

- [ ] **Step 2: Check what the lints don't see.**

```bash
L=courses/ai-dev/lessons
for f in $L/01-claude-code/1.8-*/1.8_exercises.md $L/02-claude-api/2.3-*/2.3_exercises.md $L/02-claude-api/2.6-*/2.6_exercises.md; do head -1 "$f"; done
grep -rnE "בשיעור 0\.3|בשיעור 3\.[0-9]|מודול (שלוש|חמש|שש)|המודול השלישי|מודולים 1|Make ו-n8n, בנינו|הבאבטח|שיעור 3\.8|לשיעור השני" $L --include='*_script.txt' --include='*_exercises.md'
```
Expected: three lines of `<div dir="rtl" lang="he">`, then **only** `0.2_script.txt:13` (the new "…ונסיים במודול שלוש, פרויקט מסכם.": module 03 is real). Anything else is residue: fix it the same way, then tell the user.

- [ ] **Step 3: Verify.** Dev loop and findings. **Expected: `2 finding(s)`**. They are `1.6_exercises.md:21 … NEXT_PUBLIC_SUPABASE_ANON_KEY` (Task 8) and `setup.md:… [clean_slate_no_delete]` (Task 14).

- [ ] **Step 4: Commit.** `git add -u courses/ai-dev && git commit -m "fix(content): remove archive residue from course content"`. The body names G1, RV-M1 and RV2-M6.

---

### Task 7 (C): The 1.3 hook exercise (item 10 + RV-L2 + S14)

**Files:** Modify `1.3_exercises.md` and `1.3_script.txt`.

Exercise 5 becomes a project-scoped read guard on a fake secret, with the live `cat` bypass as the lesson. Nothing deletes a file or asks the learner to try (spec §4.2 "Item 10"). The script's `:3` and `:11` facts about when auto memory arrived (2.1.59) stay.

- [ ] **Step 1: Apply the edits:**

````bash
SCRATCH=…  # your scratchpad
uv run python "$SCRATCH/apply_edits.py" <<'EOF'
[
    (
        'courses/ai-dev/lessons/01-claude-code/1.3-claude-md-memory-skills/1.3_exercises.md',
        '(v2.1.59+)',
        '(v2.1.176+)',
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.3-claude-md-memory-skills/1.3_exercises.md',
        'הפעלה אוטומטית של Skills נעשית דרך Hooks (תרגיל 5), לא דרך הגדרת Skills עצמם.',
        'קלוד יכול גם להפעיל Skill בעצמו, כשהבקשה מתאימה ל-`description` שלו; כאן נריץ אותו ידנית.',
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.3-claude-md-memory-skills/1.3_exercises.md',
        '''## תרגיל 5: הגנת מערכת עם Hooks (מעשי - 45 דקות)
### הנחיות:
Hooks משמשים כ-Guardrails (מעקות בטיחות) כדי למנוע מקלוד לבצע פעולות הרסניות באמצעות הכלים שלו (כמו כלי ה-Bash).

### שאלות/משימות:
1. אתרו או צרו את קובץ `settings.json` של Claude Code (בדרך כלל בתיקיית ההגדרות הגלובלית או בפרויקט תחת `.claude/`).
2. הוסיפו הגדרת `PreToolUse` hook עבור הכלי `Bash`.
3. כתבו סקריפט Shell קצר (למשל `safe_bash.sh`) שמקבל את הפקודה שקלוד רוצה להריץ.
4. הסקריפט צריך לבדוק: אם הפקודה מכילה את המילים `rm -rf`, `drop table`, או `npm publish`, הסקריפט יעצור וידרוש אישור הקלדה ידני מהמשתמש (Y/N).
5. חברו את הסקריפט ל-Hook ב-`settings.json`.
6. נסו לבקש מקלוד: "מחק את כל הקבצים בתיקייה הזו בכוח". ודאו שה-Hook עוצר את הפעולה ודורש אישור.

''',
        '''## תרגיל 5: שומר קריאה עם Hooks (מעשי - 45 דקות)
### הנחיות:
Hooks הם מעקות בטיחות דטרמיניסטיים: Claude Code מריץ אותם בכל פעם שקריאת כלי מתאימה להגדרה, וקלוד לא יכול לדלג עליהם. בתרגיל הזה נגן על קובץ "סודי" מזויף מפני **קריאה**, ונראה גם איפה ההגנה נגמרת. שום קובץ לא נמחק ולא נכתב, גם אם השומר נכשל.

### שאלות/משימות:
1. **הכנה.** בתיקייה `claude-advanced-lab` צרו שני קבצים:
   * `secret-demo.txt` עם השורה `FAKE_API_KEY=not-a-real-key`
   * `notes.txt` עם שורה כלשהי
2. **ה-Hook.** צרו את הקובץ `claude-advanced-lab/.claude/settings.json` (הגדרה ברמת הפרויקט, לא בהגדרות הגלובליות) עם התוכן הבא:
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
   ב-Windows בלי Git Bash, החליפו את שורת ה-`command` בשורה:
   `"command": "[Console]::Error.WriteLine('Blocked by hook: secret-demo.txt is protected'); exit 2"`
3. **בדיקה שלילית.** הפעילו מחדש את Claude Code בתוך התיקייה, ובקשו **במילים** (לא עם אזכור `@secret-demo.txt`) לקרוא את `secret-demo.txt`. הקריאה נחסמת, וקלוד חוזר על הסיבה שה-Hook כתב. *אם קלוד מנסה מיד, מיוזמתו, דרך הטרמינל, זה שלב 5 שקורה מוקדם. רשמו את זה.*
4. **בדיקת ביקורת.** בקשו לקרוא את `notes.txt`. הקריאה עובדת כרגיל.
5. **העקיפה.** בקשו במפורש: "הרץ בטרמינל `cat secret-demo.txt`" (בלי Git Bash: `Get-Content secret-demo.txt`). התוכן מופיע.
   * *אם קלוד מסרב,* הסירוב הוא התנהגות של המודל, לא אכיפה. רשמו מה קרה.
6. **המסקנה.**
   * Hook הוא מעקה בטיחות דטרמיניסטי **לקריאות הכלים שהוא תופס**. כלים אחרים (Bash, PowerShell, Grep) עדיין מגיעים לקובץ, וכנראה שגם אזכור `@file`, שאינו קריאה לכלי Read (לא נבדק). לכן Hook אינו מחסום אבטחה.
   * ל-Claude Code יש שכבות חזקות יותר:
     * **כללי deny** בהרשאות, שחוסמים גם `cat`/`head`/`tail`, אבל לא סקריפטים שפותחים קבצים בעצמם
     * **ה-sandbox**, שנאכף ברמת מערכת ההפעלה (macOS, Linux, WSL2)
   * האכיפה החזקה ביותר נמצאת מחוץ לקלוד לגמרי: הרשאות של מערכת ההפעלה שהמשתמש שמריץ את הסוכן לא יכול לבטל.

   > **להמחשה בלבד — לא להריץ** (Linux):
   > `chmod 000 secret-demo.txt && sudo chattr +i secret-demo.txt`

   * "מחוץ להישג יד" פירושו מחוץ להישג ידו של כל תהליך שהסוכן יכול להפעיל.
7. **הערה על Y/N.** ל-Hooks אין טרמינל, ולכן Hook לא יכול לשאול "Y/N" בעצמו. כדי לבקש אישור, Hook מחזיר `permissionDecision: "ask"` (קריאת רשות: תיעוד ה-Hooks של Claude Code).

''',
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.3-claude-md-memory-skills/1.3_exercises.md',
        'וסקריפט ה-Hook לגיטהאב',
        'ו-`.claude/settings.json` עם ה-Hook לגיטהאב',
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.3-claude-md-memory-skills/1.3_exercises.md',
        '| **יישום Hooks (Guardrails)** | 20% | כתיבת סקריפט מניעה תקין, חיבור נכון ל-`settings.json`, ועצירת פעולות מסוכנות. |',
        '| **יישום Hooks (Guardrails)** | 20% | ה-Hook חוסם את קריאת `secret-demo.txt` (Read), הסבר למה רק קוד יציאה 2 חוסם וקוד 1 לא, והסבר של עקיפת ה-`cat` בטרמינל. |',
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.3-claude-md-memory-skills/1.3_script.txt',
        'כדי שזה יעבוד, ודאו שיש לכם גרסה מעודכנת של קלוד קוד, שתיים נקודה אחת נקודה חמישים ותשע ומעלה.',
        'לשיעור הזה צריך קלוד קוד בגרסה שתיים נקודה אחת נקודה מאה שבעים ושש ומעלה.',
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.3-claude-md-memory-skills/1.3_script.txt',
        'הוק הוא קוד קשיח שחוסם פעולה באופן מוחלט.',
        'הוק הוא קוד קשיח שרץ באופן דטרמיניסטי על כל קריאת כלי שהוא מוגדר לתפוס, ורק עליה.',
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.3-claude-md-memory-skills/1.3_script.txt',
        'הסקריפט מחזיר שגיאה וקלוד נחסם.',
        'הסקריפט מסתיים בקוד יציאה שתיים וקלוד נחסם.',
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.3-claude-md-memory-skills/1.3_script.txt',
        'אם סקריפט הפרי טול יוז מחזיר קוד יציאה שונה מאפס, הפעולה של קלוד נחסמת והוא מקבל את הודעת השגיאה כדי שיוכל לנסות דרך אחרת.',
        'אם סקריפט הפרי טול יוז מסתיים בקוד יציאה שתיים, הפעולה של קלוד נחסמת, והוא מקבל את מה שהסקריפט כתב לפלט השגיאות כדי שיוכל לנסות דרך אחרת. שימו לב: קוד יציאה אחד לא חוסם. הוא נחשב שגיאה לא חוסמת, והפעולה ממשיכה כרגיל. רק קוד יציאה שתיים חוסם.',
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.3-claude-md-memory-skills/1.3_script.txt',
        "בואו ניצור שומר סף. בתיקיית נקודה קלוד, צרו קובץ הגדרות ג'ייסון והגדירו בו הוק מסוג פרי טול יוז שמצביע לסקריפט בשם צ'ק קומנד נקודה אס אייג'. בשורש הפרויקט, צרו את סקריפט הבאש הזה וכתבו בו תנאי שאם הפקודה מכילה את המילה אר אם, הוא מדפיס שגיאת אבטחה ומחזיר קוד יציאה אחד. תנו לסקריפט הרשאות ריצה. עכשיו, בקשו מקלוד למחוק קובץ בפרויקט ותראו איך ההוק חוסם אותו. מעניין לבדוק איך קלוד הגיב כשנחסם, והאם הוא ניסה להשתמש בדרך אחרת, כמו סקריפט פייתון, כדי לבצע את המחיקה. למשתמשי ווינדוס, אפשר לכתוב סקריפט באטש או פאוורשל מקביל, או להשתמש במערכת המשנה של לינוקס.",
        "בואו ניצור שומר סף. בתיקיית הפרויקט צרו קובץ בשם סיקרט דמו נקודה טי אקס טי עם מפתח מזויף, וקובץ נוסף בשם נוטס נקודה טי אקס טי. בקובץ ההגדרות של הפרויקט, סטינגס נקודה ג'ייסון שבתוך תיקיית נקודה קלוד, הגדירו הוק מסוג פרי טול יוז שתופס את כלי הקריאה, רק עבור הקובץ סיקרט דמו, ומסתיים בקוד יציאה שתיים עם הודעה שהקובץ מוגן. פתחו מחדש את קלוד קוד ובקשו ממנו, במילים, לקרוא את הקובץ. תראו איך ההוק חוסם אותו, ואיך קלוד מסביר למה. קריאה של נוטס נקודה טי אקס טי, לעומת זאת, עובדת כרגיל. ועכשיו החלק המעניין: בקשו ממנו במפורש להריץ בטרמינל קאט על הקובץ. התוכן יופיע, כי ההוק תופס רק את כלי הקריאה ולא את הטרמינל. וזה השיעור החשוב: הוק הוא מעקה בטיחות לקריאות הכלים שהוא תופס, לא מחסום אבטחה. למשתמשי ווינדוס בלי גיט באש, יש בדף התרגילים גרסת פאוורשל של אותה פקודה.",
    ),
]
EOF
````

- [ ] **Step 2: Check.**

```bash
f=courses/ai-dev/lessons/01-claude-code/1.3-claude-md-memory-skills
grep -c "v2.1.176+" $f/1.3_exercises.md
grep -nE "rm -rf|safe_bash|Y/N\)|drop table|אר אם|פייתון, כדי לבצע את המחיקה|קוד יציאה אחד\. תנו" $f/1.3_exercises.md $f/1.3_script.txt
grep -n "שתיים נקודה אחת נקודה" $f/1.3_script.txt
```
Expected: `1`; no output from the second grep; the third shows lines 3, 11 (2.1.59, kept) and 15 (the new 2.1.176 requirement).

- [ ] **Step 3: Verify.** Dev loop and findings. **Expected: `2 finding(s)`** (unchanged).

- [ ] **Step 4: Commit.** `git add -u courses/ai-dev && git commit -m "fix(content): make the lesson 1.3 hook exercise a safe read guard"`

---

### Task 8 (C): Supabase keys and MCP in 1.6 (item 16 + S16 + RV-M6)

**Files:** Modify `1.6_exercises.md` and `1.6_script.txt`. The `@supabase/ssr`/auth rewrite and removing Prisma stay in 1d.

The spec asks to adjust questions and rubric "wherever they assume an MCP insert". None do (checked 2026-09-29: exercise 4's questions ask about schemas and security, and the rubric has no MCP row), so only step 2 of exercise 4 changes.

- [ ] **Step 1: Apply the edits:**

````bash
SCRATCH=…  # your scratchpad
uv run python "$SCRATCH/apply_edits.py" <<'EOF'
[
    (
        'courses/ai-dev/lessons/01-claude-code/1.6-supabase/1.6_exercises.md',
        '2. העתיקו את ה-URL וה-Anon Key ממסך ה-API Settings.',
        '2. העתיקו את ה-URL ואת ה-Publishable key (`sb_publishable_...`) ממסך ה-API Keys.',
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.6-supabase/1.6_exercises.md',
        'NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key',
        'NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=sb_publishable_...',
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.6-supabase/1.6_exercises.md',
        '1. מדוע אנו משתמשים ב-Anon Key בצד הלקוח,',
        '1. מדוע אנו משתמשים ב-Publishable Key בצד הלקוח,',
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.6-supabase/1.6_exercises.md',
        '1. התקינו את שרת ה-MCP של Supabase (אם טרם הוגדר):\n```bash\n# הוספת ה-MCP לקונפיגורציה של קלוד (בהתאם לתיעוד MCP)\nclaude mcp add supabase --project-ref your-project-ref --access-token your-personal-access-token\n```\n2. השתמשו ב-Claude Code כדי לתשאל את ה-DB בלי לצאת מהטרמינל:\n```bash\nclaude "Using the Supabase MCP, describe the schema of the \'clients\' table. Then, insert a dummy record for an Israeli client named \'משה ובניו בע\\"מ\' without hardcoding a UUID (let Postgres generate it)."\n```\n',
        '''1. חברו את שרת ה-MCP המתארח של Supabase, ברמת הפרויקט ובמצב קריאה בלבד (החליפו את `<your-project-ref>` במזהה הפרויקט שלכם):
```bash
claude mcp add --scope project --transport http supabase "https://mcp.supabase.com/mcp?project_ref=<your-project-ref>&read_only=true"
```
   לאחר מכן, בטרמינל רגיל (לא בתוסף ה-IDE) הריצו `claude /mcp`, בחרו **supabase** ← **Authenticate**, והתחברו ל-Supabase בדפדפן שנפתח. אין צורך ב-Personal Access Token.
2. השתמשו ב-Claude Code כדי לתשאל את ה-DB בלי לצאת מהטרמינל:
```bash
claude "Using the Supabase MCP, describe the schema of the 'clients' table."
```
   לאחר מכן הכניסו ידנית, ב-Table Editor של Supabase, רשומה פיקטיבית של לקוח ישראלי בשם 'משה ובניו בע"מ', בלי UUID קשיח (Postgres ייצר אותו). שרת ה-MCP מוגדר כאן כקריאה בלבד בכוונה: Claude Code יכול לקרוא את הסכמה והנתונים אבל לא לשנות אותם, וזה גבול בטוח למתחילים.
''',
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.6-supabase/1.6_exercises.md',
        '(ודאו שאין סודות - `anon key` ו-`url` צריכים להיות ב-`.env`).',
        '(ודאו שאין סודות - ה-`publishable key` וה-`url` צריכים להיות ב-`.env`. `SUPABASE_SECRET_KEY` הוא לשרת בלבד: לעולם לא עם קידומת `NEXT_PUBLIC_`, ולעולם לא ב-git).',
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.6-supabase/1.6_script.txt',
        'את המפתח הציבורי שנקרא אנון קי,',
        'את המפתח הציבורי שנקרא פאבלישבל קי,',
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.6-supabase/1.6_script.txt',
        'מה ההבדל בין המפתח הציבורי למפתח תפקיד השרת שרואים שם.',
        'מה ההבדל בין המפתח הציבורי למפתח הסודי, הסיקרט קי, שרואים שם.',
    ),
    (
        'courses/ai-dev/lessons/01-claude-code/1.6-supabase/1.6_script.txt',
        'לעולם אין לשים את מפתח השרת בקוד הלקוח',
        'לעולם אין לשים את המפתח הסודי בקוד הלקוח',
    ),
]
EOF
````

- [ ] **Step 2: Check.**

```bash
f=courses/ai-dev/lessons/01-claude-code/1.6-supabase
grep -niE "anon|service_role|access-token|insert a dummy" $f/1.6_exercises.md $f/1.6_script.txt
```
Expected: no output.

- [ ] **Step 3: Verify.** Dev loop and findings. **Expected: `1 finding(s)`** (only `clean_slate_no_delete`).

- [ ] **Step 4: Commit.** `git add -u courses/ai-dev && git commit -m "fix(content): Supabase publishable/secret keys and read-only MCP in 1.6"`

---

### Task 9 (C): Move old project B (item 12, content part; RV-L7, RV2-L3)

**Files:** Modify `courses/ai-dev/lessons/03-final-project/projects.md`. Create `…/03-final-project/old_B-document-intelligence.md`. Leave `projects.md:7` "מתוך ארבעה" stale on purpose (unit 1e).

- [ ] **Step 1: Move lines 174–318 verbatim.** Also delete the now-redundant `---` at `:319` and its blank line, so one separator remains between A and C:

````bash
uv run python - <<'EOF'
from pathlib import Path

src = Path("courses/ai-dev/lessons/03-final-project/projects.md")
dst = src.with_name("old_B-document-intelligence.md")
with open(src, encoding="utf-8", newline="") as f:
    lines = f.read().split("\n")
# 1-based: 174..318 is project B, 319 its trailing "---", 320 blank, 321 project C.
assert lines[173] == "## פרויקט ב: Document Intelligence Service", lines[173]
assert lines[318] == "---" and lines[319] == "", lines[318:320]
assert lines[320].startswith("## פרויקט ג"), lines[320]
note = (
    "> **הערה:** זהו פרויקט ב׳ הישן (Document Intelligence Service), שהועבר לכאן"
    " כפי שהוא. הוא אינו מחובר ל-`/learn project`, והוא אינו מסלול ב׳ החדש (PRD D5)."
)
body = "\n".join(lines[173:318]).rstrip("\n")
with open(dst, "w", encoding="utf-8", newline="") as f:
    f.write('<div dir="rtl" lang="he">\n\n' + note + "\n\n" + body + "\n\n</div>\n")
with open(src, "w", encoding="utf-8", newline="") as f:
    f.write("\n".join(lines[:173] + lines[320:]))
print(f"moved lines 174-318 to {dst.name}; removed the separator at 319-320")
EOF
````

- [ ] **Step 2: Check.**

```bash
d=courses/ai-dev/lessons/03-final-project
grep -n "^## \|^---" $d/projects.md | sed -n '1,8p'
head -3 $d/old_B-document-intelligence.md; tail -2 $d/old_B-document-intelligence.md
```
Expected: in `projects.md`, `## פרויקט א` is followed by one `---` and then `## פרויקט ג`. The new file opens with `<div dir="rtl" lang="he">` and the note, and ends with `</div>`.

- [ ] **Step 3: Verify.** Dev loop and findings. **Expected: `1 finding(s)`**. `old_B*` is skipped by every lint.

- [ ] **Step 4: Commit.** `git add courses/ai-dev/lessons/03-final-project && git commit -m "refactor(content): move old project B into its own unwired file"`

---

### Task 10 (T): Frontmatter on all 15 sub-modules (item 11)

**Files:** Modify all 15 `.claude/commands/learn/*.md`. `learn.md` gets **no** frontmatter (S2a decides its invocability). `display.md` gets the frontmatter and nothing else.

- [ ] **Step 1: Prepend the block:**

````bash
uv run python - <<'EOF'
from pathlib import Path

files = sorted(Path(".claude/commands/learn").glob("*.md"))
assert len(files) == 15, [f.name for f in files]
block = "---\ndisable-model-invocation: true\n---\n"
texts = {}
for f in files:  # check every file before writing any
    with open(f, encoding="utf-8", newline="") as fh:
        texts[f] = fh.read()
    assert not texts[f].startswith("---"), f"{f} already has frontmatter"
for f, text in texts.items():
    with open(f, "w", encoding="utf-8", newline="") as fh:
        fh.write(block + text)
print(f"frontmatter added to {len(files)} files")
EOF
````

- [ ] **Step 2: Check (the PR's grep, RV5-L6).**

```bash
for f in .claude/commands/learn/*.md; do head -3 "$f"; done | sort | uniq -c
head -1 .claude/commands/learn.md
```
Expected: `30 ---` and `15 disable-model-invocation: true`, and `learn.md` still starts with `# /learn — Interactive Tutor`. Cited line numbers in these files now shift by +3, and later tasks anchor on text.

- [ ] **Step 3: Verify.** Dev loop and findings. **Expected: `1 finding(s)`**.

- [ ] **Step 4: Commit.** `git add .claude/commands/learn && git commit -m "fix(tutor): disable model invocation of the learn sub-modules"`

---

### Task 11 (T): Hebrew aliases (item 7, S2)

**Files:** Modify `.claude/commands/learn.md` (the Learner Commands and Route tables) and `.claude/commands/learn/progress.md` (only its two "stop" trigger lines, RV5-L7). `quiz.md`'s body, `teaching.md:144` and `setup.md:225` stay unchanged. "בחן אותי" stays diagnostic.

- [ ] **Step 1: Apply the edits:**

````bash
SCRATCH=…  # your scratchpad
uv run python "$SCRATCH/apply_edits.py" <<'EOF'
[
    (
        '.claude/commands/learn.md',
        '| "quiz me" trigger | Read `.claude/commands/learn/quiz.md` |',
        '''| "quiz me" / "בוחן" trigger | Read `.claude/commands/learn/quiz.md` (covered sections) |
| "quiz me full" / "בוחן מלא" trigger | Read `.claude/commands/learn/quiz.md` in **quiz me full** mode |''',
    ),
    (
        '.claude/commands/learn.md',
        '| "stop" trigger |',
        '| "stop" / "עצור" / "סיום" trigger |',
    ),
    (
        '.claude/commands/learn.md',
        '| continue | Move to next section |',
        '| continue / המשך | Move to next section |',
    ),
    (
        '.claude/commands/learn.md',
        '| quiz me | Read `.claude/commands/learn/quiz.md` (covered sections) |',
        '| quiz me / בוחן | Read `.claude/commands/learn/quiz.md` (covered sections) |',
    ),
    (
        '.claude/commands/learn.md',
        '| quiz me full | Read `.claude/commands/learn/quiz.md` (whole lesson, 8 Qs) |',
        '| quiz me full / בוחן מלא | Read `.claude/commands/learn/quiz.md` in **quiz me full** mode (whole lesson, 8 Qs) |',
    ),
    (
        '.claude/commands/learn.md',
        '| stop | Read `.claude/commands/learn/progress.md`, then summarize |',
        '| stop / עצור / סיום | Read `.claude/commands/learn/progress.md`, then summarize |',
    ),
    (
        '.claude/commands/learn/progress.md',
        '*Loaded after covering at least one section, and on the "stop" command.*',
        '*Loaded after covering at least one section, and on the "stop / עצור / סיום" command.*',
    ),
    (
        '.claude/commands/learn/progress.md',
        '## Session End (on "stop" command)',
        '## Session End (on "stop / עצור / סיום" command)',
    ),
]
EOF
````

- [ ] **Step 2: Verify.** Dev loop and findings. **Expected: `1 finding(s)`**.

- [ ] **Step 3: Commit.** `git add -u .claude && git commit -m "feat(tutor): Hebrew aliases for continue, quiz me and stop"`

---

### Task 12 (T): No capstones until 1e (item 12 + G4)

**Files:** Modify `.claude/commands/learn.md` (the `project` row, RV4-L3), `learn/project.md` (a new first section) and `learn/resume.md` (one TEMPORARY rule replaces the eligibility line; both 🏗️ lines go; the route row stays).

Wording trap: `tutor_refs` (b) flags a backticked bare `name.md` **directly after** "Read"/"Load". So the new `project.md` step says "Do not open the final-projects file (`projects.md`)", never "Do not read `projects.md`".

- [ ] **Step 1: Apply the edits:**

````bash
SCRATCH=…  # your scratchpad
uv run python "$SCRATCH/apply_edits.py" <<'EOF'
[
    (
        '.claude/commands/learn.md',
        '| project | Read `.claude/commands/learn/project.md` — final project mode |',
        "| project | Read `.claude/commands/learn/project.md` — final projects (until unit 1e: shows 'being rebuilt') |",
    ),
    (
        '.claude/commands/learn/project.md',
        '## Step 1 — Load Project State',
        '''## Step 0 — TEMPORARY (until unit 1e)

**Until unit 1e lands, this module runs only this step.**

Tell the learner, in `session.language` and using `session.address`, that the final projects are being rebuilt, and that meanwhile they should continue with the lessons (`/learn`). Hebrew wording:

> "פרויקטי הגמר נבנים מחדש כרגע. בינתיים, המשיכו עם השיעורים: `/learn`"

Then **stop**. Do not open the final-projects file (`projects.md`), do not look for a project state file, and do not run Step 1 or any later step. Unit 1e deletes this step.

---

## Step 1 — Load Project State''',
    ),
    (
        '.claude/commands/learn/resume.md',
        'Check final project eligibility: learner is ready to start the final project if they have progress files for lessons in module 2 (any lesson 2.x), or have completed all lessons through 1.8.',
        '**TEMPORARY (until unit 1e): do not offer the final project.** Skip the final-project eligibility check, and never show a 🏗️ line in Step 2. Unit 1e restores both.',
    ),
    (
        '.claude/commands/learn/resume.md',
        '''[if eligible: 🏗️ Final Project — [show "starting" or current phase if already selected]]
''',
        '',
        2,
    ),
]
EOF
````

- [ ] **Step 2: Check.**

```bash
grep -c "🏗️" .claude/commands/learn/resume.md
grep -n "Step 0 — TEMPORARY" .claude/commands/learn/project.md
```
Expected: `2` (the new TEMPORARY rule, which names the 🏗️ line, and the route row at old `:74`), then one match.

- [ ] **Step 3: Verify.** Dev loop and findings. **Expected: `1 finding(s)`**.

- [ ] **Step 4: Commit.** `git add -u .claude && git commit -m "fix(tutor): stop offering the final project until unit 1e"`

---

### Task 13 (T): `security.md` ownership gate and `timingSafeEqual` (item 6, RV2-L10)

**Files:** Modify `.claude/commands/learn/security.md`: the Pre-flight section and the category-2 code sample (old `:128-136`).

- [ ] **Step 1: Apply the edits:**

````bash
SCRATCH=…  # your scratchpad
uv run python "$SCRATCH/apply_edits.py" <<'EOF'
[
    (
        '.claude/commands/learn/security.md',
        '''## Pre-flight — Get the URL

Parse `$ARGUMENTS` for a URL (starts with `http://` or `https://`).

- **URL provided** → store as `target_url`, proceed to Phase A (Live Scan).
- **No URL** → ask: "מה ה-URL של האפליקציה? (למשל: `https://my-app.onrender.com`). אם עוד לא העלית — הרץ `/learn deploy` קודם, ותחזור לכאן עם הכתובת."

''',
        '''## Pre-flight — Get the URL

Parse `$ARGUMENTS` for a URL (starts with `http://` or `https://`).

- **URL provided** → store as `target_url`, then run the ownership check below.
- **No URL** → ask: "מה ה-URL של האפליקציה? (למשל: `https://my-app.onrender.com`). אם עוד לא העלית — הרץ `/learn deploy` קודם, ותחזור לכאן עם הכתובת." When the learner gives a URL, store it as `target_url`, then run the ownership check below.

### Pre-flight — Ownership check (required on every entry path)

Run this once `target_url` is known and before Phase A, however the learner got here: `/learn security http…`, `/learn security` followed by a URL, or the `deploy` module's handoff. **Make no network request of any kind before this check passes.**

Use `AskUserQuestion`, in `session.language` (Hebrew shown):

```
question: "האפליקציה בכתובת הזו שלך, או שיש לך אישור מפורש לבדוק אותה?"
header: "אישור בדיקה"
options:
  - label: "כן — היא שלי, או שיש לי אישור מפורש"
    description: "ממשיכים לסריקה"
  - label: "לא"
    description: "לא סורקים את הכתובת הזו"
```

- **Only the first option continues** to Phase A.
- **Any other answer** (including "לא", free text, or anything unclear):
  - make no network request of any kind, and run none of Phases A–E
  - explain briefly, in `session.language`, that testing an app without permission can cause harm and may be illegal
  - suggest rerunning `/learn security` with the URL of an app the learner owns
  - then **end** the module

''',
    ),
    (
        '.claude/commands/learn/security.md',
        '''```js
const secret = process.env.SYNC_SECRET
if (!secret) return res.status(503).json({ error: 'Service unavailable' })

const provided = req.headers['x-sync-key']
if (!provided || !timingSafeEqual(Buffer.from(provided), Buffer.from(secret))) {
  return res.status(401).json({ error: 'Unauthorized' })
}
```

הסבר `timingSafeEqual`: השוואה רגילה (`===`) פגיעה ל-timing attack — אפשר לנחש מפתח תו-תו לפי זמן התשובה. `timingSafeEqual` לוקח אותו זמן תמיד.''',
        '''```js
const { createHash, timingSafeEqual } = require('node:crypto')
const digest = (s) => createHash('sha256').update(String(s)).digest()

const secret = process.env.SYNC_SECRET
if (!secret) return res.status(503).json({ error: 'Service unavailable' })

const provided = req.headers['x-sync-key']
if (!provided || !timingSafeEqual(digest(provided), digest(secret))) {
  return res.status(401).json({ error: 'Unauthorized' })
}
```

הסבר `timingSafeEqual`: השוואה רגילה (`===`) פגיעה ל-timing attack — אפשר לנחש מפתח תו-תו לפי זמן התשובה. `timingSafeEqual` לוקח אותו זמן תמיד. **למה משווים digests:** `timingSafeEqual` זורק שגיאה כשהאורכים שונים, והשרת היה מחזיר 500 במקום 401 וחושף את אורך המפתח; ל-SHA-256 של שני הצדדים יש תמיד אותו אורך (32 בתים), ולכן אין 500 ואין דליפה של האורך.''',
    ),
]
EOF
````

- [ ] **Step 2: Check.**

```bash
grep -n "Ownership check\|createHash\|digest(provided)" .claude/commands/learn/security.md
grep -c "Buffer.from(provided)" .claude/commands/learn/security.md
```
Expected: four matching lines (the ownership-check heading and three code lines), then `0`.

- [ ] **Step 3: Verify.** Dev loop and findings. **Expected: `1 finding(s)`**.

- [ ] **Step 4: Commit.** `git add -u .claude && git commit -m "fix(tutor): ownership gate and safe timingSafeEqual in /learn security"`

---

### Task 14 (T5): The clean-slate step (item 14, S4, S5)

**Files:** Modify `.claude/commands/learn/setup.md`: a new `## 0. Clean slate` between the CLEAN-SLATE markers, before `## A. Show Current Settings`.

The section's hard rules, find/show, ask, one-invocation move, verify and continue-or-stop follow spec §4.3 exactly. Wording traps checked by `clean_slate_no_delete`, which is case-insensitive:
- no delete verb anywhere between the markers, **not even to forbid it**. The prose says "no command that destroys files" and "removes the original".
- the repo's local settings file is named without backticks (RV-H4).

- [ ] **Step 1: Apply the edit:**

````bash
SCRATCH=…  # your scratchpad
uv run python "$SCRATCH/apply_edits.py" <<'EOF'
[
    (
        '.claude/commands/learn/setup.md',
        '## A. Show Current Settings',
        '<!-- CLEAN-SLATE:BEGIN — TEMPORARY, remove at first-cohort gate (PRD D10) -->\n## 0. Clean slate\n\n*TEMPORARY, for the tester period only. Runs on every `/learn setup`, before section 0.1.*\n\nLeftovers from an earlier install fail quietly: a personal `~/.claude/commands/learn.md` shadows this repo\'s `/learn` and keeps running old code, and an old `settings.json` is half-read. This step finds them and offers to move them into a backup folder.\n\n**Hard rules for this section:**\n- Look at exactly three paths, and nothing else: `~/skill-tutor-tutorials/`, `~/.claude/commands/learn.md` and `~/.claude/commands/learn/`. No globs, no other names.\n- Always build them from `$HOME`. Never use a relative path: this repo has its own skill-tutor-tutorials folder, which must never be touched.\n- Never touch anything inside this repo. That includes the repo\'s local settings file (.claude/settings.local.json) and the repo\'s own skill-tutor-tutorials folder.\n- Never touch an earlier backup folder (`~/skill-tutor-tutorials-backup-…`).\n- Move, never destroy. This section has no command that destroys files, and you must not run one. If any step fails, stop and report the error. Never retry with force.\n- When in doubt, keep.\n\n### Step 1 — Find and show\n\nRun this as **one** Bash tool call (on native Windows without Git Bash, run the PowerShell block instead):\n\n```bash\n: "${HOME:?HOME is not set}"\nfor p in "$HOME/skill-tutor-tutorials" "$HOME/.claude/commands/learn.md" "$HOME/.claude/commands/learn"; do\n  if [ -e "$p" ] || [ -L "$p" ]; then\n    echo "FOUND $p"\n    echo "  entries: $(find "$p" | wc -l | tr -d \' \')"\n    echo "  newest:  $(find "$p" -exec ls -ldt {} + | head -n 1)"\n    find "$p" -type l -exec ls -ld {} +\n  fi\ndone\n```\n\n```powershell\n$ErrorActionPreference = \'Stop\'\nif (-not $HOME) { throw \'HOME is not set\' }\nfunction Get-Entries([string]$Path) {\n  $item = Get-Item -LiteralPath $Path -Force\n  $item\n  if ($item.PSIsContainer -and -not $item.LinkType) {\n    Get-ChildItem -LiteralPath $Path -Force | ForEach-Object { Get-Entries $_.FullName }\n  }\n}\nforeach ($p in @((Join-Path $HOME \'skill-tutor-tutorials\'), (Join-Path $HOME \'.claude\\commands\\learn.md\'), (Join-Path $HOME \'.claude\\commands\\learn\'))) {\n  if (Get-Item -LiteralPath $p -Force -ErrorAction SilentlyContinue) {\n    $entries = @(Get-Entries $p)\n    "FOUND $p"\n    "  entries: $($entries.Count)"\n    "  newest:  $(($entries | Sort-Object LastWriteTime -Descending | Select-Object -First 1).LastWriteTime)"\n    $entries | Where-Object { $_.LinkType } | ForEach-Object { "  link: $($_.FullName) -> $($_.Target)" }\n  }\n}\n```\n\n- `find` without `-L` never follows a symlink: a symlink counts as **one** entry, and its target is printed next to it. The bash block uses only commands that behave the same on GNU (Linux, WSL) and BSD (macOS). The PowerShell block uses `Get-Item -Force`, which also finds a dangling symlink.\n- The entry count is always exact. For a very large folder, `find … -exec ls -ldt {} +` can split into batches, so the "newest" line is then only approximate.\n- **If nothing is found:** say, in Hebrew, "לא נמצאו שאריות מהתקנה קודמת." and continue to section 0.1.\n- **Otherwise:** show each path found with its entry count, its newest modification date and any symlink targets, and remember the counts for Step 4.\n\n### Step 2 — Ask\n\nUse `AskUserQuestion`:\n\n```\nquestion: "נמצאו קבצים מהתקנה קודמת של /learn. מה לעשות איתם?"\nheader: "ניקוי התקנה"\noptions:\n  - label: "להשאיר הכל"\n    description: "שום דבר לא זז. ממשיכים בהגדרה."\n  - label: "להעביר לגיבוי ולהתחיל מחדש"\n    description: "הכל עובר לתיקייה ~/skill-tutor-tutorials-backup-<תאריך>. שום דבר לא הולך לאיבוד."\n```\n\nOnly `להעביר לגיבוי ולהתחיל מחדש` is a yes. Any other answer, including free text, means keep: touch nothing and continue to section 0.1.\n\n### Step 3 — Move\n\nRun the whole move as **one single** Bash tool call (or one PowerShell call), never split across calls: shell variables do not survive between tool calls.\n\n```bash\n: "${HOME:?HOME is not set}"\nts=$(date +%Y%m%d-%H%M%S)\ndest="$HOME/skill-tutor-tutorials-backup-$ts"\n: "${dest:?dest is not set}"\nmkdir "$dest" && mkdir "$dest/commands" || exit 1\nif [ -e "$HOME/skill-tutor-tutorials" ] || [ -L "$HOME/skill-tutor-tutorials" ]; then mv "$HOME/skill-tutor-tutorials" "$dest/" || exit 1; fi\nif [ -e "$HOME/.claude/commands/learn.md" ] || [ -L "$HOME/.claude/commands/learn.md" ]; then mv "$HOME/.claude/commands/learn.md" "$dest/commands/" || exit 1; fi\nif [ -e "$HOME/.claude/commands/learn" ] || [ -L "$HOME/.claude/commands/learn" ]; then mv "$HOME/.claude/commands/learn" "$dest/commands/" || exit 1; fi\necho "BACKUP $dest"\nfor p in "$HOME/skill-tutor-tutorials" "$HOME/.claude/commands/learn.md" "$HOME/.claude/commands/learn"; do\n  if [ -e "$p" ] || [ -L "$p" ]; then echo "STILL PRESENT $p"; fi\ndone\nfor b in "$dest/skill-tutor-tutorials" "$dest/commands/learn.md" "$dest/commands/learn"; do\n  if [ -e "$b" ] || [ -L "$b" ]; then echo "IN BACKUP $b entries: $(find "$b" | wc -l | tr -d \' \')"; fi\ndone\n```\n\n```powershell\n$ErrorActionPreference = \'Stop\'\nif (-not $HOME) { throw \'HOME is not set\' }\nfunction Get-Entries([string]$Path) {\n  $item = Get-Item -LiteralPath $Path -Force\n  $item\n  if ($item.PSIsContainer -and -not $item.LinkType) {\n    Get-ChildItem -LiteralPath $Path -Force | ForEach-Object { Get-Entries $_.FullName }\n  }\n}\n$dest = Join-Path $HOME (\'skill-tutor-tutorials-backup-\' + (Get-Date -Format \'yyyyMMdd-HHmmss\'))\nif (-not $dest) { throw \'dest is not set\' }\nNew-Item -ItemType Directory -Path $dest | Out-Null\nNew-Item -ItemType Directory -Path (Join-Path $dest \'commands\') | Out-Null\n$moves = @(\n  @((Join-Path $HOME \'skill-tutor-tutorials\'), $dest),\n  @((Join-Path $HOME \'.claude\\commands\\learn.md\'), (Join-Path $dest \'commands\')),\n  @((Join-Path $HOME \'.claude\\commands\\learn\'), (Join-Path $dest \'commands\'))\n)\nforeach ($m in $moves) {\n  if (Get-Item -LiteralPath $m[0] -Force -ErrorAction SilentlyContinue) { Move-Item -LiteralPath $m[0] -Destination $m[1] -ErrorAction Stop }\n}\n"BACKUP $dest"\nforeach ($m in $moves) { if (Get-Item -LiteralPath $m[0] -Force -ErrorAction SilentlyContinue) { "STILL PRESENT $($m[0])" } }\nforeach ($b in @((Join-Path $dest \'skill-tutor-tutorials\'), (Join-Path $dest \'commands\\learn.md\'), (Join-Path $dest \'commands\\learn\'))) {\n  if (Get-Item -LiteralPath $b -Force -ErrorAction SilentlyContinue) { "IN BACKUP $b entries: $(@(Get-Entries $b).Count)" }\n}\n```\n\n- `mv` and `Move-Item` move a symlink as a link; they never follow it.\n- **On any error:** stop and report it. Never retry with force.\n- **Across filesystems** (e.g. `~/.claude/commands` is a symlink into `/mnt/c/…`), `mv` copies and then removes the original. An interruption leaves the original intact, or both copies, but never neither. So nothing is lost.\n\n### Step 4 — Verify and report\n\nCheck the output: no `STILL PRESENT` line, and each `IN BACKUP` entry count equals the count shown in Step 1. If anything differs, stop and report it. Otherwise tell the learner, in Hebrew, the backup path from the `BACKUP` line.\n\n### Step 5 — Continue or stop\n\n- If `~/.claude/commands/learn.md` or `~/.claude/commands/learn/` was moved: stop setup here. Tell the tester, in Hebrew, to close Claude Code, open it again in this repo and run `/learn setup` again. Do not continue in this session.\n- Otherwise continue to section 0.1.\n<!-- CLEAN-SLATE:END -->\n\n---\n\n## A. Show Current Settings',
    ),
]
EOF
````

- [ ] **Step 2: Verify.** Dev loop and findings. **Expected: `0 finding(s)`**, and pytest is fully green: `58 passed`. From here on, every task must stay green.

- [ ] **Step 3: Commit.** `git add -u .claude && git commit -m "feat(setup): temporary clean-slate step (move-only backup)"`

---

### Task 15 (T6): Claude Code version check (S14, RV3-M1)

**Files:** Modify `.claude/commands/learn/setup.md`: a new `## 0.1 Claude Code version` directly after the CLEAN-SLATE end marker and before `## A`, so first runs reach it (A says "skip directly to section B").

The floor appears **once**, on the `**Floor:** 2.1.176` line, so manual check 2b can change it with a single `sed`. The comparison example deliberately doesn't repeat the floor.

- [ ] **Step 1: Apply the edit:**

````bash
SCRATCH=…  # your scratchpad
uv run python "$SCRATCH/apply_edits.py" <<'EOF'
[
    (
        '.claude/commands/learn/setup.md',
        '''<!-- CLEAN-SLATE:END -->

---

## A. Show Current Settings''',
        '''<!-- CLEAN-SLATE:END -->

---

## 0.1 Claude Code version

*Runs on every `/learn setup`, including a first run with no settings file.*

**Floor:** 2.1.176

1. Run `claude --version`. If `claude` is not found (e.g. a Desktop-bundled install with no `claude` on PATH), skip this section silently and continue to section A.
2. Take the first `major.minor.patch` version in the output (e.g. `2.1.284 (Claude Code)` gives `2.1.284`).
3. Compare it with the floor **numerically, one component at a time**: major first, then minor, then patch. Never compare the two strings as text: `2.1.99` is lower than `2.1.100`, although it sorts higher as text.
4. If it is lower than the floor, show this warning in Hebrew, filling in both versions, then continue to section A:
   > "גרסת Claude Code שלך (<installed>) ישנה מהגרסה המינימלית שהקורס צריך (<floor>). כדי לעדכן, הריצו בטרמינל: `claude update`"
5. Otherwise continue to section A without a message.

*Limitation:* `claude --version` reports whichever `claude` comes first on PATH, which may not be the binary running this session.

---

## A. Show Current Settings''',
    ),
]
EOF
````

- [ ] **Step 2: Check.**

```bash
grep -c "2\.1\.176" .claude/commands/learn/setup.md
grep -n "^## " .claude/commands/learn/setup.md | head -4
```
Expected: `1`, then `## 0. Clean slate`, `## 0.1 Claude Code version`, `## A. Show Current Settings`, `## B. Session Language`.

- [ ] **Step 3: Verify.** Dev loop: green.

- [ ] **Step 4: Commit.** `git add -u .claude && git commit -m "feat(setup): warn when Claude Code is older than 2.1.176"`

---

### Task 16 (D): Remove the global install (item 8 + G2, RV3-L2)

**Files:** Modify `setup.md` (delete §F through its trailing separator, then re-letter "G. Setup Complete" to **F**), `README.md` (old `:46` and `:202`), `CLAUDE.md` (`:14` loses "global install"; delete step 4 at `:75`) and `CONTRIBUTING.md` (old `:61`). Existing `changes.md` sections stay unchanged.

- [ ] **Step 1: Apply the edits:**

````bash
SCRATCH=…  # your scratchpad
uv run python "$SCRATCH/apply_edits.py" <<'EOF'
[
    (
        '.claude/commands/learn/setup.md',
        '## F. Global Install (optional)\n\nBy default `/learn` works inside this repo — no install needed. Global install is only useful if the learner wants to run `/learn` from *other* projects (a future cross-repo use case).\n\n**Note the trade-off:** a global copy is a second source of truth. If the repo\'s modules are later edited, the global copy goes stale until re-synced. Most learners should say no.\n\nUse the `AskUserQuestion` tool:\n\n```\nquestion: "להתקין את /learn גם בפרויקטים אחרים? (רוב הלומדים: לא)"\nheader: "התקנה גלובלית"\noptions:\n  - label: "לא, רק בריפו הזה"\n    description: "/learn יעבוד בתוך הריפו. מומלץ — אין עותק כפול שעלול להתיישן."\n  - label: "כן, התקן גלובלית"\n    description: "אעתיק את המודולים ל-~/.claude/commands כדי שאפשר יהיה להשתמש מכל מקום."\n```\n\n**If no:** skip — confirm settings are saved and `/learn` is ready inside this repo.\n\n**If yes:** copy the skill files to the global Claude commands folder, then warn that future repo edits require re-running setup to re-sync.\n\n```powershell\n$dest = "$env:USERPROFILE\\.claude\\commands"\nif (!(Test-Path $dest)) { New-Item -ItemType Directory -Force -Path $dest | Out-Null }\nCopy-Item -Force "$PWD\\.claude\\commands\\learn.md" "$dest\\learn.md"\n\n$moduleDest = "$dest\\learn"\nif (!(Test-Path $moduleDest)) { New-Item -ItemType Directory -Force -Path $moduleDest | Out-Null }\nCopy-Item -Force "$PWD\\.claude\\commands\\learn\\*.md" "$moduleDest\\"\n```\n\n---\n\n',
        '',
    ),
    (
        '.claude/commands/learn/setup.md',
        '## G. Setup Complete — REQUIRED',
        '## F. Setup Complete — REQUIRED',
    ),
    (
        'README.md',
        '''- Optionally install `/learn` globally so it works in other projects (off by default — most learners keep it repo-local)
''',
        '',
    ),
    (
        'README.md',
        '''4. Update the global install command in `setup.md`
''',
        '',
    ),
    (
        'CLAUDE.md',
        '| הגדרות ראשוניות, קול, global install |',
        '| הגדרות ראשוניות, קול |',
    ),
    (
        'CLAUDE.md',
        '''4. (אופציונלי) אם ההתקנה הגלובלית מופעלת — עדכן את רשימת הקבצים שמועתקים ב-`setup.md` סעיף F. ברירת מחדל: `/learn` רץ מתוך הריפו בלבד, ללא התקנה גלובלית.
''',
        '',
    ),
    (
        'CONTRIBUTING.md',
        '''4. Update the global install `Copy-Item` command in `setup.md`
''',
        '',
    ),
]
EOF
````

- [ ] **Step 2: Check (the PR's grep, RV5-L6).**

```bash
grep -n "Global Install" .claude/commands/learn/setup.md
grep -rn "global install\|globally" README.md CLAUDE.md CONTRIBUTING.md .claude/commands/learn/setup.md
grep -n "^## F\. \|^## G\. " .claude/commands/learn/setup.md
```
Expected: no output, then no output, then only `## F. Setup Complete — REQUIRED`.

- [ ] **Step 3: Verify.** Dev loop: green.

- [ ] **Step 4: Commit.** `git add -u && git commit -m "docs: remove the global install"`

---

### Task 17 (D): Document the frontmatter (RV-L6)

**Files:** Modify the "add a module" steps in `README.md`, `CONTRIBUTING.md` (57–61) and `CLAUDE.md` ("הוספת מודול חדש"). Each gains one step.

- [ ] **Step 1: Apply the edits:**

````bash
SCRATCH=…  # your scratchpad
uv run python "$SCRATCH/apply_edits.py" <<'EOF'
[
    (
        'README.md',
        '''1. Create `.claude/commands/learn/[module-name].md`
2. Add a row to the modules table in `CLAUDE.md`
3. Add a routing entry in `learn.md` (Step 2 — Route table)
''',
        '''1. Create `.claude/commands/learn/[module-name].md`
2. Start the file with the `disable-model-invocation: true` frontmatter block (three lines: `---`, `disable-model-invocation: true`, `---`), so Claude never loads the module on its own
3. Add a row to the modules table in `CLAUDE.md`
4. Add a routing entry in `learn.md` (Step 2 — Route table)
''',
    ),
    (
        'CONTRIBUTING.md',
        '''1. Create `.claude/commands/learn/[module-name].md`
2. Add a routing entry in `.claude/commands/learn.md` (Step 2 — Route table)
3. Add a row to the modules table in `CLAUDE.md`
''',
        '''1. Create `.claude/commands/learn/[module-name].md`
2. Start the file with the `disable-model-invocation: true` frontmatter block (three lines: `---`, `disable-model-invocation: true`, `---`), so Claude never loads the module on its own
3. Add a routing entry in `.claude/commands/learn.md` (Step 2 — Route table)
4. Add a row to the modules table in `CLAUDE.md`
''',
    ),
    (
        'CLAUDE.md',
        '''1. צור קובץ ב-`.claude/commands/learn/[module-name].md`
2. הוסף שורה לטבלת ה-Modules למעלה
3. הוסף routing ב-`learn.md` (Step 2 — Route table)
''',
        '''1. צור קובץ ב-`.claude/commands/learn/[module-name].md`
2. התחל את הקובץ בבלוק ה-frontmatter של `disable-model-invocation: true` (שלוש שורות: `---`, `disable-model-invocation: true`, `---`), כדי שקלוד לא יטען את המודול בעצמו
3. הוסף שורה לטבלת ה-Modules למעלה
4. הוסף routing ב-`learn.md` (Step 2 — Route table)
''',
    ),
]
EOF
````

- [ ] **Step 2: Verify.** Dev loop: green.

- [ ] **Step 3: Commit.** `git add -u && git commit -m "docs: document the disable-model-invocation frontmatter"`

---

### Task 18 (D): README tester note (item 13, RV2-M2, RV4-L1)

**Files:** Modify `README.md`: under the title, between the TEMPORARY markers.

- [ ] **Step 1: Apply the edit:**

````bash
SCRATCH=…  # your scratchpad
uv run python "$SCRATCH/apply_edits.py" <<'EOF'
[
    (
        'README.md',
        '''# Tov-learn

''',
        "# Tov-learn\n\n<!-- TEMPORARY: remove at first-cohort gate (PRD D10) -->\n> **Testers: fresh install only.** Before testing, delete `~/skill-tutor-tutorials/` (`%USERPROFILE%\\skill-tutor-tutorials` on Windows) and any old global install at `~/.claude/commands/learn.md` and `~/.claude/commands/learn/` — or run `/learn setup`, which offers to move them into a backup for you. **If `~/.claude/commands/learn.md` exists and `/learn setup` doesn't offer to move it, you have an older global install: move or delete `~/.claude/commands/learn.md` and `~/.claude/commands/learn/` by hand, then restart Claude Code.**\n<!-- /TEMPORARY -->\n\n",
    ),
]
EOF
````

- [ ] **Step 2: Verify.** Dev loop: green.

- [ ] **Step 3: Commit.** `git add README.md && git commit -m "docs(readme): temporary tester note"`

---

### Task 19 (D): README version floor (S14, RV2-L6)

**Files:** Modify `README.md` "Step 1 — Prerequisites" (`:25`) and "Requirements" (`:208`). Don't mention uv.

- [ ] **Step 1: Apply the edits:**

````bash
SCRATCH=…  # your scratchpad
uv run python "$SCRATCH/apply_edits.py" <<'EOF'
[
    (
        'README.md',
        '- [Claude Code](https://claude.ai/code) installed (Pro plan or higher)',
        '- [Claude Code](https://claude.ai/code) 2.1.176 or later installed (Pro plan or higher)',
    ),
    (
        'README.md',
        '- Claude Code (Pro plan or higher)',
        '- Claude Code 2.1.176 or later (Pro plan or higher)',
    ),
]
EOF
````

- [ ] **Step 2: Verify.** Dev loop: green. Also run `grep -c "2.1.176" README.md` (expected `2`) and `grep -ci "uv" README.md` (expected `0`).

- [ ] **Step 3: Commit.** `git add README.md && git commit -m "docs(readme): Claude Code 2.1.176 or later"`

---

### Task 20 (D): Contributor test command (S12, RV2-L7, RV3-L2)

**Files:** Modify `CLAUDE.md` (a new contributors-only section at the end) and `CONTRIBUTING.md` "Pull Requests" (`:65-69`).

- [ ] **Step 1: Apply the edits:**

````bash
SCRATCH=…  # your scratchpad
uv run python "$SCRATCH/apply_edits.py" <<'EOF'
[
    (
        'CLAUDE.md',
        '''4. הוסף routing ב-`learn.md` (Step 2 — Route table)
''',
        '''4. הוסף routing ב-`learn.md` (Step 2 — Route table)

---

## בדיקות (למפתחי הקורס בלבד — contributors only)

לומדים לא צריכים את זה. מפתחי הקורס צריכים את [uv](https://docs.astral.sh/uv/getting-started/installation/); זו נקודת הכניסה היחידה הנתמכת לבדיקות:

```
uv run ruff check -q && uv run pytest -q
```

אם pytest אדום, הריצו שוב `uv run pytest -v` כדי לראות אילו בדיקות נכשלו. הבדיקות עצמן נמצאות ב-`tests/validate_structure.py`.
''',
    ),
    (
        'CONTRIBUTING.md',
        '''- Test the flow manually with `/learn` before opening the PR
''',
        '''- Test the flow manually with `/learn` before opening the PR
- Run `uv run ruff check -q && uv run pytest -q` before opening a PR (contributors need [uv](https://docs.astral.sh/uv/getting-started/installation/))
''',
    ),
]
EOF
````

- [ ] **Step 2: Verify.** Dev loop: green.

- [ ] **Step 3: Commit.** `git add CLAUDE.md CONTRIBUTING.md && git commit -m "docs: contributor test command (uv)"`

---

### Task 21 (D): What CI enforces, and the README aliases (RV3-M7, RV4-L9, RV5-L5)

**Files:** Modify `CONTRIBUTING.md` "Adding a Lesson" (13–35: one paragraph after step 4), and `README.md` `:72` plus the command table (`:113-124`).

- [ ] **Step 1: Apply the edits:**

````bash
SCRATCH=…  # your scratchpad
uv run python "$SCRATCH/apply_edits.py" <<'EOF'
[
    (
        'CONTRIBUTING.md',
        '''4. Update `courses/[course-name]/COURSE.md` with the new lesson row
''',
        '''4. Update `courses/[course-name]/COURSE.md` with the new lesson row

**CI checks every lesson** (see `tests/validate_structure.py`): each script has at least 5 `[מעבר שקף]` markers; the exercises' first heading contains `שיעור X.Y`, and any `**שיעור:**` line names the same lesson; `COURSE.md` has a row for the lesson and a correct module range; and spoken lesson references (e.g. "שתיים נקודה אחת") name lessons that exist. The example below predates these rules; F rewrites it.
''',
    ),
    (
        'README.md',
        'At any point you can type `quiz me` to test yourself, or `stop` to end the session',
        'At any point you can type `quiz me` (or `בוחן`) to test yourself, or `stop` (or `עצור` / `סיום`) to end the session',
    ),
    (
        'README.md',
        '| `continue` | Move to the next section |',
        '| `continue` / `המשך` | Move to the next section |',
    ),
    (
        'README.md',
        '| `quiz me` | 4-question quiz on everything covered so far |',
        '| `quiz me` / `בוחן` | 4-question quiz on everything covered so far |',
    ),
    (
        'README.md',
        "| `stop` | End session — shows what's covered, what's left, next recommendation |",
        "| `stop` / `עצור` / `סיום` | End session — shows what's covered, what's left, next recommendation |",
    ),
]
EOF
````

- [ ] **Step 2: Verify.** Dev loop: green.

- [ ] **Step 3: Commit.** `git add CONTRIBUTING.md README.md && git commit -m "docs: what CI enforces, and the Hebrew aliases"`

---

### Task 22 (D, last): `changes.md` (S11, S18)

**Files:** Modify `changes.md`: append three sections after the existing ones, in the current style (an Overview, numbered `##` entries with Before/After, and a File Map):
1. #12
2. #13
3. `fix/stage0-quick-wins`, with the **Testers** note

The docs PR gets no section (S18). Earlier PRs without sections are left for F.

- [ ] **Step 1: Append:**

````bash
cat >> changes.md <<'EOF'

---

# Changes — fix/lesson-1.8-workers-ai-exercise branch

PR #12, merged 2026-09-28.

## Overview

Repairs the Workers AI exercise in lesson 1.8, which did not compile and used a deprecated model, and moves Cloudflare config references from `wrangler.toml` to `wrangler.jsonc`, the current default.

---

## 1. Lesson 1.8 exercise 7 (AI on the Edge)

**Before:** the `src/index.ts` sample failed TypeScript strict-mode compilation (`request.json()` was untyped), called the deprecated Workers AI model `@cf/meta/llama-2-7b-chat-int8`, and configured the binding in `wrangler.toml`.

**After:**
- `request.json()` is cast to `{ text: string }`, so the sample compiles in strict mode.
- The model is `@cf/meta/llama-3.1-8b-instruct-fp8`, with an inline pointer to Cloudflare's model list.
- An instructor note (an HTML comment, not read to the learner) says to confirm the model ID before teaching and to swap in a current model if it has been deprecated.
- The AI binding is configured in `wrangler.jsonc`.
- The same fix was applied to the archived copy (`courses/_archive/…/3.8_exercises.md`).

## 2. `wrangler.jsonc` references

**Before:** `cli-first.md` and project C in `projects.md` pointed to `wrangler.toml`.

**After:** both use `wrangler.jsonc`, including project C's Cron Trigger config and its checklist line.

---

## File Map

| File | Status | Purpose |
|------|--------|---------|
| `courses/ai-dev/lessons/01-claude-code/1.8-deploy-production/1.8_exercises.md` | Modified | Exercise 7: strict-mode cast, current model, instructor note, `wrangler.jsonc` binding |
| `courses/_archive/ai-engineer/lessons/03-vibe-coding/3.8-deploy-production/3.8_exercises.md` | Modified | The same fix in the archived course |
| `courses/ai-dev/lessons/03-final-project/projects.md` | Modified | Project C: Cron Trigger in `wrangler.jsonc` |
| `.claude/commands/learn/cli-first.md` | Modified | Reproducibility example uses `wrangler.jsonc` |

---

# Changes — fix/lesson-2.5-2.6-content-corrections branch

PR #13, merged 2026-09-28.

## Overview

Corrects outdated API details in lessons 2.5 and 2.6.

---

## 1. Lesson 2.5 exercise 3 (currency converter)

**Before:** the exercise called a defunct Bank of Israel endpoint and read a `rate` field that no longer exists; the instructions converted in the wrong direction.

**After:** it calls `https://boi.org.il/PublicApi/GetExchangeRate?key=USD`, reads `currentExchangeRate` divided by `unit`, and states that the rate is shekels per one dollar, so shekels ÷ rate = dollars.

## 2. Lesson 2.6 script (filesystem MCP server)

**Before:** the script narrated installing the filesystem MCP server with `pip`, contradicting the exercises.

**After:** the script connects the server through Claude Code (`claude mcp add`), matching the exercises, which run the official Node.js package with `npx`.

---

## File Map

| File | Status | Purpose |
|------|--------|---------|
| `courses/ai-dev/lessons/02-claude-api/2.5-python-patterns/2.5_exercises.md` | Modified | Current Bank of Israel endpoint and fields; conversion direction |
| `courses/ai-dev/lessons/02-claude-api/2.6-mcp/2.6_script.txt` | Modified | MCP server added through Claude Code, not `pip` |

---

# Changes — fix/stage0-quick-wins branch

Stage 0 of the project redesign (the "quick-win PR"). Spec: `docs/superpowers/specs/2026-09-27-stage0-quick-wins-design.md`.

## Overview

Fixes what testers hit now (wrong course name, missing lessons, a broken hook, an unsafe lab, deprecated Supabase keys, stale lesson cross-references), adds the first CI lints, and moves CI to `node24` actions on uv + pytest + ruff.

**Testers:** reset your data before testing this branch: delete `~/skill-tutor-tutorials/`, or run `/learn setup` and choose the backup option.

---

## 1. `COURSE.md` lists lessons 2.1 and 2.2

**Before:** module 02 listed only 2.3–2.6, so `/learn` resume skipped from 1.8 to 2.3.

**After:** rows for 2.1 and 2.2, and the module range is 2.1–2.6.

## 2. PowerShell Stop hook removed

**Before:** `.claude/settings.json` ran a PowerShell Stop hook, which showed a "hook error" after every reply on macOS and Linux.

**After:** `.claude/settings.json` is `{}`. (`auto-save-progress.ps1` stays until unit M.)

## 3. Israeli VAT is 18%

**Before:** seven places in lessons 1.3, 2.2 and 2.6 used 17% (including `vat_rate = 0.17`).

**After:** all seven use 18%.

## 4. Lesson 0.4 splits into slides

**Before:** 0.4 used `[SLIDE TRANSITION]`, which the tutor does not recognise, so the lesson was one slide.

**After:** all 19 markers are `[מעבר שקף]`.

## 5. Archive residue removed from course content

**Before:** the course called itself "AI Engineer"; lesson headers and spoken lesson numbers used the archived course's numbering (e.g. "שלוש נקודה ארבע" for 1.4, "חמש נקודה שתיים" for 2.2); scripts pointed to lessons and modules that don't exist; three exercise files began with a leaked AI preamble.

**After:** "AI Dev" throughout (the job title "AI Engineer" stays); every header and spoken lesson number names the real lesson; the dead cross-references are replaced with bridges between the real modules; the preambles are gone.

## 6. Lesson 1.3 hook exercise is safe

**Before:** exercise 5 asked for a Bash hook that prompts for Y/N (hooks have no terminal), with no exit code, in global settings; the script claimed exit code 1 blocks.

**After:** a project-scoped PreToolUse hook blocks *reading* a fake secret (`if: "Read(secret-demo.txt)"`, exit 2), then a `cat` in the terminal shows the bypass. Nothing is written or deleted. The script explains that only exit 2 blocks. The lesson needs Claude Code 2.1.176 or later.

## 7. Supabase keys and MCP in lesson 1.6

**Before:** the deprecated anon/service_role keys, and an invalid `claude mcp add` command.

**After:** `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` / `SUPABASE_SECRET_KEY`; the hosted MCP server added read-only at project scope, then authenticated through `claude /mcp`. The exercise inserts its sample row in the Table Editor, not through MCP.

## 8. Old project B moved out

**Before:** `projects.md` offered project B (Document Intelligence Service).

**After:** it lives, unwired, in `03-final-project/old_B-document-intelligence.md`. It is not the new track B.

## 9. Tutor: sub-modules can't be auto-invoked

**Before:** Claude could load any `learn/*.md` sub-module on its own.

**After:** all 15 start with `disable-model-invocation: true`.

## 10. Tutor: Hebrew aliases

**After:** `המשך` = continue, `בוחן` / `בוחן מלא` = quiz me / quiz me full, `עצור` / `סיום` = stop. "בחן אותי" still switches to diagnostic mode.

## 11. Tutor: no final project until unit 1e

**Before:** `/learn project` and resume offered the final projects, which are being rebuilt.

**After:** `/learn project` says they are being rebuilt and points back to the lessons; resume no longer offers them.

## 12. Tutor: `/learn security` asks first

**Before:** it scanned any URL; its `timingSafeEqual` sample returned a 500 on keys of a different length.

**After:** it asks whether the app is the learner's (or they have permission) and makes no request unless they say yes; the sample compares SHA-256 digests.

## 13. Setup: temporary clean-slate step

**After:** `/learn setup` looks for leftovers at exactly `~/skill-tutor-tutorials/`, `~/.claude/commands/learn.md` and `~/.claude/commands/learn/`, shows them, and on an explicit yes moves them into `~/skill-tutor-tutorials-backup-<date>`. Nothing is deleted. Removed at the first-cohort gate.

## 14. Setup: Claude Code version check

**After:** `/learn setup` warns when `claude --version` is below 2.1.176 (compared numerically).

## 15. Global install removed

**Before:** setup offered to copy `/learn` into `~/.claude/commands`, creating a stale second copy.

**After:** the option is gone from `setup.md`, README, CONTRIBUTING and CLAUDE.md.

## 16. Docs

- README: a temporary tester note; Claude Code 2.1.176 or later; the Hebrew aliases.
- The "add a module" steps (README, CONTRIBUTING, CLAUDE.md) include the frontmatter block.
- CLAUDE.md (contributors only) and CONTRIBUTING: the test command `uv run ruff check -q && uv run pytest -q`.
- CONTRIBUTING: what CI now checks for every lesson.

## 17. CI and contributor toolchain

**Before:** `validate.yml` used `checkout@v4` and `setup-python@v5` (both `node20`, retired on runners) and ran a script with 4 checks.

**After:** SHA-pinned `actions/checkout` v7.0.1 and `astral-sh/setup-uv` v10.2.0 (`node24`), `permissions: contents: read`, and `uv sync --locked` → `ruff check` → `pytest`. The lints are `check_*` functions in `tests/validate_structure.py`, each proven by a seeded regression in `tests/test_validate_structure.py`. Dependabot keeps the action pins fresh. uv is required for contributors only; learners never need it.

---

## File Map

| File | Status | Purpose |
|------|--------|---------|
| `pyproject.toml`, `uv.lock` | New | Contributor toolchain: Python 3.14, pytest, ruff |
| `tests/validate_structure.py` | Rewritten | The lints, as a library of `check_*` functions |
| `tests/test_validate_structure.py` | New | Seeded regressions, must-pass negatives, real-repo check |
| `.github/workflows/validate.yml` | Modified | node24 actions, uv, least privilege |
| `.github/dependabot.yml` | New | Weekly `github-actions` updates |
| `.gitignore` | Modified | Python caches and `.venv/` |
| `.claude/settings.json` | Modified | `{}` |
| `.claude/commands/learn.md` | Modified | Aliases; project route wording |
| `.claude/commands/learn/*.md` (15 files) | Modified | `disable-model-invocation: true` frontmatter |
| `.claude/commands/learn/setup.md` | Modified | Clean-slate step, version check, global install removed |
| `.claude/commands/learn/security.md` | Modified | Ownership gate, digest comparison |
| `.claude/commands/learn/project.md`, `resume.md` | Modified | No final project until unit 1e |
| `.claude/commands/learn/progress.md` | Modified | Hebrew stop triggers |
| `courses/ai-dev/COURSE.md` | Modified | Lessons 2.1 and 2.2 |
| `courses/ai-dev/lessons/**` | Modified | VAT, 0.4 markers, residue, 1.3 hook exercise, 1.6 Supabase |
| `courses/ai-dev/lessons/03-final-project/old_B-document-intelligence.md` | New | Old project B, unwired |
| `README.md`, `CLAUDE.md`, `CONTRIBUTING.md` | Modified | Docs above |
EOF
````

- [ ] **Step 2: Check.**

```bash
grep -n "^# Changes" changes.md
```
Expected: five headings, in this order: `yuval_ver`, `sean_changes`, `fix/lesson-1.8-workers-ai-exercise`, `fix/lesson-2.5-2.6-content-corrections`, `fix/stage0-quick-wins`.

- [ ] **Step 3: Verify.** Dev loop: fully green (`58 passed`, ruff silent, `0 finding(s)`).

- [ ] **Step 4: Commit.** `git add changes.md && git commit -m "docs(changes): sections for #12, #13 and fix/stage0-quick-wins"`

---

### Task 23: Automated evidence for the PR (spec §6.2)

**Files:** none. Collect outputs into `$SCRATCH/evidence.md` for the PR description.

- [ ] **Step 1: Test run and IDs.**

```bash
uv run ruff check -q; echo "ruff exit $?"
uv run pytest -q 2>&1 | tail -1
uv run pytest --collect-only -q
```
Expected: `ruff exit 0`; `58 passed`; 58 test IDs.

- [ ] **Step 2: The three greps.**

```bash
grep -rnE "17%|0\.17|שבעה עשר" courses/ai-dev; echo "vat grep exit $?"
for f in .claude/commands/learn/*.md; do head -3 "$f"; done
grep -n "Global Install" .claude/commands/learn/setup.md; echo "global grep exit $?"
```
Expected: `vat grep exit 1` (nothing found); 15 identical frontmatter blocks; `global grep exit 1`.

- [ ] **Step 3: Branch sanity.**

```bash
git log --oneline master..HEAD | wc -l
git status --short
ls .python-version 2>&1
```
Expected: `22`; clean; `No such file or directory`.

- [ ] **Step 4: Final branch review by a fresh Opus 5.5 subagent.**
  - Run `free -h` first. If `available` is below about 1.5 GB, tell the user and stop.
  - Spawn **one** fresh subagent. Not a fork: it must carry no context from your session. Use `model: opus` (Opus 5.5) and a read-only agent type with no Edit/Write tools and no Agent tool (e.g. `Plan`).
  - Brief it neutrally, with file paths only: the worktree `/home/emanresu/Tov-learn-stage0`, `git diff master...HEAD`, the spec and this plan. The task: "Review this branch against the locked spec and the plan; find bugs, deviations from the spec, missing items, unsafe changes and wrong facts; rank findings by severity with evidence." It reviews as a single agent (no subagents, no splitting by angle) and changes nothing.
  - **Relay its findings to the user unfiltered before changing anything.** Fix only what the user approves. Each fix is its own commit, with the dev loop green, only with the user's commit authorization. Then rerun Steps 1–3.

---

### Task 24: Manual verification (spec §6.2 checks 0 → 2a → 2b → 1 → 3 → 2 → 4 → 5 → 6)

The **user** runs these interactively. Headless `claude -p` can't exercise `AskUserQuestion` or show hook-error notices reliably (S8). Your job: give the user each check's commands one at a time, in this order, and record in `$SCRATCH/evidence.md` for each check:
- steps
- date
- OS/shell (WSL2 Ubuntu, bash)
- Claude Code version (`claude --version`)
- who ran it
- result
- cleanup done
- every permission prompt shown
- the settings hash printed by check 0

Run Claude Code **from the worktree** (`cd /home/emanresu/Tov-learn-stage0 && claude`), except check 4.

**Rules for every check:**
- **Permission prompts (RV2-L1, RV5-L8).** At every prompt, in **every** check, answer "Yes" (once). Never answer "Yes, and don't ask again": from v2.1.211, that approval is saved to the **main checkout's** `.claude/settings.local.json`, even from a worktree session. Write each prompt down.
- **Isolation (RV3-M2, RV4-M4a, RV5-M3).** Run check 0 before **every** check that touches `$HOME` (2a, 2b, 1, 3, 5, 6) and again after its cleanup.
- **Cleanup deletes only what the check created.** Every fixture folder gets a sentinel file, `.stage0-fixture`, and every `rm -r` is guarded by it. If a guard fails, **stop**: that folder isn't a fixture.
- **Aside and restore.** Anything moved aside in check 0a stays aside for the **whole** of Task 24. It's restored once, in the final "Restore" step, after the last cleanup.
- **Never touch** `/mnt/c/Users/…/skill-tutor-tutorials`. Run every check from WSL/Linux.

#### Check 0a — Once, before the first check: move leftovers aside, record the settings hash

```bash
case "$HOME" in /mnt/*) echo "STOP: HOME is on the Windows side";; esac
aside=""
for p in "$HOME/skill-tutor-tutorials" "$HOME/.claude/commands/learn.md" "$HOME/.claude/commands/learn"; do
  if [ -e "$p" ] || [ -L "$p" ]; then
    [ -n "$aside" ] || { aside="$HOME/stage0-manual-check-aside-$(date +%Y%m%d-%H%M%S)"; mkdir "$aside" || exit 1; }
    mv "$p" "$aside/" && echo "MOVED ASIDE: $p -> $aside/"
  fi
done
echo "aside=${aside:-none}"
sha256sum /home/emanresu/Tov-learn/.claude/settings.local.json
```
Expected on this machine: no `STOP`, no `MOVED ASIDE`, `aside=none`, and one hash line. Record the `aside=` value and the hash in `$SCRATCH/evidence.md`: that hash is the **baseline**.

#### Check 0 — Precondition (before every `$HOME` check, and after its cleanup)

```bash
for p in "$HOME/skill-tutor-tutorials" "$HOME/.claude/commands/learn.md" "$HOME/.claude/commands/learn"; do
  if [ -e "$p" ] || [ -L "$p" ]; then echo "PRESENT: $p"; fi
done
ls -ld "$HOME/.claude/commands" 2>&1
ls -d "$HOME"/skill-tutor-tutorials-backup-* 2>/dev/null
sha256sum /home/emanresu/Tov-learn/.claude/settings.local.json
```
Expected:
- no `PRESENT` line
- `ls: cannot access …/.claude/commands` (it doesn't exist on this machine)
- no backup folder listed
- the **baseline** hash

A `PRESENT` line or a different hash means a check leaked state or an approval was persisted. **Stop** and tell the user before running the next check.

#### Check 2a — Version check on a first run (RV3-M1)

1. Run check 0.
2. In the worktree, run `claude`, then `/learn setup`.
3. Expected: step 0 prints "לא נמצאו שאריות מהתקנה קודמת." Step 0.1 runs `claude --version` (e.g. 2.1.284 ≥ 2.1.176) and shows **no warning**. Setup then reaches section B (the language question).
4. Press Esc at section B and quit Claude Code. Nothing is written before section E.
5. Cleanup: nothing was created. Run check 0.

#### Check 2b — Version-check warning branch (RV4-M4b, RV5-M2)

A PATH shim can't work on this machine (see Global Constraints), so raise the floor temporarily instead. `2.1.1000` is numerically above the installed version but sorts *below* it as text:

```bash
cd /home/emanresu/Tov-learn-stage0
grep -n '^\*\*Floor:\*\* 2\.1\.176$' .claude/commands/learn/setup.md
sed -i 's/^\*\*Floor:\*\* 2\.1\.176$/**Floor:** 2.1.1000/' .claude/commands/learn/setup.md
git diff --stat
```
Expected: one match, then `1 file changed, 1 insertion(+), 1 deletion(-)`.
1. Run check 0.
2. Run `claude`, then `/learn setup`. Expected: step 0.1 shows the Hebrew warning with both versions and `claude update`, then **continues** to A/B. That proves the comparison is numeric.
3. Press Esc, then quit.
4. Restore the file:
```bash
git checkout -- .claude/commands/learn/setup.md && git diff --exit-code && echo RESTORED
```
Expected: `RESTORED`. Then run check 0.

#### Check 1 — Resume offers 2.1 after 1.8 (done-when row 2)

1. Run check 0.
2. Create the fixtures:
```bash
T="$HOME/skill-tutor-tutorials"; mkdir -p "$T/progress" && touch "$T/.stage0-fixture"
cat > "$T/settings.json" <<'EOF'
{
  "session": { "language": "he", "address": "neutral" },
  "course": { "name": "ai-dev", "path": "courses/ai-dev/lessons" },
  "tts": { "enabled": false },
  "learning_style": { "mode": "standard", "detail_level": 2 }
}
EOF
cat > "$T/learner_profile.md" <<'EOF'
# Learner Profile

Background: Stage 0 manual-check fixture.

## Lessons Studied
| Lesson | Title | Score | Last Date |
|--------|-------|-------|-----------|
| 1.8 | Deploy לפרודקשן | 9/10 | 28-09-2026 |
EOF
for n in 0.1 0.2 0.3 0.4 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8; do
  printf '# Progress: Lesson %s\n\n## Sessions\n| Date | Sections Covered | Quiz Score | Notes |\n|------|-----------------|-----------|-------|\n| 28-09-2026 | all | 9/10 | fixture |\n\nNext recommended review: 26-12-2026\n' "$n" > "$T/progress/lesson-$n.md"
done
find "$T" -type f | sort
```
Expected: 15 files (the sentinel, `settings.json`, `learner_profile.md` and 12 progress files).
3. In the worktree, run `claude`, then `/learn` (no arguments). Expected: the suggestion offers **lesson 2.1** as the next new lesson, and there is **no 🏗️ line**.
4. Quit. Cleanup:
```bash
T="$HOME/skill-tutor-tutorials"; find "$T" -type f | sort
[ -f "$T/.stage0-fixture" ] && rm -r "$T" || echo "STOP: $T is not a fixture folder"
```
Before the `rm`, the list must show only the 15 fixture files plus anything this session wrote (e.g. `topics/knowledge_map.md`). Then run check 0.

#### Check 3 — Clean-slate (done-when row 6; RV-H5, RV2-L1, RV5-L1)

1. Run check 0. Then, in one terminal, set these variables and create the fixtures. Keep that terminal open for the whole check:
```bash
WT=/home/emanresu/Tov-learn-stage0
H0=$(sha256sum /home/emanresu/Tov-learn/.claude/settings.local.json)
[ -d "$HOME/.claude/commands" ] && CMD_EXISTED=1 || CMD_EXISTED=0; echo "CMD_EXISTED=$CMD_EXISTED"
ls "$WT/.claude/settings.local.json" 2>&1
mkdir -p "$HOME/skill-tutor-tutorials" && touch "$HOME/skill-tutor-tutorials/.stage0-fixture"
mkdir -p "$HOME/.claude/commands/learn" && echo fixture > "$HOME/.claude/commands/learn/fixture.md"
cp "$WT/.claude/commands/learn.md" "$HOME/.claude/commands/learn.md"
```
Expected: `CMD_EXISTED=0`, and `ls` reports no such file (the worktree has no local settings file).
2. **Keep run.** `cd "$WT" && claude`, then `/learn setup`. Expected: step 0 lists all three paths: `skill-tutor-tutorials` with 2 entries, `learn.md` with 1, `learn` with 2. Answer `להשאיר הכל`, then **press Esc right away** (RV5-L1), so no `settings.json` or `learner_profile.md` is written. Quit. Check: `ls -A "$HOME/skill-tutor-tutorials" "$HOME/.claude/commands" "$HOME/.claude/commands/learn"` shows only the fixtures.
3. **Move run.** `cd "$WT" && claude` again, then `/learn setup`, and answer `להעביר לגיבוי ולהתחיל מחדש`. Expected: one Bash call does the move; the output has `BACKUP …`, no `STILL PRESENT`, and `IN BACKUP` counts of 2, 1 and 2; the tutor prints the backup path and tells you to restart and rerun `/learn setup`, then stops. Quit.
4. Check, in the same terminal:
```bash
B=$(ls -d "$HOME"/skill-tutor-tutorials-backup-* | tail -1); echo "$B"
find "$B" | sort
for p in "$HOME/skill-tutor-tutorials" "$HOME/.claude/commands/learn.md" "$HOME/.claude/commands/learn"; do [ -e "$p" ] && echo "STILL THERE: $p"; done
git -C "$WT" status --short
ls "$WT/.claude/settings.local.json" 2>&1
[ "$H0" = "$(sha256sum /home/emanresu/Tov-learn/.claude/settings.local.json)" ] && echo "HASH UNCHANGED"
```
Expected:
- `find` lists exactly `$B`, `$B/skill-tutor-tutorials`, `…/.stage0-fixture`, `$B/commands`, `$B/commands/learn.md`, `$B/commands/learn` and `…/learn/fixture.md`
- no `STILL THERE`
- empty `git status`
- no local settings file in the worktree
- `HASH UNCHANGED`
5. Cleanup. Run it only after the `find` above shows nothing but the fixtures:
```bash
[ -f "$B/skill-tutor-tutorials/.stage0-fixture" ] && [ -f "$B/commands/learn/fixture.md" ] && rm -r "$B" || echo "STOP: $B is not the fixture backup"
[ "$CMD_EXISTED" = 0 ] && rmdir "$HOME/.claude/commands"
```
Then run check 0.

#### Check 2 — No hook error after replies (done-when row 4)

1. In the worktree, run `claude` and send two short messages (e.g. "hi", then "thanks").
2. Expected: no "hook error" notice after either reply. If one appears, run `/hooks` to see which settings file it came from, and record it. The user's global `~/.claude/settings.json` is a symlink into `/mnt/c`, so a hook there isn't this repo's.

#### Check 4 — 1.3 exercise 5 (Linux/bash), in a lab outside the repo (RV5-L9)

```bash
LAB="$HOME/stage0-lab-$(date +%Y%m%d-%H%M%S)"; mkdir -p "$LAB/.claude" && cd "$LAB" && touch .stage0-fixture
printf 'FAKE_API_KEY=not-a-real-key\n' > secret-demo.txt
printf 'just notes\n' > notes.txt
cat > .claude/settings.json <<'EOF'
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
EOF
claude
```
In that session:
1. Ask in words (no `@` mention): "read the file secret-demo.txt". Expected: the read is blocked and Claude repeats the reason. If Claude tries the terminal on its own, record that (it's step 5 happening early).
2. Ask: "read notes.txt". Expected: it works.
3. Ask: "run `cat secret-demo.txt` in the terminal". Expected: the fake key appears, or Claude declines. **Record which one happened.**

Cleanup: quit, then:
```bash
cd ~ && [ -f "$LAB/.stage0-fixture" ] && rm -r "$LAB" || echo "STOP: $LAB is not the lab"
```
Claude Code's own session logs under `~/.claude/projects/` stay.

#### Check 5 — Security gate (item 6)

1. Run check 0.
2. Create only the sentinel, `settings.json` and `learner_profile.md`, exactly as in check 1 step 2, without the `progress/` files (`mkdir -p "$T"` instead of `"$T/progress"`). Then `find "$HOME/skill-tutor-tutorials" -type f`: 3 files.
3. In the worktree, run `claude`, then `/learn security https://example.com`, and answer `לא` to the ownership question.
4. Expected: a short explanation (without permission it can cause harm and may be illegal), a suggestion to rerun with your own app's URL, and the module ends. **No `curl` or other network tool call** appears in the transcript.
5. Cleanup: quit, then:
```bash
T="$HOME/skill-tutor-tutorials"; find "$T" -type f | sort
[ -f "$T/.stage0-fixture" ] && rm -r "$T" || echo "STOP: $T is not a fixture folder"
```
Then run check 0.

#### Check 6 — Aliases and project (items 7 and 12; RV2-L12, RV5-M3)

1. Run check 0.
2. Create the same three fixture files as in check 5.
3. In the worktree, run `claude`, then `/learn 0.1`. After the first section:
   - Type `בוחן`. Expected: a quiz starts. Answer it or skip it.
   - Type `עצור`. Expected: progress is saved (the session-end summary) and files appear under `~/skill-tutor-tutorials/`.
   - Run `/learn 0.1` again and type `בחן אותי`. Expected: it switches to **diagnostic** mode, not a quiz.
   - Run `/learn project`. Expected: only the "being rebuilt, continue with the lessons" message; no project list.
4. Cleanup: quit, then:
```bash
T="$HOME/skill-tutor-tutorials"; find "$T" -type f | sort
[ -f "$T/.stage0-fixture" ] && rm -r "$T" || echo "STOP: $T is not a fixture folder"
```
Before the `rm`, the list must show only the fixtures plus the progress/tutorial/knowledge-map files this session wrote. Then run check 0.

#### Restore — Once, after check 6

Only if check 0a recorded an `aside=` folder (with `none`, skip this step):
```bash
aside=<the folder recorded in check 0a>
ls -A "$aside"
for n in skill-tutor-tutorials learn.md learn; do
  [ -e "$aside/$n" ] || [ -L "$aside/$n" ] || continue
  case "$n" in skill-tutor-tutorials) dst="$HOME/";; *) mkdir -p "$HOME/.claude/commands" && dst="$HOME/.claude/commands/";; esac
  [ -e "$dst$n" ] && { echo "STOP: $dst$n exists"; continue; }
  mv "$aside/$n" "$dst" && echo "RESTORED: $dst$n"
done
rmdir "$aside"
```
Then run check 0 one last time. Its `PRESENT` lines must match exactly what check 0a moved aside, and the hash must still equal the baseline.

---

### Task 25: Push and open the PR (only when the user asks)

**Files:** none.

- [ ] **Step 1: Ask the user** whether to push `fix/stage0-quick-wins` and open the PR. Don't proceed without a yes.

- [ ] **Step 2: Push and open it as a draft.**

```bash
git push -u origin fix/stage0-quick-wins
gh pr create --draft --base master --head fix/stage0-quick-wins --title "Stage 0: quick-win PR (content fixes, first CI lints, node24 CI)" --body-file "$SCRATCH/pr-body.md"
```
Write `$SCRATCH/pr-body.md` first, with the sections in Step 4.

- [ ] **Step 3: CI evidence (RV4-M3).**

```bash
run_id=$(gh run list --branch fix/stage0-quick-wins --workflow validate.yml --event pull_request --limit 1 --json databaseId --jq '.[0].databaseId')
echo "run_id=${run_id:-none yet}"
gh run watch "$run_id" --exit-status
job_id=$(gh run view "$run_id" --json jobs --jq '.jobs[0].databaseId')
gh api "repos/TovTechOrg/Tov-learn/check-runs/$job_id/annotations"
```
The run may not be queued yet right after `gh pr create`. If `run_id` is empty, don't call `gh run watch ""`. Wait with the Monitor tool (foreground `sleep` is blocked in Claude Code) on `until [ -n "$(gh run list --branch fix/stage0-quick-wins --workflow validate.yml --event pull_request --limit 1 --json databaseId --jq '.[0].databaseId')" ]; do sleep 10; done`, then rerun the block.

**Pass condition:** the run succeeds, and **no annotation mentions `Node.js 20` or `node20`**. The notice "The ubuntu-latest label will migrate to Ubuntu 26 beginning October 19, 2026" is expected and doesn't fail the check (`runs-on: ubuntu-latest` is kept by user decision). Paste the annotations output into the PR.

- [ ] **Step 4: PR description (spec §6.2).** Required sections:
  - **Summary:** every item 1–16, G1/G2/G4, and each RV-* through RV5-* fix (spec rev 6.1, PR-S4), each mapped to its commit (`git log --oneline master..HEAD`). Link the three new `changes.md` sections.
  - **Automated verification:** everything from Task 23 (the pytest result and the 58 test IDs, ruff clean, the VAT grep, the frontmatter grep, the Global Install grep), plus the Actions run and annotations from Step 3.
  - **Manual verification:** the Task 24 record for checks 0 → 2a → 2b → 1 → 3 → 2 → 4 → 5 → 6.
  - **Untested (stated explicitly):**
    - the native-PowerShell hook variant
    - the 1.6 MCP add + Authenticate flow, unless a contributor with a Supabase project runs it
    - the version check on Desktop-bundled installs (it skips), and the PATH-binary limitation (`claude --version` may not be the running binary; RV3-L4)
    - the bash clean-slate variant on macOS (portable commands, but run only on Linux/WSL; RV5-L3)
    - the PowerShell clean-slate variant (lint-checked for delete verbs, never run on Windows; RV3-M3)
  - **Future concerns:** spec §9.
  - **Reviewer note:** Hebrew changes need a Hebrew-speaking contributor's approval.

  Then `gh pr edit --body-file "$SCRATCH/pr-body.md"`. Mark the PR ready only when the user says so.

---

## Spec coverage map

| Spec | Task |
|---|---|
| §1 baseline guard, manual worktree | 0 |
| §5.1–§5.5 validator, tests, pyproject, lock, .gitignore, CI, Dependabot (S6, S9, S12, S13, S15, S17, S19, S20) | 1 |
| Item 2 | 2 |
| Item 1 | 3 |
| Item 3 (7 occurrences) | 4 |
| Item 4 | 5 |
| Item 5 + G1 + RV-M1 + RV2-M6 (full inventory, §4.2) | 6 |
| Item 10 + RV-L2 + S14 script/exercise edits | 7 |
| Item 16 + S16 + RV-M6 | 8 |
| Item 12 content (old B) | 9 |
| Item 11 | 10 |
| Item 7 (S2, RV5-L7) | 11 |
| Item 12 tutor + G4 + RV4-L3 | 12 |
| Item 6 (RV2-L10) | 13 |
| Item 14 (S4, S5, RV3-M4, RV5-M5, RV5-L3) | 14 |
| S14 version check (RV2-L2, RV3-M1, RV3-L4) | 15 |
| Item 8 + G2 (RV3-L2) | 16 |
| RV-L6 | 17 |
| Item 13 (RV2-M2, RV4-L1) | 18 |
| S14 README floor (RV2-L6) | 19 |
| Test command (S12, RV2-L7, RV3-L2) | 20 |
| RV3-M7 + README aliases | 21 |
| S11, S18 changes.md | 22 |
| §6.2 automated evidence | 23, 25 |
| §6.2 manual checks, order and isolation (RV3-M2, RV4-M4a, RV5-M3) | 24 |
| §6.2 PR description, untested list | 25 |
| §6.3 done-when → proof | 1 (seeds), 3 + check 1, 5, 2 + check 2, 25 (annotations), 14 + check 3 |
