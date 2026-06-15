# שאלות נפוצות — Tov-learn

> **שאלות על פריסה (deploy)?** ראו את ה-FAQ הייעודי: [`courses/ai-dev/deploy-faq.md`](courses/ai-dev/deploy-faq.md) — GitHub Pages, Cloudflare Workers, Render ועוד.

---

## AntiGravity — עבודה עם פרויקטים

### איך פותחים פרויקט חדש ב-AntiGravity?

כדי לפתוח חלון עבודה חדש על תיקייה אחרת:

1. לחצו **File** בתפריט העליון
2. לחצו **New Window**
3. בחלון החדש — לחצו **Open Folder** (או גררו תיקייה)
4. תנו שם לתיקייה ואשרו

כך ניתן לעבוד על שני פרויקטים במקביל — שיחת הלמידה בחלון אחד ופרויקט אמיתי בחלון שני.

> **שימו לב:** הפקודות `cd ~/folder && claude` מיועדות לטרמינל רגיל (Terminal של Mac), **לא** ל-AntiGravity.

---

## קול ו-TTS

### איך מוסיפים קול בעברית למערכת?

מערכת ה-TTS של Tov-learn משתמשת בקולות Windows SAPI. ברירת המחדל היא לחפש קול עברי אוטומטית — אם אין קול עברי מותקן, הדיקלום לא יעבוד.

**שלב 1 — התקנת חבילת שפה עברית:**

1. פתחו **הגדרות** ← **זמן ושפה** ← **שפה ואזור**
2. לחצו **הוסף שפה** וחפשו **עברית**
3. לאחר ההתקנה, לחצו על **עברית** ← **אפשרויות שפה**
4. מצאו את **המרת טקסט לדיבור** ולחצו **הורד**

**שלב 2 — חיבור הקול ל-SAPI (נדרש פעם אחת):**

Windows מתקין קולות חדשים תחת "OneCore" שאינו נגיש ישירות ל-SAPI. יש להריץ את הפקודה הבאה ב-PowerShell **כמנהל** (Admin):

```powershell
$src = "HKLM:\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens\MSTTS_V110_heIL_Asaf"
$dst = "HKLM:\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_heIL_Asaf"
function Copy-RegKey($srcPath, $dstPath) {
    $srcKey = Get-Item $srcPath
    New-Item -Path $dstPath -Force | Out-Null
    foreach ($val in $srcKey.GetValueNames()) {
        $data = $srcKey.GetValue($val, $null, "DoNotExpandEnvironmentNames")
        $kind = $srcKey.GetValueKind($val)
        Set-ItemProperty -Path $dstPath -Name $val -Value $data -Type $kind
    }
    foreach ($sub in $srcKey.GetSubKeyNames()) {
        Copy-RegKey "$srcPath\$sub" "$dstPath\$sub"
    }
}
Copy-RegKey $src $dst
Write-Host "הקול אסף חובר בהצלחה"
```

**שלב 3 — בדיקה:**

```powershell
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$s.GetInstalledVoices() | ForEach-Object { $_.VoiceInfo.Name + " | " + $_.VoiceInfo.Culture.Name }
```

אם מופיע `Microsoft Asaf | he-IL` — הכל מוכן.

---

### אילו קולות נתמכים?

| קול | שפה | סטטוס |
|-----|-----|--------|
| Microsoft Asaf | עברית (ישראל) | מומלץ |
| Microsoft David | אנגלית (ארה"ב) | ברירת מחדל אם אין עברית |

המערכת תמיד מנסה לבחור קול עברי ראשון. אם לא נמצא — תדובר השפה הזמינה (ייתכן שלא יקרא עברית נכון).

---

### ה-TTS מדלג על הטקסט העברי ומדבר רק מילים באנגלית — מה קורה?

זה קורה כשאין קול עברי מותקן. הקול האנגלי קורא רק את האותיות הלטיניות ומדלג על כל האות העברי.

**פתרון:** התקינו קול עברי לפי השלבים למעלה.

---
