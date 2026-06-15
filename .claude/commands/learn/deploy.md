# Deploy Module — איזה כלי פריסה לבחור

*Loaded when /learn is called with "deploy" argument, or when a learner asks how/where to deploy a project.*

Respond in `session.language` throughout (default Hebrew). Address the learner using `session.address`. Follow **cli-first** — read `.claude/commands/learn/cli-first.md` and prefer commands over dashboards, always showing the command + a one-line "why".

The job of this module is **not** to deploy for them silently — it is to help them *choose the right tool, understand why, and run the commands themselves* so they learn by doing.

---

## Core Principles (state these once, briefly, at the start)

1. בונים פרויקטים אמיתיים — לומדים תוך כדי deploy.
2. מעדיפים כלים חינמיים, ומכירים את המגבלות של ה-free tier.
3. מעדיפים CLI על פני לחיצות בדאשבורד (follow cli-first).
4. פותחים חשבון חדש **רק כשבאמת צריך** — לא מראש.
5. תמיד מסבירים *למה* בחרנו בכלי.

---

## Step 1 — Read the FAQ first

Read `courses/ai-dev/deploy-faq.md`. If the learner's question already has an answer there, lead with it (and mention it came from the shared FAQ). This rewards the contribution loop.

---

## Step 2 — Diagnose (3 questions, ask together)

Do **not** guess the platform from project type alone. Ask:

1. הפרויקט הוא רק frontend (HTML/CSS/JS, או build של React/Vite) בלי שרת?
2. הוא קורא ל-LLM / API עם מפתח סודי, או צריך בסיס נתונים?
3. הוא צריך שרת שרץ כל הזמן — websockets, תהליך ברקע, job מתוזמן, או Postgres?

The most important branch for this course: **question 2.** A static site cannot hide an API key — anything in the browser is visible. So an AI project that *looks* static (a React chat UI calling Claude) actually needs a tiny server to hold the key. Make this explicit when it applies.

---

## Step 3 — Decision tree

| מצב | המלצה | למה |
|-----|--------|-----|
| סטטי בלבד, בלי סודות ובלי שרת | **GitHub Pages** | חינם, אפס תחזוקה, deploy ישירות מה-repo. ברירת המחדל תמיד. |
| סטטי + מפתח API / LLM / DB קל | **Cloudflare Workers + Wrangler** | Worker קטן מחזיק את המפתח (`wrangler secret put`) ומעביר את הבקשה. KV/D1 לנתונים. free tier נדיב. |
| צריך build/preview deploys, טפסים, או DX של אתר סטטי "פלוס" | **Cloudflare Pages** (או Netlify) | עדיין חינם, build אוטומטי, preview לכל PR. |
| שרת תמידי — websockets, Postgres, job ברקע | **Render** | תומך בשרת ארוך-טווח. **אזהרה:** free tier נרדם אחרי 15 דק' (cold start ~30 שניות). |
| Next.js עם SSR, רוצים zero-config | **Vercel / Netlify** | הכי קל ל-Next. **אבל:** vendor lock-in ו-hobby tier מוגבל לשימוש לא-מסחרי. |

**כלל הברירת מחדל:** אם זה סטטי — תמיד GitHub Pages, אלא אם סיבה ספציפית שוללת אותו.

When recommending, give:
- שם הכלי + משפט "למה",
- מגבלת ה-free tier הרלוונטית,
- הפקודות הראשונות (follow cli-first), בלי לפתוח חשבון עד שבאמת צריך.

---

## Step 4 — Account creation (only when needed)

פותחים חשבון רק כשמגיעים לשלב שדורש אותו, לפי הסדר:

1. **GitHub** — תמיד (כבר יש להם מהקורס).
2. **Cloudflare** — רק אם בוחרים Workers/Pages. אין צורך בכרטיס אשראי ל-free tier.
3. **Render** — רק אם צריך שרת תמידי.
4. **Vercel / Netlify** — רק אם באמת נדרש (Next SSR).

לכל חשבון: ציין שזה צעד UI-only חד-פעמי (OAuth login), והמשך משם ב-CLI.

---

## Step 5 — Cost & free-tier awareness

לפני שמסיימים, ודא שהלומד יודע את המגבלה של מה שבחר (זה מתחבר ל-checklist של פרויקט הגמר — חישוב עלות):

- **GitHub Pages:** repo ציבורי, ~1GB, 100GB תעבורה/חודש.
- **Cloudflare Workers:** ~100K בקשות/יום ב-free.
- **Render free:** נרדם אחרי 15 דק' חוסר פעילות.
- **Vercel/Netlify hobby:** לא-מסחרי, מגבלות build/bandwidth.

אם הפרויקט קורא ל-LLM — הזכר את עלות ה-API עצמו (זה נפרד מעלות ה-hosting).

---

## Step 6 — Contribute to the FAQ (PR via gh)

If the learner hit a snag **not** already in `deploy-faq.md` and solved it, offer:

> "פתרת בעיה חדשה — רוצה להוסיף אותה ל-FAQ המשותף? זה תרגול אמיתי של git + PR, ותעזור לתלמידים הבאים."

If yes, follow **cli-first** and walk them through it (let them run the commands — explain each):

```bash
git checkout -b faq/<short-topic>
# הוסף את השאלה + התשובה לסעיף המתאים ב-courses/ai-dev/deploy-faq.md
git add courses/ai-dev/deploy-faq.md
git commit -m "faq: <short topic>"
gh pr create --fill
```

Draft the FAQ entry text for them (question + concise answer + command if relevant), but let *them* run the git/PR commands so they practice the workflow. If `gh` isn't authenticated, that's the one UI-only step (`gh auth login`).

---

## Step 7 — Security scan on the live app

כשיש URL חי — זה הרגע לסקירת אבטחה אמיתית. לא לפני: בדיקת headers, חשיפת קבצים, ו-auth endpoints דורשות אפליקציה שרצה.

אמור ללומד:

> "האפליקציה חיה — זה הזמן הנכון לבדוק אבטחה. סקירה על URL חי מוצאת דברים שבדיקת קוד בלבד מפספסת: קבצים שנחשפים בפועל, כותרות שחסרות, endpoints שמגיבים בצורה שלא ציפית.
>
> הרץ: `/learn security [הכנס כאן את ה-URL שקיבלת]`"

אם הלומד לא רוצה עכשיו — קבל בשקט. אל תחזור על זה שוב.
