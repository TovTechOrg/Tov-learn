# Security Module — סקירת אבטחה

*Loaded when /learn is called with "security [URL]" or "security" argument, or when the deploy module offers a security check and the learner accepts.*

Respond in `session.language` throughout. Address the learner using `session.address`.

The goal of this module is **not** to be a static checklist — it is to help the learner *find real vulnerabilities in their running app, understand why each one is dangerous, and fix it themselves* so they learn by doing.

A live URL reveals what code review misses: files that are actually served, headers the server sends, endpoints that respond unexpectedly. Always prefer testing the live app when a URL is available.

---

## Pre-flight — Get the URL

Parse `$ARGUMENTS` for a URL (starts with `http://` or `https://`).

- **URL provided** → store as `target_url`, proceed to Phase A (Live Scan).
- **No URL** → ask: "מה ה-URL של האפליקציה? (למשל: `https://my-app.onrender.com`). אם עוד לא העלית — הרץ `/learn deploy` קודם, ותחזור לכאן עם הכתובת."

---

## Phase A — Live HTTP Scan (silently, before speaking)

Run these Bash checks against `target_url` silently. Record every result.

**1. TLS & redirect**
```bash
# HTTP → HTTPS redirect?
curl -s -o /dev/null -w "%{http_code} %{redirect_url}" http://TARGET_HOST/
# TLS version
curl -s -v --tlsv1.2 https://TARGET_URL/ 2>&1 | grep -E "SSL|TLS|issuer"
```

**2. קבצים רגישים — האם נחשפים?**
```bash
for path in /server.js /app.js /index.js /package.json /.env /config.js /upload.js; do
  code=$(curl -s -o /dev/null -w "%{http_code}" https://TARGET_URL$path)
  echo "$code $path"
done
```
200 = חשיפה קריטית. 404/403 = תקין.

**3. Security headers**
```bash
curl -s -I https://TARGET_URL/ | grep -iE "strict-transport|content-security|x-frame|x-content-type|referrer-policy|x-powered-by"
```
רשום אילו כותרות חסרות ואיזה מידע `x-powered-by` חושף.

**4. Endpoint auth — נסה בלי אימות**
```bash
# החלף /api/upload-doc בנתיב האמיתי שהלומד יספק ב-Phase B
curl -s -o /dev/null -w "%{http_code}" -X POST https://TARGET_URL/api/upload-doc \
  -H "Content-Type: application/json" -d '{"test":1}'
```
200/201 = endpoint פתוח. 401/403 = מוגן.

**5. /config ו-endpoints חשופים**
```bash
curl -s https://TARGET_URL/config
```
בדוק אם מחזיר מזהים פנימיים, doc IDs, או שמות משתני סביבה.

שמור את כל התוצאות בזיכרון הפגישה — תשתמש בהם ב-Phase C.

### Phase A.2 — Code Scan (bonus, אם יש גישה לקוד)

אם הפרויקט פתוח בסביבה המקומית, הרץ גם את בדיקות הקוד:

| Pattern | What to flag |
|---------|-------------|
| `express.static(__dirname)` | חשיפת קוד מקור |
| `innerHTML` | HTML injection |
| `req.body\.\w+` עובר לשירות חיצוני | Confused deputy |
| `error\.message` ב-`res.send` | דליפת מידע |
| `helmet` — קיים ב-package.json? | כותרות חסרות |
| `express-rate-limit` — קיים? | חסר rate limiting |
| `.env` ב-`.gitignore`? | סוד שעלול לדלוף |

---

## Phase B — 2 שאלות ממוקדות (שאל יחד בהודעה אחת)

הצג את התוצאות הגולמיות של Phase A בקצרה, ואז שאל:

> "רצתי כמה בדיקות על האפליקציה החיה. יש לי עוד שתי שאלות לפני שאסכם."

השאלות:

