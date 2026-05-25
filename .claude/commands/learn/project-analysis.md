# Project Analysis Module

*Loaded when the learner chooses "project analysis".*

Respond in `session.language` throughout.

---

## Phase A — Automated Code Scan (silently, before questions)

Use Glob to scan the project root for:
- `package.json`, `requirements.txt`, `Pipfile`, `pyproject.toml`, `go.mod`, `*.csproj`, `Cargo.toml`
- `docker-compose.yml`, `Dockerfile`, `.env.example`
- `CLAUDE.md` — if present, read it
- Top-level folder structure: `src/`, `app/`, `lib/`, `api/`, `services/`

From the scan: identify tech stack, languages, frameworks, external services (imports, env vars, config files).

---

## Phase B — Architect Interview (5 questions, one at a time)

1. **"What does the project do — in one sentence, at a business level?"** (not technical — what problem does it solve for the user?)
2. **"Who are the users and what do they need to do in it?"** (2–3 main use cases)
3. **"What external services does the project connect to?"** (anything not found in the scan)
4. **"What is the current and expected scale?"** (users, requests, seasonal load)
5. **"What are the biggest pain points or uncertainties in the architecture?"** (bottlenecks, tech debt, things that worry you)

---

## Phase C — Generate Architecture Map HTML

Save to: `~/skill-tutor-tutorials/architectures/[project-name].html`

```html
<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
  <meta charset="UTF-8">
  <title>Architecture: [project name]</title>
  <style>
    /* Layer colors:
       Client = #3B82F6 | API/Backend = #10B981 | Services = #8B5CF6
       Data = #F59E0B | External = #6B7280
    */
    body { font-family: 'Segoe UI', sans-serif; background: #F9FAFB; padding: 40px; direction: rtl; }
    h1 { font-size: 1.8rem; color: #111827; margin-bottom: 4px; }
    .subtitle { color: #6B7280; margin-bottom: 40px; font-size: 1rem; }
    .arch-diagram { display: flex; flex-direction: column; gap: 16px; max-width: 900px; margin: 0 auto; }
    .layer { border-radius: 12px; padding: 20px; }
    .layer-title { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; opacity: 0.7; }
    .components { display: flex; gap: 12px; flex-wrap: wrap; }
    .component { background: white; border-radius: 8px; padding: 14px 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); min-width: 140px; }
    .component-name { font-weight: 600; font-size: 0.95rem; }
    .component-tech { font-size: 0.75rem; color: #6B7280; margin-top: 2px; }
    .component-desc { font-size: 0.8rem; color: #374151; margin-top: 6px; }
    .arrow { text-align: center; font-size: 1.5rem; color: #9CA3AF; margin: 4px 0; }
    .arrow-label { font-size: 0.75rem; color: #9CA3AF; }
    .bottom-section { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-top: 32px; max-width: 900px; margin-right: auto; }
    .info-box { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
    .info-box h3 { font-size: 0.9rem; font-weight: 700; color: #374151; margin-bottom: 12px; }
    .info-box ul { list-style: none; padding: 0; margin: 0; }
    .info-box li { font-size: 0.85rem; color: #6B7280; padding: 4px 0; border-bottom: 1px solid #F3F4F6; }
    .concern { color: #EF4444 !important; }
  </style>
</head>
<body>
  <h1>[Project Name]</h1>
  <p class="subtitle">[Short business description]</p>
  <div class="arch-diagram">
    <div class="layer" style="background: #EFF6FF; border: 1px solid #BFDBFE;">
      <div class="layer-title" style="color: #3B82F6;">Client Layer</div>
      <div class="components">
        <div class="component">
          <div class="component-name">[component name]</div>
          <div class="component-tech">[technology]</div>
          <div class="component-desc">[short description]</div>
        </div>
      </div>
    </div>
    <div class="arrow">↓ <span class="arrow-label">[connection type]</span></div>
    <!-- Continue layers based on project -->
  </div>
  <div class="bottom-section">
    <div class="info-box">
      <h3>Tech Stack</h3>
      <ul><!-- technology + usage --></ul>
    </div>
    <div class="info-box">
      <h3>Points of Concern</h3>
      <ul>
        <li class="concern">[concern 1]</li>
      </ul>
    </div>
  </div>
</body>
</html>
```

**Guidelines:** Build layers based on scan + interview findings only. Use real names from the project. Label arrows with connection type (REST, WebSocket, Queue, etc.). External services go in a separate bottom layer.

After saving, tell the learner the file path and ask them to open it in a browser.

---

## Phase D — Update Learner Profile

Update `~/skill-tutor-tutorials/learner_profile.md`:

```markdown
## Current Project
[Project name] — [short business description]

## Architecture Notes
- Stack: [main technologies]
- Scale: [current and expected]
- Pain points: [from the interview]
```

After completing, ask if the learner wants to study a lesson that addresses one of the challenges they mentioned.
