<div dir="rtl">

# SPEC.md — Document Intelligence Service: תוכניות חינוכיות יחידניות (תח"י)

## בחירת Domain

**נבחרה אפשרות 1 (חוזים ומסמכים משפטיים), מותאמת לתחום החינוך המיוחד.**

הנימוק: מסמך תח"י / החלטת ועדת שילוב הוא מבנית מסמך משפטי-מנהלי — יש בו צדדים
(הורים, בית ספר, רשות), תוקף בזמן, תנאים לשינוי סטטוס, ונוהל/חוק מסגרת. השדות
המקוריים הותאמו לתוכן הספציפי (ראו טבלת מיפוי בהמשך) במקום שימוש ישיר בשמות
השדות הגנריים.

| שדה מקורי (אפשרות 1) | שדה מותאם | הסבר |
|---|---|---|
| `parties` | (מפוצל ל-`disability_category`, `placement_type` וכו') | אין "צדדים" חוזיים קלאסיים; הוחלף בתוכן מהותי של ההחלטה |
| `start_date` / `end_date` | `review_date` | תאריך התוקף/העדכון הבא של התוכנית |
| `value_ils` | `weekly_support_hours` | ההיקף הכמותי המרכזי הוא שעות תמיכה, לא סכום כספי |
| `payment_terms` | — | לא רלוונטי; הושמט |
| `termination_clauses` | (חלק מ-`goals`/הערות) | תנאים לשינוי שיבוץ, אם קיימים במסמך |
| `governing_law` | — | לא נדרש בשלב זה; ניתן להוסיף כשדה עתידי (`legal_basis`) |

## Pydantic Schema

```python
from pydantic import BaseModel, Field
from datetime import date

class IEPExtraction(BaseModel):
    student_id: str | None = Field(description="מזהה תלמיד פנימי בלבד — לעולם לא שם מלא")
    school_year: str = Field(description="שנת לימודים, למשל תשפ״ז")
    disability_category: str | None = Field(description="קטגוריית הליקוי כפי שמופיע במסמך")
    placement_type: str = Field(description="הכלה מלאה / הכלה חלקית / כיתה מיוחדת / חינוך מיוחד נפרד")
    weekly_support_hours: float | None = Field(description="שעות תמיכה שבועיות שהוקצו")
    goals: list[str] = Field(description="יעדים חינוכיים/טיפוליים כפי שמופיעים בתוכנית")
    review_date: date | None = Field(description="תאריך הוועדה או עדכון התוכנית הבא")
    accommodations: list[str] = Field(description="התאמות נדרשות (בחינות, סביבה לימודית וכו׳)")
    confidence: float = Field(description="0-1 ציון ביטחון בחילוץ")
```

## מודל נתונים (Supabase)

```sql
documents: id, storage_path (R2), status (processing/done/failed), uploaded_at
extractions: id, document_id (FK), student_id, school_year, disability_category,
             placement_type, weekly_support_hours, goals (jsonb), review_date,
             accommodations (jsonb), confidence, created_at
student_identity_map: student_id, real_name_encrypted   -- טבלה נפרדת, הרשאות מוגבלות בלבד
```

## זרימת המערכת

```
POST /api/upload (PDF/סרוק)
    ↓ שומר קובץ ב-Cloudflare R2, יוצר document_id, מחזיר מיד (status=processing)
    ↓
Background job:
    1. חילוץ טקסט מהמסמך
    2. שכבת Redaction — הסרת שם מלא/ת.ז. לפני שליחה ל-Vertex AI (regex/NER)
    3. Vertex AI (gemini-2.5-flash) — Structured Output לפי IEPExtraction
    4. שמירת התוצאה ב-Supabase (extractions), עדכון status=done
    ↓
Outgoing Webhook (HMAC-signed) → התראה לדשבורד/Telegram: "מסמך X עובד, confidence: 0.87"
```

## דרישות אבטחה ופרטיות

- שם מלא/ת.ז. **אינם** נשלחים ל-Vertex AI (ספק חיצוני) — Redaction חובה לפני הקריאה.
- `student_id` הוא המזהה היחיד המשמש בטבלת `extractions`; המיפוי לזהות אמיתית
  מנותק בטבלה נפרדת עם הרשאות מחמירות.
- Webhook יוצא חתום ב-HMAC.
- REST API מוגן ב-API Key.

## Checklist עדכני (בהתאם למסמך הקורס, פרויקט ב')

- [ ] Pydantic Schema עם לפחות 6 שדות + `confidence`
- [ ] שכבת Redaction לפני קריאת Vertex AI
- [ ] Upload endpoint + עיבוד אסינכרוני + Outgoing Webhook עם HMAC
- [ ] תוצאות ב-Supabase, טבלת מיפוי זהות מופרדת
- [ ] Dashboard: רשימה + פנל + Upload UI
- [ ] REST API עם API Key Auth
- [ ] נבדק על מדגם מסמכים (אמיתיים/סינתטיים) — accuracy מתועד
- [ ] חישוב עלות ל-100 מסמכים/יום

</div>
