# Import Module — ייבוא נתוני תלמיד

Import learner data from a ZIP file (created by `/learn export`) into `~/skill-tutor-tutorials/`.

---

## Step 1 — Get import path

If `$ARGUMENTS` contains a file path (ends with `.zip`), use it directly.

Otherwise, default to `[CWD]/tov-learn-export-[TODAY].zip` — the same default the export module uses:

```powershell
$date = Get-Date -Format "yyyy-MM-dd"
$default = "$(Get-Location)\tov-learn-export-$date.zip"
Test-Path $default
```

If the default file **exists** → use it silently (no need to ask).
If the default file **does not exist** → ask the learner: "לא נמצא קובץ ייצוא בתיקייה הנוכחית. מה הנתיב לקובץ ה-ZIP?"

---

## Step 2 — Validate file

Run:

```powershell
Test-Path "IMPORT_PATH"
```

If **missing** → tell the learner the file was not found and stop.

Peek inside the ZIP to verify it's a valid tov-learn export:

```powershell
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [System.IO.Compression.ZipFile]::OpenRead("IMPORT_PATH")
$entries = $zip.Entries | Select-Object -ExpandProperty FullName
$zip.Dispose()
$hasSettings = ($entries | Where-Object { $_ -eq 'settings.json' }).Count -gt 0
"hasSettings=$hasSettings|count=$($entries.Count)"
```

If `settings.json` is not found → warn the learner that this might not be a valid tov-learn export and ask (AskUserQuestion, single-select):
- **המשך בכל זאת** — proceed with import
- **ביטול** — cancel

---

## Step 3 — Preview contents

Show the learner what the ZIP contains:

```powershell
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [System.IO.Compression.ZipFile]::OpenRead("IMPORT_PATH")
$entries = $zip.Entries | Select-Object -ExpandProperty FullName
$zip.Dispose()
$groups = $entries | Where-Object { $_ -ne '' } |
  Group-Object { ($_ -split '/')[0] }
foreach ($g in $groups) { "$($g.Name): $($g.Count) קבצים" }
"סך הכל: $($entries.Count) פריטים"
```

Also check how much existing data is already on this device:

```powershell
$ex = Get-ChildItem "$HOME\skill-tutor-tutorials" -Recurse -File -ErrorAction SilentlyContinue
$ex.Count
```

---

## Step 4 — Choose import mode

Ask (AskUserQuestion, single-select), responding in `session.language`:

**Question:** "כיצד לייבא?"

**Options:**
1. **החלף הכל** — מחק את כל הנתונים הקיימים והחלף בתוכן הקובץ (מומלץ למעבר למכשיר חדש)
2. **מזג** — ייבא קבצים חדשים ודרוס קבצים קיימים שהשתנו, אבל שמור קבצים שנמצאים רק במכשיר (Recommended)
3. **הוסף בלבד** — ייבא רק קבצים שאינם קיימים עדיין, אל תדרוס שום דבר
4. **ביטול** — אל תשנה כלום

If learner chooses **ביטול** → stop and confirm nothing changed.

---

## Step 5A — Replace all

```powershell
$dest = "$HOME\skill-tutor-tutorials"
if (Test-Path $dest) { Get-ChildItem $dest | Remove-Item -Recurse -Force }
Expand-Archive -Path "IMPORT_PATH" -DestinationPath $dest -Force
$count = (Get-ChildItem $dest -Recurse -File).Count
"imported=$count"
```

---

## Step 5B — Merge (add new + overwrite changed, keep device-only files)

Extract to a temp folder, then copy all files from the ZIP — overwriting existing ones, but leaving files that exist only on the device untouched:

```powershell
$temp = "$env:TEMP\tov-import-temp"
if (Test-Path $temp) { Remove-Item $temp -Recurse -Force }
Expand-Archive -Path "IMPORT_PATH" -DestinationPath $temp -Force
$dest = "$HOME\skill-tutor-tutorials"
$added = 0; $updated = 0
Get-ChildItem $temp -Recurse -File | ForEach-Object {
  $rel    = $_.FullName.Substring($temp.Length).TrimStart('\/')
  $target = Join-Path $dest $rel
  $isNew  = -not (Test-Path $target)
  $dir    = Split-Path $target -Parent
  if (-not (Test-Path $dir)) { New-Item -ItemType Directory $dir -Force | Out-Null }
  Copy-Item $_.FullName $target -Force
  if ($isNew) { $added++ } else { $updated++ }
}
Remove-Item $temp -Recurse -Force
"added=$added|updated=$updated"
```

---

## Step 5C — Add only (no overwrite)

Extract to a temp folder, then copy only files that do not yet exist on this device:

```powershell
$temp = "$env:TEMP\tov-import-temp"
if (Test-Path $temp) { Remove-Item $temp -Recurse -Force }
Expand-Archive -Path "IMPORT_PATH" -DestinationPath $temp -Force
$dest = "$HOME\skill-tutor-tutorials"
$imported = 0; $skipped = 0
Get-ChildItem $temp -Recurse -File | ForEach-Object {
  $rel    = $_.FullName.Substring($temp.Length).TrimStart('\/')
  $target = Join-Path $dest $rel
  if (-not (Test-Path $target)) {
    $dir = Split-Path $target -Parent
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory $dir -Force | Out-Null }
    Copy-Item $_.FullName $target
    $imported++
  } else { $skipped++ }
}
Remove-Item $temp -Recurse -Force
"imported=$imported|skipped=$skipped"
```

---

## Step 6 — Confirm

Report success (respond in `session.language`):

**Replace all:**
```
✅ ייבוא הושלם!

📁 [N] קבצים יובאו
📍 ~/skill-tutor-tutorials/

הקלד /learn כדי להמשיך ללמוד.
```

**Merge:**
```
✅ ייבוא הושלם!

📥 נוספו: [N] קבצים חדשים
🔄 עודכנו: [N] קבצים קיימים

הקלד /learn כדי להמשיך ללמוד.
```

**Add only:**
```
✅ ייבוא הושלם!

📥 יובאו: [N] קבצים חדשים
⏭ נדלגו: [N] קבצים (כבר קיימים)

הקלד /learn כדי להמשיך ללמוד.
```