1. **איזה endpoints חשופים לאינטרנט מעבר ל-`/`?** (למשל: POST /api/save, POST /api/upload-doc, GET /config) — רשום אותם. אם לא בטוח — כתוב "לא יודע" ונמצא ביחד.
2. **האם יש קלט של משתמש שמוצג חזרה לדף?** (הערות, שמות, חיפוש, כל דבר שהמשתמש כותב ורואה על המסך — כן/לא)

---

## Phase C — Checklist ממוקד לפי סוג הפרויקט

בנה את הסקירה מתוך **שני מקורות**: ממצאי Phase A + תשובות Phase B.

לא לחזור על כל הרשימה — רק על מה שרלוונטי לפרויקט הזה.

### קטגוריה 1 — חשיפת קבצים

**בדוק:** האם `express.static` מגיש את תיקיית השורש (`__dirname`) במקום תיקיית `public/`?

אם כן — זה קריטי. הסבר:

> "כשכותבים `express.static(__dirname)`, השרת מגיש **את כל הקבצים בתיקייה** — כולל `server.js`, `package.json`, ואם יש קובץ סוד שלא נכלל ב-.gitignore — גם אותו. כל אחד באינטרנט יכול להוריד את הקוד שלך."

תיקון:
```js
// ❌ חושף הכל
app.use(express.static(__dirname))

// ✅ מגיש רק את public/
app.use(express.static(path.join(__dirname, 'public')))
```

---

### קטגוריה 2 — אימות Endpoints

**בדוק:** האם יש אנדפוינטים שמקבלים POST/PUT/DELETE בלי לבדוק זהות?

אם כן — חומרה גבוהה. הסבר:

> "אנדפוינט ללא אימות הוא כמו דלת שפתוחה לכולם. כל אחד שיודע את הכתובת יכול לשלוח בקשה — מהדפדפן שלו, מ-curl, מסקריפט אוטומטי."

דפוס מינימלי לבדיקת סוד משותף:
```js
const secret = process.env.SYNC_SECRET
if (!secret) return res.status(503).json({ error: 'Service unavailable' })

const provided = req.headers['x-sync-key']
if (!provided || !timingSafeEqual(Buffer.from(provided), Buffer.from(secret))) {
  return res.status(401).json({ error: 'Unauthorized' })
}
```

הסבר `timingSafeEqual`: השוואה רגילה (`===`) פגיעה ל-timing attack — אפשר לנחש מפתח תו-תו לפי זמן התשובה. `timingSafeEqual` לוקח אותו זמן תמיד.

---

### קטגוריה 3 — Confused Deputy

**בדוק:** האם ערכים מ-`req.body` (כמו `docId`, `userId`, `path`) עוברים ישירות לשירות חיצוני?

אם כן — חומרה גבוהה. הסבר:

> "זה נקרא 'confused deputy' — השרת שלך פועל כסוכן מורשה (deputy) של שירות חיצוני, אבל הוא מאפשר לתוקף להגיד לו *למי* לפעול. המשתמש שולח `docId: 'מסמך-של-מישהו-אחר'` — והשרת מבצע פעולה על המסמך הזה."

תיקון:
```js
// ❌ המשתמש שולט על היעד
const docId = req.body.docId || process.env.DOC_ID

// ✅ השרת תמיד קובע את היעד
const docId = process.env.DOC_ID
```

---

### קטגוריה 4 — HTML Injection

**בדוק:** האם יש `innerHTML` עם ערכים שהגיעו מקלט משתמש?

אם כן — חומרה בינונית (גבוהה אם המידע נשמר ומוצג למשתמשים אחרים). הסבר:

> "כשמכניסים ישירות מחרוזת מהמשתמש ל-innerHTML, התוקף יכול לכתוב `<img src=x onerror='alert(document.cookie)'>` — וזה ירוץ בדפדפן של כל מי שרואה את הדף."

תיקון — פונקציית escape פשוטה:
```js
function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

// שימוש:
element.innerHTML = escapeHtml(userInput)
// או עדיף:
element.textContent = userInput  // לא צריך escape כלל
```

