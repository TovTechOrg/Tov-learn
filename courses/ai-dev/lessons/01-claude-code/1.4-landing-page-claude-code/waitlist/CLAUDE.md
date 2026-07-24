# CyberShield.AI — Waitlist Landing Page

## עסק
- **שם:** CyberShield.AI
- **קהל יעד:** חברות וסטארטאפים שמחפשים הגנת ענן מבוססת AI
- **מיקום:** תל אביב, ישראל
- **מטרת הדף:** איסוף אימיילים לרשימת המתנה (גרסת בטא מוקדמת)

## מבנה הדף
דף נחיתה מינימליסטי — עמוד אחד, מרכוז מלא (centered layout).

| אלמנט | תוכן |
|-------|------|
| Badge | סטטוס "גרסת בטא מוקדמת" עם `animate-ping` |
| Icon | לוגו מגן עם גרדיאנט indigo→cyan |
| Headline | "דור העתיד של אבטחת ענן" |
| Subheadline | תיאור קצר 2 שורות |
| Form | שדה אימייל + כפתור הרשמה |
| Counter | "240+ חברות ממתינות" |

## ערכת עיצוב
- **אווירה:** Dark mode, הייטק ישראלי, עתידני
- **רקע:** `#07091A` (שחור-כחול עמוק)
- **Primary:** Indigo-600 (`#4F46E5`)
- **Accent:** Cyan-400 (`#22D3EE`)
- **Glow:** עיגולי `blur` מטושטשים + `animate-pulse` ברקע קבוע
- **Framework:** Tailwind CSS CDN — חייב חיבור אינטרנט להצגה

## כללי פיתוח
- אנימציות: **Tailwind classes בלבד** — `animate-pulse`, `animate-ping`, `transition-all`, `hover:scale-*`
- שפה: עברית RTL — `dir="rtl"` ב-`<html>`, שדה האימייל עם `dir="ltr"`
- אין תלויות נוספות מלבד Tailwind CDN
- הטופס: feedback ויזואלי מיידי לאחר submit (גוון ירוק + הודעת אישור)
- קונטרסט: slate-100 על רקע חשוך — WCAG AA לפחות
