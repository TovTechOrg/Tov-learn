"""Hook tests for the stuck and lesson-order hooks (.claude/scripts).

Runs each hook the way Claude Code does (documented exec form: powershell.exe -NoProfile
-ExecutionPolicy Bypass -WindowStyle Hidden -File <script>), with the hook input as UTF-8 JSON on
stdin. Uses a fake course and a fake USERPROFILE in a temporary folder (with Hebrew in the path, like
real installs), so real learner data is never touched.

Windows only (the hooks are PowerShell). Run: python tests/test_hooks.py
"""
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")   # Hebrew test names on any console

SCRIPTS = Path(__file__).resolve().parent.parent / ".claude" / "scripts"
if shutil.which("powershell.exe") is None:
    print("SKIPPED — powershell.exe not found (the hooks are Windows PowerShell)")
    sys.exit(0)


def run(script, payload, env=None):
    p = subprocess.run(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden",
                        "-File", str(SCRIPTS / script)],
                       input=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                       capture_output=True, env=env, timeout=60)
    out = p.stdout.decode("utf-8", errors="replace").strip()
    return p.returncode, (json.loads(out) if out else None)


results = []
def check(name, ok, detail=""):
    results.append(f"[{'OK  ' if ok else 'FAIL'}] {name}" + ("" if ok else f"  -> {detail}"))


# ---- detect-stuck.ps1 ----
for text, want in [("לא הבנתי את השקף על טוקנים", True), ("הקוד לא עובד, יש שגיאה", True), ("אני לא מבינה למה", True),
                   ("נתקעתי בתרגיל 2", True), ("it doesn't work", True), ("I'm stuck on the exercise", True),
                   ("continue", False), ("/learn 2.4", False), ("מה זה API?", False), ("המערכת עובדת מצוין", False)]:
    code, out = run("detect-stuck.ps1", {"hook_event_name": "UserPromptSubmit", "prompt": text})
    ctx = out["hookSpecificOutput"]["additionalContext"] if out else ""
    check(f"stuck: {text!r} -> {want}", code == 0 and (out is not None) == want and (not want or "stuck.md" in ctx), out)
code, out = run("detect-stuck.ps1", {"prompt": "לא הבנתי"})
ctx = out["hookSpecificOutput"]["additionalContext"] if out else ""
check("stuck: Hebrew round trip + factual wording (no 'read'/'follow' commands)",
      "לא הבנתי" in ctx and "read " not in ctx.lower() and "follow it" not in ctx.lower(), ctx)