---

### קטגוריה 5 — כותרות אבטחה

**בדוק:** האם `helmet` קיים ב-`package.json`?

אם לא — חומרה בינונית. הסבר:

> "כותרות HTTP כמו `X-Frame-Options`, `Content-Security-Policy`, ו-`Strict-Transport-Security` מגנות מפני סוגי התקפה שלמות — clickjacking, MIME sniffing, הורדה ל-HTTP. `helmet` מוסיף את כולן בשורה אחת."

```bash
npm install helmet
```
```js
const helmet = require('helmet')
app.use(helmet())
```

---

### קטגוריה 6 — Rate Limiting

**בדוק:** האם `express-rate-limit` מוגדר?

אם לא — חומרה בינונית. הסבר:

> "בלי rate limiting, תוקף יכול לשלוח אלפי בקשות לאנדפוינטים שלך — להציף את מכסת ה-API, לנסות סיסמאות, או פשוט להשבית את השרת."

```bash
npm install express-rate-limit
```
```js
const rateLimit = require('express-rate-limit')
app.use('/api/', rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 דקות
  max: 30,                     // 30 בקשות לחלון
  message: { error: 'Too many requests' }
}))
```

---

### קטגוריה 7 — דליפת מידע בשגיאות

**בדוק:** האם יש `res.send(error.message)` או `res.json({ error: err.stack })`?

אם כן — חומרה בינונית. הסבר:

> "הודעות שגיאה מפורטות חושפות לתוקף את מבנה הקוד, שמות קבצים, גרסאות תלויות — מידע שעוזר לו לתכנן התקפה מדויקת."

```js
// ❌
res.status(500).send(error.message)

// ✅
console.error('Internal error:', error)  // מלא ב-logs
res.status(500).json({ error: 'Internal server error' })  // גנרי לחוץ
```

---

### קטגוריה 8 — ניהול סודות

**בדוק:** האם `.env` מוזכר ב-`.gitignore`? האם יש מפתחות hardcoded בקוד?

אם `.env` לא ב-`.gitignore` — קריטי מיד. הסבר:

> "אם `.env` יעלה ל-git — כל מי שיש לו גישה ל-repo (כולל GitHub בחשבון ציבורי) יוכל לראות את כל המפתחות שלך לנצח, גם אחרי מחיקה — כי git שומר היסטוריה."

```
# .gitignore
.env
.env.local
*.pem
service-account*.json
```

---

## Phase D — דוח סיכום

אחרי שסיימת את ה-checklist, הצג דוח מסודר:

```
🔒 סקירת אבטחה — [שם הפרויקט]
═══════════════════════════════

🔴 קריטי (תקן לפני כל העלאה):
  • [ממצא + שורת קוד רלוונטית]

🟠 גבוה (תקן בהקדם):
  • [ממצא]

🟡 בינוני (מומלץ לפני פרסום):
  • [ממצא]

✅ תקין:
  • [מה שנמצא תקין]
```

בסוף הדוח, שאל:
> "על איזה ממצא תרצה להתחיל? אני יכול לעבור איתך על התיקון צעד-צעד."

---

## Phase E — שמירת ממצאים

שמור ב-`~/skill-tutor-tutorials/progress/security-[project-name].md`:

```markdown
# Security Review — [project name]
date: [תאריך]

## ממצאים
[רשימת ממצאים עם חומרה]

## תוקן
[מה תוקן בפגישה זו]

## נותר
[מה עוד פתוח]
```

אחרי השמירה: "שמרתי את הממצאים. בפעם הבאה שתרוץ `/learn security` אציג לך את מה שנותר."

---

## כלל עזיבה

אם הלומד רוצה לחזור לפריסה אחרי הסקירה — אמור:

> "סיימנו את הסקירה. כשתהיה מוכן — חזור ל`/learn deploy` ונמשיך מהשלב שעצרנו."
