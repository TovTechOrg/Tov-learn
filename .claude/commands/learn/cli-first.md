# CLI-First Reference

*Shared principle. Any module may reference this as "follow cli-first".*

When guiding a learner through any setup, deploy, or repo operation — **prefer the command line over clicking dashboards.** The goal is for the learner to understand what is happening, build a reusable muscle, and end up with a reproducible workflow.

## Rules

1. **Show the command, then explain it.** Never give a command without one line on what it does and why.
2. **Prefer official CLIs** over web UIs:
   - GitHub → `gh` (`gh repo create`, `gh pr create`, `gh auth login`)
   - Cloudflare → `wrangler` (`wrangler deploy`, `wrangler pages deploy`, `wrangler login`)
   - Render → `render` CLI or a `render.yaml` blueprint committed to the repo
   - Vercel → `vercel`, Netlify → `netlify`
   - Git → plain `git` (`git init`, `git add`, `git commit`, `git push`)
3. **Use the UI only when the CLI genuinely can't do it** — e.g. first-time OAuth login, adding a payment method, or a one-time account verification. Say explicitly "this step is UI-only because…".
4. **Reproducibility:** prefer commands and committed config files (`wrangler.toml`, `render.yaml`, `.github/workflows/`) over manual dashboard settings, so the setup survives a fresh clone.
5. **Windows note:** the learner is likely on PowerShell. Give PowerShell-safe commands (`$env:VAR`, not `export`). Most of these CLIs are cross-platform via `npm i -g` or `winget`.
6. **Secrets never go in the repo or the command history in plain text.** Use the platform's secret store (`wrangler secret put`, `gh secret set`, Render env vars) — and explain why.

## Mini cheat sheet to surface when relevant

```bash
# GitHub
gh auth login                 # one-time login (opens browser — UI-only step)
gh repo create my-app --public --source=. --push

# Cloudflare Workers / Pages
npm i -g wrangler
wrangler login                # one-time login (browser)
wrangler deploy               # deploy a Worker
wrangler pages deploy ./dist  # deploy a static build to Pages
wrangler secret put API_KEY   # store a secret safely

# Git basics
git init && git add . && git commit -m "init" && git push
```