# ---- check-lesson-order.ps1 ----
H = "check-lesson-order.ps1"
note = lambda out: out["hookSpecificOutput"]["additionalContext"] if out else ""
read = lambda path: {"hook_event_name": "PostToolUse", "tool_name": "Read", "tool_input": {"file_path": path}, "tool_response": {}}

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp, "טוב טק", "Tov-learn")                       # Hebrew in the path, like real installs
    lessons = root / "courses" / "demo" / "lessons"
    for mod, lesson in [("00-a", "0.1"), ("00-a", "0.2"), ("01-b", "1.1"), ("01-b", "1.2"), ("02-c", "2.1")]:
        d = lessons / mod / f"{lesson}-x"; d.mkdir(parents=True)
        (d / f"{lesson}_script.txt").write_text("Title: x", encoding="utf-8")
    # 2.1 is deliberately missing from the lesson list, to test the folder-order fallback
    (root / "courses" / "demo" / "COURSE.md").write_text(
        "| מספר | שם |\n|---|---|\n| 0.1 | a |\n| 0.2 | b |\n| 1.1 | c |\n| 1.2 | d |\n\n| Gemini | חינמי | 2.1 |\n", encoding="utf-8")
    home = Path(tmp, "home"); prog = home / "skill-tutor-tutorials" / "progress"; prog.mkdir(parents=True)
    env = dict(os.environ, USERPROFILE=str(home))
    script = lambda l: str(next(lessons.rglob(f"{l}_script.txt")))
    start = lambda l: run(H, read(script(l)), env)[1]
    legacy = "**Slides covered:** all 9\n"                                   # finished before the exercises rule
    new = "**Slides covered:** all 9\n**Exercises required:** yes\n"        # finished since the rule
    def put(name, text, enc="utf-8"): (prog / name).write_text(text, encoding=enc)
    def drop(name): (prog / name).unlink(missing_ok=True)
    ex = lambda req, n, extra="": f"# תרגילים — שיעור 0.1\n**נדרשים:** {req}{extra}\n\n" + "".join(f"## תרגיל {i} — x\n---\n" for i in range(1, n + 1))

    _, out = run(H, read(str(root / "CLAUDE.md")), env)
    check("order: non-script read -> nothing", out is None, out)
    check("order: first lesson -> nothing", start("0.1") is None)
    out = start("0.2")
    check("order: previous lesson not started -> note", "0.1 (not started)" in note(out), out)
    check("order: note says the lesson skip quiz applies only to lessons not started", "applies only to lessons marked not started" in note(out), out)
    check("order: note is factual (no imperative 'read'/'follow')", "read " not in note(out).lower().replace("script read", "")
          and "follow" not in note(out).lower(), note(out))
    check("order: same module -> no module skip quiz offered", "can pass as a whole" not in note(out), note(out))
    put("lesson-0.1.md", "**Slides covered:** 4 of 9\n")
    check("order: previous lesson's slides not finished -> note", "0.1 (learning started, slides not finished)" in note(start("0.2")))
    put("lesson-0.1.md", legacy)
    check("order: finished before the exercises rule, no exercises file -> nothing", start("0.2") is None)
    sessions = lambda cov: ("# Progress: Lesson 0.1\n\n## Sessions\n| Date | Sections Covered | Quiz Score | Notes |\n"
                            f"|------|-----------------|-----------|-------|\n| 17-06-2026 | {cov} | 8/10 | x |\n")
    for cov in ("All 15", "All sections", "All 19 sections"):
        put("lesson-0.1.md", sessions(cov))
        check(f"order: legacy quiz-format file, Sections Covered '{cov}' -> nothing", start("0.2") is None)
    put("lesson-0.1.md", sessions("1–5"))
    check("order: legacy quiz-format file, only some sections -> slides not finished", "0.1 (learning started, slides not finished)" in note(start("0.2")))
    put("lesson-0.1.md", "**Exercises required:** yes\n\n" + sessions("All 9 (diagnostic quiz)"))
    check("order: current-rules lesson, quiz row says All but slides not marked done -> slides not finished",
          "0.1 (learning started, slides not finished)" in note(start("0.2")))

    put("lesson-0.1.md", new)
    out = start("0.2")
    check("order: finished since the rule, no exercises file -> note", "0.1 (slides finished, no exercises started)" in note(out), out)
    check("order: starting 0.2 again (e.g. new session) -> note again", "no exercises started" in note(start("0.2")))
    check("order: no marker files left behind", not list(prog.glob(".*")), list(prog.glob(".*")))
    put("exercises-lesson-0.1.md", ex(3, 1))
    check("order: 1 of 3 recorded -> note with count", "1 of 3 exercises recorded" in note(start("0.2")))
    put("lesson-0.1.md", "<!-- auto-save -->\n**שיעור:** 0.1\n**שקף אחרון:** 9\n<!-- /auto-save -->\n\n" + new, "utf-8-sig")
    check("order: early save with BOM + auto-save block, 1 of 3 -> note", "1 of 3" in note(start("0.2")))
    put("exercises-lesson-0.1.md", ex(3, 2) + "## תרגיל 3 — ג (דולג — דורש תשלום)\n**סיבה:** x\n---\n")
    check("order: complete (incl. paid-skipped) -> nothing", start("0.2") is None)
    tag = " (רק התרגילים שקשורים לנושאים שנענו לא נכון במבחן הדילוג)"
    put("exercises-lesson-0.1.md", ex(1, 1, tag))
    check("order: failed skip quiz, 1 of 1 related exercise -> nothing", start("0.2") is None)
    put("exercises-lesson-0.1.md", ex(2, 1, tag))
    check("order: failed skip quiz, 1 of 2 related exercises -> note", "1 of 2" in note(start("0.2")))
    put("exercises-lesson-0.1.md", ex(0, 0, tag))
    check("order: failed skip quiz, no related exercises (0) -> nothing", start("0.2") is None)
    put("exercises-lesson-0.1.md", "## תרגיל 1 — old format, no count\n")
    check("order: old exercises file without נדרשים -> nothing (can't tell)", start("0.2") is None)
    put("exercises-lesson-0.1.md", ex(2, 1, "\n\n## תוכנית\n- 1 — a\n- 2 — b\n"))
    check("order: the planned list (## תוכנית) isn't counted as done (1 of 2)", "1 of 2" in note(start("0.2")))

    drop("exercises-lesson-0.1.md"); put("lesson-0.1.md", "**Skip quiz passed:** 8/10 (21-10-2026)\n")
    check("order: lesson skip quiz passed -> nothing", start("0.2") is None)

    # A -> C: 0.1 complete, 0.2 never started, learner opens 1.1
    out = start("1.1")
    check("order: skipping a lesson (0.1 done, 0.2 not started, start 1.1) -> note about 0.2 only",
          "0.2 (not started)" in note(out) and "0.1 (" not in note(out), out)
    check("order: module 0 has a started lesson (0.1 passed by its skip quiz) -> no module skip quiz offer",
          "as a whole" not in note(out), note(out))
    put("lesson-0.1.md", "**Exercises required:** yes\n")
    out = start("1.1")
    check("order: module 0 has a lesson in progress -> both listed, no module skip quiz offer",
          "0.1 (learning started, slides not finished)" in note(out) and "0.2 (not started)" in note(out)
          and "as a whole" not in note(out), note(out))
    drop("lesson-0.1.md")
    out = start("1.1")
    check("order: no lesson of module 0 started -> module skip quiz offered for module 0",
          "no earlier module-quiz attempt, which a module skip quiz (quiz module N) can pass as a whole: 0." in note(out), note(out))
    out = start("1.2")
    check("order: jump from nothing to 1.2 -> lists 0.1, 0.2, 1.1; module quiz offered for module 0 only",
          all(f"{l} (not started)" in note(out) for l in ("0.1", "0.2", "1.1")) and "as a whole: 0." in note(out), note(out))
    put("module-0.md", "# Module 0 — skip quiz\n**Skip quiz passed:** 9/10 (21-10-2026)\n")
    out = start("1.2")
    check("order: module 0 passed by module skip quiz -> only 1.1 listed, no module quiz offer",
          "1.1 (not started)" in note(out) and "0.1" not in note(out) and "as a whole" not in note(out), note(out))
    put("module-0.md", "# Module 0 — skip quiz\n| 21-10-2026 | 6/10 | 0.2 | not passed |\n")
    out = start("1.2")
    check("order: module quiz not passed -> module 0 lessons still listed", "0.1 (not started)" in note(out))
    check("order: module quiz not passed -> not offered again (one attempt)", "as a whole" not in note(out), note(out))
    drop("module-0.md")

    for l in ("0.1", "0.2", "1.1", "1.2"): put(f"lesson-{l}.md", new)
    for l in ("0.1", "0.2", "1.1", "1.2"): put(f"exercises-lesson-{l}.md", ex(1, 1))
    check("order: everything earlier complete -> nothing", start("1.2") is None)
    check("order: lesson missing from COURSE.md -> folder order, all earlier complete -> nothing", start("2.1") is None)
    drop("exercises-lesson-1.2.md")
    check("order: lesson missing from COURSE.md -> folder order (1.2 before 2.1)",
          "1.2 (slides finished, no exercises started)" in note(start("2.1")))

    code, out = run(H, {}, env)
    check("order: empty input -> safe exit", code == 0 and out is None, out)

