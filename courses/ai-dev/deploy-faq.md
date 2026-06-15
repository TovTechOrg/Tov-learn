# Deploy FAQ — שאלות נפוצות על פריסה

*נקרא על ידי מודול `deploy`. תלמידים מוסיפים שאלות חדשות דרך PR (ראה תחתית הקובץ).*

כל ערך: שאלה, תשובה קצרה, ופקודה אם רלוונטי.

---

## כללי

### האם אפשר להחביא מפתח API באתר סטטי?
**לא.** כל מה שרץ בדפדפן גלוי למשתמש — כולל מפתחות. אם הפרויקט קורא ל-LLM או לכל API עם מפתח, צריך שכבת שרת קטנה (Cloudflare Worker) שמחזיקה את המפתח ומעבירה את הבקשה. האתר הסטטי קורא ל-Worker, ה-Worker קורא ל-API.

### מתי GitHub Pages ומתי משהו אחר?
GitHub Pages = אתר סטטי בלבד (HTML/CSS/JS, build של React/Vite), בלי שרת ובלי סודות. ברגע שצריך מפתח, DB, או לוגיקת שרת — עוברים ל-Cloudflare Workers. שרת ארוך-טווח (websockets, Postgres, job ברקע) — Render.

---

## GitHub Pages

### האתר עלה אבל הקבצים (CSS/JS) לא נטענים — מסך לבן
ב-build של Vite/React הנתיבים מוחלטים (`/assets/...`) אבל Pages מגיש מתת-נתיב (`/repo-name/`). הוסיפו `base: '/repo-name/'` ל-`vite.config.js` ובנו מחדש.

### איך מפרסמים build של Vite ל-Pages דרך CLI?
```bash
npm run build
npx gh-pages -d dist      # או GitHub Action שמפרסם את dist אוטומטית
```

---

## Cloudflare Workers / Wrangler

### איך שומרים מפתח API ב-Worker בלי לחשוף אותו?
```bash
wrangler secret put ANTHROPIC_API_KEY   # נשמר מוצפן בצד Cloudflare, לא ב-repo
```
בקוד ניגשים אליו דרך `env.ANTHROPIC_API_KEY`. אף פעם לא בתוך הקוד או ב-git.

### חייבים כרטיס אשראי כדי לפתוח חשבון Cloudflare?
לא ל-Workers/Pages ברמת ה-free. פותחים חשבון רק כשבאמת מגיעים לשלב פריסה.

### שגיאת CORS כשהאתר הסטטי קורא ל-Worker
הוסיפו ל-Worker את כותרות ה-CORS (`Access-Control-Allow-Origin`) וטפלו בבקשת `OPTIONS` (preflight).

---

## Render

### השירות "נרדם" ולוקח 30 שניות לענות בבקשה הראשונה
ה-free tier של Render משבית שירות אחרי 15 דקות חוסר פעילות והבקשה הבאה מעירה אותו (cold start). תקין ללמידה — לא לפרודקשן אמיתי.

---

## תרומה ל-FAQ

נתקלתם בבעיה שלא מופיעה כאן ופתרתם? הוסיפו ערך — זה תרגול אמיתי של git + PR:

```bash
git checkout -b faq/short-topic
# הוסיפו את השאלה והתשובה לסעיף המתאים
git add courses/ai-dev/deploy-faq.md
git commit -m "faq: <נושא קצר>"
gh pr create --fill
```

מודול ה-deploy יציע לכם לעשות את זה אוטומטית כשאתם פותרים בעיה חדשה.
