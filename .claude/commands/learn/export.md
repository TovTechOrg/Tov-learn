# Export Module — ייצוא נתוני תלמיד

Export all learner data from `~/skill-tutor-tutorials/` to a ZIP file that can be transferred to another device or kept as a backup.

---

## Step 1 — Check source

Run silently:

```powershell
Test-Path "$HOME\skill-tutor-tutorials"
```

If the directory is **missing** → tell the learner (in `session.language`):
- No learner data found. Run `/learn setup` first.

If it **exists** → continue.

---

## Step 2 — Collect file list

Run:

```powershell
$base = "$HOME\skill-tutor-tutorials"
$files = Get-ChildItem $base -Recurse -File -ErrorAction SilentlyContinue
$groups = $files | Group-Object { $_.DirectoryName.Replace($base, '').TrimStart('\').Split('\')[0] }
foreach ($g in $groups) {
  $label = if ($g.Name -eq '') { 'שורש' } else { $g.Name }
  "$label ($($g.Count) קבצים)"
}
"סך הכל: $($files.Count) קבצים"
```

Show a brief summary of what will be exported (e.g., "settings.json, 3 tutorials, 3 progress files, knowledge map…").

---

## Step 3 — Determine destination

Get today's date and the current working directory:

```powershell
Get-Date -Format "yyyy-MM-dd"
(Get-Location).Path
```

Default path: `[CURRENT_WORKING_DIR]/tov-learn-export-[DATE].zip`

Proceed directly with the default path — no need to ask. Only ask if the user explicitly specified a different path in `$ARGUMENTS` (e.g., `/learn export C:\backups\my.zip`).

---

## Step 4 — Create ZIP

Ensure the destination directory exists, then run:

```powershell
$src  = "$HOME\skill-tutor-tutorials"
$dest = "CWD\tov-learn-export-DATE.zip"   # replace CWD and DATE with values from Step 3
$destDir = Split-Path $dest -Parent
if (-not (Test-Path $destDir)) { New-Item -ItemType Directory -Force $destDir | Out-Null }
if (Test-Path $dest) { Remove-Item $dest -Force }
Compress-Archive -Path "$src\*" -DestinationPath $dest -CompressionLevel Optimal
$size = [math]::Round((Get-Item $dest).Length / 1KB, 1)
"$dest|$size KB"
```

If the command fails → show the error and stop; don't report success.

---

## Step 5 — Confirm

Report success (respond in `session.language`):

```
✅ ייצוא הושלם!

📦 נשמר ב: [DEST_PATH]
📁 [N] קבצים | [SIZE]

כדי לייבא את הגיבוי במכשיר אחר:
/learn import
```