# ---- check-lesson-order.ps1: optional lessons (type רשות in COURSE.md) ----
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp, "טוב טק", "Tov-learn")
    lessons = root / "courses" / "demo" / "lessons"
    for mod, l in [("00-a", "0.1"), ("00-a", "0.5"), ("01-b", "1.1"), ("01-b", "1.9"), ("02-c", "2.1")]:
        d = lessons / mod / f"{l}-x"; d.mkdir(parents=True)
        (d / f"{l}_script.txt").write_text("Title: x", encoding="utf-8")
    (root / "courses" / "demo" / "COURSE.md").write_text(
        "| מספר | שם | סוג |\n|---|---|---|\n| 0.1 | a | תיאורטי |\n| 0.5 | b | רשות |\n| 1.1 | c | מעשי |\n"
        "| 1.9 | d | רשות |\n| 2.1 | e | מעשי |\n", encoding="utf-8")
    home = Path(tmp, "home"); prog = home / "skill-tutor-tutorials" / "progress"; prog.mkdir(parents=True)
    env = dict(os.environ, USERPROFILE=str(home))
    start = lambda l: note(run(H, read(str(next(lessons.rglob(f"{l}_script.txt")))), env)[1])

    (prog / "lesson-0.1.md").write_text("**Slides covered:** all 9\n**Exercises required:** yes\n", encoding="utf-8")
    (prog / "exercises-lesson-0.1.md").write_text("**נדרשים:** 1\n\n## תרגיל 1 — x\n---\n", encoding="utf-8")
    check("optional: 0.5 not started doesn't block 1.1", start("1.1") == "", start("1.1"))
    n = start("2.1")
    check("optional: 1.1 incomplete blocks 2.1; optional 0.5 and 1.9 not listed",
          "1.1 (not started)" in n and "1.9" not in n and "0.5" not in n, n)
    (prog / "lesson-0.5.md").write_text("**Exercises required:** yes\n", encoding="utf-8")
    check("optional: 0.5 started but unfinished still doesn't block 1.1", start("1.1") == "", start("1.1"))

print("\n".join(results))
passed = sum(r.startswith("[OK") for r in results)
print(f"\n{passed}/{len(results)} passed")
sys.exit(0 if passed == len(results) else 1)
