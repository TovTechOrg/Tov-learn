<div dir="rtl">

# פרויקטי גמר – קורס AI Dev

## הנחיות כלליות

בחרו **פרויקט אחד** מתוך ארבעה. כל הפרויקטים חייבים לעמוד בדרישות הבאות:

- **פועל בפרודקשן** — לא localhost. כתובת ציבורית שאפשר לפתוח מכל מקום
- **CLAUDE.md מתועד** — מתאר את הפרויקט, ה-Tech Stack, וה-Conventions
- **עלות תפעול מוגדרת** — חישוב מדויק: כמה עולה לרוץ עם 100 בקשות ביום
- **מצגת 10 דקות + הדגמה חיה** — הדגמה שנכשלת בפני הכיתה לא עוברת
- **קוד ב-GitHub** — עם commit history אמיתי, לא push אחד בסוף

**לגבי מודל AI:** כל הפרויקטים משתמשים ב-**Vertex AI API (Google Cloud)** לקריאות בתשלום — `vertexai.generative_models.GenerativeModel`. מי שיש לו קרדיטים אצל ספק אחר יכול להחליף, אבל הקוד צריך לתמוך ב-Provider Abstraction (החלפת מודל בשינוי env var אחד).

---

## פרויקט א: מערכת תמיכת לקוחות AI עם WhatsApp

**מודולים נדרשים:** 1 (Claude Code) + 2 (API, Webhooks, Structured Output)
**זמן מוערך:** 14 שעות
**רמת קושי:** בינונית-גבוהה

### מה בונים

מערכת תמיכת לקוחות end-to-end: לקוח שולח הודעת WhatsApp, Gemini קורא את Knowledge Base מ-Supabase ועונה אוטומטית. אם רמת הביטחון נמוכה מ-70%, הפנייה עוברת לנציג אנושי עם כל ההקשר. הנציג רואה את כל ההיסטוריה ב-Dashboard שבנויה ב-Next.js.

### תרשים זרימה

```
WhatsApp נכנס
    ↓
Webhook (Cloudflare Worker)
    ↓
Vertex AI API — קורא Knowledge Base מ-Supabase
    ↓
confidence ≥ 70%? ──── כן ──── תשובה אוטומטית בחזרה ל-WhatsApp
    │
    לא
    ↓
סימון "ממתין לנציג" + התראה ל-Dashboard
    ↓
נציג רואה שיחה + הקשר מלא + עונה מה-Dashboard
```

### דרישות טכניות

| רכיב | פרטים |
|-------|--------|
| **בנייה** | Claude Code — כל הקוד |
| **Frontend** | Next.js + Tailwind — Dashboard לניהול פניות |
| **Backend / DB** | Supabase — טבלאות: `tickets`, `messages`, `knowledge_base` |
| **AI** | Vertex AI (gemini-2.5-flash) — Structured Output: `{answer, confidence, sources}` |
| **WhatsApp** | Meta Cloud API — Webhook לקבלה, HTTP לשליחה |
| **Hosting** | Cloudflare Workers (Webhook) + Cloudflare Pages (Dashboard) |

### שלבי הפרויקט

**שלב 1 — Spec, CLAUDE.md, ומסד נתונים (1.5 שעות)**

כתבו `SPEC.md` עם מודל הנתונים המלא:
```sql
tickets: id, wa_phone, status (open/auto_resolved/escalated/closed), created_at
messages: id, ticket_id, role (user/assistant/agent), content, confidence, created_at
knowledge_base: id, category, question, answer, embedding (vector)
```

כתבו `CLAUDE.md` ובקשו מ-Claude Code לבנות את הסכמה ב-Supabase.

**שלב 2 — Webhook + Gemini Integration (3 שעות)**

בקשו מ-Claude Code לבנות Cloudflare Worker שמקבל Webhook מ-WhatsApp.
לאחר מכן, הוסיפו קריאת Gemini עם Structured Output:

```python
response_schema = {
    "type": "object",
    "properties": {
        "answer": {"type": "string"},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "sources": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["answer", "confidence", "sources"]
}
```

Gemini מקבל: הודעת הלקוח + 3 תוצאות רלוונטיות מה-Knowledge Base (חיפוש ב-Supabase Vector). מחזיר Structured JSON.

**שלב 3 — WhatsApp Business API (2.5 שעות)**

1. הרשמה ל-Meta for Developers
2. יצירת WhatsApp Business App וחיבור מספר טלפון
3. הגדרת Webhook URL (ה-Cloudflare Worker מהשלב הקודם)
4. בנייה עם Claude Code: פונקציות `send_text_message()` ו-`send_reply_button_message()`
5. בדיקה: שלחו הודעה אמיתית מהטלפון וקבלו תשובה אוטומטית

**שלב 4 — Dashboard לנציגים (3 שעות)**

בקשו מ-Claude Code לבנות Dashboard ב-Next.js:
- רשימת פניות עם סינון לפי סטטוס
- מסך שיחה עם היסטוריה מלאה + הצעת תשובה מ-Gemini
- כפתור "שלח תשובה" שמעדכן את WhatsApp ומסגר את הכרטיס
- מד Confidence לכל תשובה אוטומטית

**שלב 5 — Code Review, Deploy, תיעוד (4 שעות)**

הריצו `/review` על כל הקוד. בדקו במיוחד: HMAC validation על ה-Webhook (חובה לאבטחה). Deploy. מלאו Knowledge Base עם 20 שאלות ותשובות אמיתיות ובדקו End-to-End.

חשבו עלויות: Vertex AI (gemini-2.5-flash) = $0.075 לכל מיליון Output Tokens. עם 100 שיחות/יום × 500 Tokens תשובה = כמה?

### Checklist

- [ ] WhatsApp Webhook עם HMAC Validation
- [ ] Gemini Structured Output עם `confidence` score
- [ ] לוגיק Escalation: confidence < 70% → נציג
- [ ] Knowledge Base ב-Supabase עם לפחות 20 רשומות
- [ ] Dashboard מציג פניות פתוחות + היסטוריה
- [ ] נציג יכול לשלוח תשובה ישירות מה-Dashboard
- [ ] CLAUDE.md + README
- [ ] Deploy: Webhook + Dashboard
- [ ] חישוב עלות ל-100 שיחות/יום
- [ ] הדגמה חיה: שלחו הודעה מהטלפון בפני הכיתה

### עלויות משוערות

| שירות | עלות |
|--------|------|
| Vertex AI (gemini-2.5-flash) | ~$1-3/חודש (100 req/יום) |
| Supabase Free | חינם |
| Cloudflare Workers Free | חינם |
| Cloudflare Pages | חינם |
| WhatsApp Meta Cloud API | חינם (עד 1,000 שיחות שירות/חודש) |
| **סה"כ** | **~$1-3/חודש** |

---

## פרויקט ב: Document Intelligence Service

**מודולים נדרשים:** 1 (Claude Code) + 2 (Webhooks, Structured Output, Python)
**זמן מוערך:** 12 שעות
**רמת קושי:** בינונית-גבוהה

### מה בונים

שירות ווב שמקבל מסמכים (PDF, CSV, URL לאתר) ומחזיר נתונים מובנים — עם Vertex AI Structured Output + Pydantic schema מוגדר מראש. יש Dashboard לניהול וצפייה בתוצאות, ו-REST API לשאר המערכות. נבנה לגמרי עם Claude Code.

**הדגמה שמרשימה:** מעלים חוזה PDF → תוך 10 שניות מקבלים JSON עם: שמות הצדדים, תאריכי תוקף, סכום, וסעיפי ביטול. כולם בפורמט שאפשר לשלוח ישירות ל-CRM.

### בחירת Domain — בחרו אחד

**אפשרות 1: חוזים ומסמכים משפטיים**
Schema: `{parties, start_date, end_date, value_ils, payment_terms, termination_clauses, governing_law}`

**אפשרות 2: חשבוניות וקבלות**
Schema: `{vendor, date, items: [{description, qty, unit_price}], subtotal, vat, total, currency}`

**אפשרות 3: קורות חיים (HR)**
Schema: `{name, email, years_experience, skills, last_role, education, languages, red_flags}`

**אפשרות 4: דפי מוצר / Landing Pages**
Schema: `{product_name, pricing_tiers, key_features, target_audience, cta_text, competitors_mentioned}`

### דרישות טכניות

| רכיב | פרטים |
|-------|--------|
| **בנייה** | Claude Code |
| **Frontend** | Next.js + Tailwind — Dashboard + Upload UI |
| **API** | Next.js API Routes — upload endpoint + query endpoint |
| **Storage** | Cloudflare R2 (קבצים) + Supabase (תוצאות JSON) |
| **AI** | Vertex AI — Structured Output עם Pydantic schema |
| **Deploy** | Cloudflare Pages (Next.js) |
| **Auth** | API Key פשוט בהדר לגישת ה-REST API |

### שלבי הפרויקט

**שלב 1 — Spec ו-CLAUDE.md (1 שעה)**

הגדירו את ה-Pydantic Schema המדויק שאתם מחלצים. זה ה-לב של הפרויקט:

```python
from pydantic import BaseModel, Field
from datetime import date

class ContractExtraction(BaseModel):
    parties: list[str] = Field(description="Names of all signing parties")
    start_date: date | None = Field(description="Contract start date, null if not found")
    end_date: date | None = Field(description="Contract end date or expiry")
    value_ils: float | None = Field(description="Total contract value in ILS, null if not monetary")
    payment_terms: str = Field(description="Payment schedule description")
    termination_clauses: list[str] = Field(description="Conditions under which contract can be terminated")
    confidence: float = Field(description="0-1 confidence score for the extraction")
```

כתבו `CLAUDE.md` ובקשו מ-Claude Code להקים Next.js + Supabase + Cloudflare R2.

**שלב 2 — Upload Endpoint + Vertex AI (4 שעות)**

בנו עם Claude Code את ה-Upload flow:
1. `POST /api/upload` — מקבל קובץ, שומר ב-R2, מחזיר `document_id`
2. עיבוד אסינכרוני: שולף קובץ מ-R2, שולח ל-Vertex AI עם Schema, שומר JSON ב-Supabase

```python
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import json

vertexai.init(project=GCP_PROJECT, location="us-central1")

def extract_document(file_bytes: bytes, mime_type: str, schema: type) -> dict:
    model = GenerativeModel("gemini-2.5-flash")
    
    prompt = f"""Extract the following information from this document.
    Return a JSON object that strictly follows this schema:
    {schema.model_json_schema()}
    
    If a field cannot be found, use null. Include a confidence score (0-1).
    Return ONLY valid JSON, no explanation."""
    
    response = model.generate_content(
        [Part.from_data(file_bytes, mime_type=mime_type), prompt],
        generation_config={"response_mime_type": "application/json"}
    )
    
    result = json.loads(response.text)
    return schema(**result).model_dump()  # Pydantic validation
```

**שלב 3 — Dashboard (3 שעות)**

בקשו מ-Claude Code לבנות Dashboard:
- טבלת מסמכים עם סטטוס (processing / done / failed)
- לחיצה על שורה → פנל עם ה-JSON המחולץ בצורה קריאה
- כפתור Upload חדש
- סינון לפי תאריך / confidence score

**שלב 4 — REST API + Deploy (2 שעות)**

הוסיפו `GET /api/documents` ו-`GET /api/documents/{id}` עם API Key authentication בהדר.
בדקו עם curl שהחיצוני יכול לשלוף את הנתונים.

Deploy ל-Cloudflare Pages: `wrangler pages deploy`.

**שלב 5 — בדיקה End-to-End + הדגמה (2 שעות)**

העלו 5 מסמכים אמיתיים (אפשר דוגמאות). בדקו:
- accuracy: כמה שדות חולצו נכון?
- confidence score: האם מתאים?
- edge cases: מסמך סרוק גרוע, שפה אחרת, שדה חסר

חשבו עלות ל-100 מסמכים/יום.

### Checklist

- [ ] Pydantic Schema מוגדר עם לפחות 6 שדות + `confidence`
- [ ] Upload endpoint + עיבוד Vertex AI
- [ ] תוצאות JSON שמורות ב-Supabase
- [ ] Dashboard: רשימה + פנל + Upload UI
- [ ] REST API עם API Key Auth
- [ ] Deploy על Cloudflare Pages
- [ ] נבדק על 5 מסמכים אמיתיים — accuracy documented
- [ ] חישוב עלות ל-100 מסמכים/יום
- [ ] הדגמה: upload PDF בפני הכיתה ← JSON מוצג תוך 15 שניות

### עלויות משוערות

| שירות | עלות |
|--------|------|
| Vertex AI (100 docs/יום × ~2K tokens) | ~$3-5/חודש |
| Cloudflare Pages + R2 (10GB) | חינם / ~$1.5/חודש |
| Supabase Free | חינם |
| **סה"כ** | **~$3-7/חודש** |

---

## פרויקט ג: סוכן Intelligence יומי עם Telegram

**מודולים נדרשים:** 2 (Tool Use, Agent Loop, Python Patterns)
**זמן מוערך:** 12 שעות
**רמת קושי:** גבוהה

### מה בונים

סוכן Python שרץ על Schedule, אוסף מידע ממספר מקורות (אתרים, RSS, APIs), מנתח ומסכם עם Vertex AI API, ושולח דוח יומי מובנה ל-Telegram Channel או Group. הסוכן מיישם Agent Loop מאפס — ללא Framework חיצוני.

Telegram (ולא WhatsApp) — כי מדובר בהתראות פנימיות לצוות / למפתחים, לא תקשורת עם לקוחות. Telegram Bot API פשוט יותר, ללא אישורים של Meta, ומתאים להתראות טכניות.

### שלוש אפשרויות לסוכן — בחרו אחת

**אפשרות 1: Competitive Intelligence Agent**
כל בוקר בשעה 7:00 — בודק 5-10 מתחרים מוגדרים: מחירים שהשתנו, מוצרים חדשים, פוסטים חדשים בבלוג, שינויים בעמוד ה-Pricing. מסכם ב-Vertex AI ושולח ל-Telegram: "3 דברים שקרו אצל המתחרים היום."

**אפשרות 2: Industry News Digest Agent**
כל יום — קורא RSS Feeds + Hacker News + Reddit ו-Twitter/X handles רלוונטיים. מסנן עם Vertex AI: רק מה שרלוונטי לתחום (לפי קריטריונים מוגדרים). מייצר Digest יומי עם 5-10 פריטים + פסקת "Takeaway" — מוכן לפרסום כפוסט לינקדאין.

**אפשרות 3: Personal Research Assistant Agent**
מקבל שאלת מחקר פעם בשבוע (מ-Telegram עצמו או מקובץ config), מריץ מחקר מעמיק: מחפש, קורא מאמרים, מסכם ממצאים, מזהה סתירות בין מקורות. מחזיר דוח מובנה: Executive Summary, Key Findings, Open Questions.

### דרישות טכניות

| רכיב | פרטים |
|-------|--------|
| **AI** | Vertex AI API — Tool Use + Agent Loop |
| **Agent Loop** | מיושם ידנית. לא LangChain, לא AutoGen |
| **Tools** | לפחות 5: מקורות קלט שונים + `send_telegram_report` |
| **Telegram** | Bot API — `sendMessage` עם Markdown formatting |
| **Scheduling** | Cloudflare Cron Triggers |
| **Logging** | כל Tool Call: שם, פרמטרים, תוצאה, זמן |
| **Cost Tracking** | Tokens + עלות מדויקת אחרי כל ריצה |
| **Deploy** | Cloudflare Workers — long-running process |

### שלבי הפרויקט

**שלב 1 — הגדרה ו-Telegram Bot (1 שעה)**

1. הגדירו: איזו אפשרות בחרתם, מה מקורות המידע, מה פורמט הפלט
2. צרו Telegram Bot דרך @BotFather, קבלו `BOT_TOKEN`
3. צרו Channel/Group, הוסיפו את הבוט, קבלו `CHAT_ID`
4. בדיקה בסיסית:
```python
import httpx

def send_telegram(text: str):
    httpx.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    )
```

**שלב 2 — Agent Loop עם Vertex AI (3 שעות)**

```python
import vertexai
from vertexai.generative_models import GenerativeModel, FunctionDeclaration, Tool, Part

vertexai.init(project=GCP_PROJECT, location="us-central1")

def agent_loop(task: str, tool_declarations: list[FunctionDeclaration],
               max_iterations: int = 15) -> str:
    model = GenerativeModel(
        "gemini-2.5-flash",
        tools=[Tool(function_declarations=tool_declarations)]
    )
    chat = model.start_chat()
    response = chat.send_message(task)

    for i in range(max_iterations):
        fn_calls = [p for p in response.candidates[0].content.parts if p.function_call]

        if not fn_calls:
            return response.candidates[0].content.parts[0].text  # סיום

        results = []
        for part in fn_calls:
            name = part.function_call.name
            args = dict(part.function_call.args)
            result = execute_tool(name, args)
            log_tool_call(i, name, args, result)
            results.append(Part.from_function_response(name=name, response={"result": result}))

        response = chat.send_message(results)

    raise RuntimeError(f"Agent exceeded {max_iterations} iterations")
```

בנו עם Tool אחד (חיפוש פשוט). בדקו שהלולאה עובדת לפני שממשיכים.

**שלב 3 — Tools + `send_telegram_report` (4 שעות)**

בנו את כל ה-Tools בהתאם לאפשרות שבחרתם. הגדירו `FunctionDeclaration` מפורטת — Vertex AI קורא את ה-`description` כדי להחליט מתי לקרוא לכל Tool.

ה-Tool האחרון תמיד: `send_telegram_report(title, sections, takeaway)` — מפרמט ושולח:
```
📊 *Daily Intelligence Report — 28.05.2026*

*🔍 מה חדש אצל המתחרים:*
• Competitor A הוריד מחיר ב-15% ל-Pro Plan
• Competitor B פרסם Feature חדש: AI Summarization

*💡 Takeaway:*
שניים מהמתחרים המרכזיים זזו לכיוון AI features השבוע.

_⏱ זמן ריצה: 42 שניות | עלות: $0.008_
```

**שלב 4 — Scheduler + Deploy (2.5 שעות)**

במקום APScheduler, משתמשים ב-**Cloudflare Cron Triggers** — ה-Worker מופעל אוטומטית לפי לוח זמנים:

```jsonc
// wrangler.jsonc
"triggers": {
  "crons": ["0 5 * * 1-5"]   // 07:00 ישראל = 05:00 UTC, ימים א'-ה'
}
```

```python
# worker.py
async def on_scheduled(event, env, ctx):
    logger.info("Agent run started")
    try:
        await agent_loop(DAILY_TASK, TOOL_DECLARATIONS)
    except Exception as e:
        send_telegram(f"⚠️ Agent failed: {e}")
```

```bash
wrangler deploy
wrangler trigger cron  # בדיקה ידנית לפני ההגשה
```

Deploy עם `wrangler deploy`. בדקו שה-Cron מופיע ב-Cloudflare Dashboard תחת Workers → Triggers.

**שלב 5 — הדגמה (0.5 שעות)**

הריצו ידנית בפני הכיתה. הראו: הלולאה, ה-Tool Calls ב-Logs, הדוח ב-Telegram בזמן אמת.

### Checklist

- [ ] Telegram Bot פועל ושולח Markdown מפורמט
- [ ] Agent Loop מיושם ידנית עם Vertex AI
- [ ] לפחות 5 Tools עם FunctionDeclarations מפורטות
- [ ] Tool אחרון הוא `send_telegram_report`
- [ ] max_iterations + שגיאה ל-Telegram אם Agent נכשל
- [ ] Logging: כל Tool Call עם timestamp
- [ ] Cost Tracking: Tokens + עלות בסוף כל ריצה + נשלח ב-Telegram
- [ ] Cloudflare Cron Trigger מוגדר ב-wrangler.jsonc בזמן ישראל
- [ ] הדגמה חיה: הסוכן רץ ושולח ל-Telegram בפני הכיתה

### עלויות משוערות

| שירות | עלות |
|--------|------|
| Vertex AI (ריצה יומית ~15K Tokens) | ~$0.50-1/חודש |
| Cloudflare Workers (Cron Triggers) | חינם (100K req/יום) |
| Telegram Bot API | חינם |
| **סה"כ** | **~$0.50-1/חודש (Vertex AI בלבד)** |

---

## פרויקט ד: מנוע Code Review אוטונומי — GitHub Integration

**מודולים נדרשים:** 1 (Claude Code) + 2 (Webhooks, Tool Use, Agent Loop, Python)
**זמן מוערך:** 16 שעות
**רמת קושי:** גבוהה

### מה בונים

שרת שמקשיב ל-GitHub Webhooks: כשנפתח PR חדש, Orchestrator שולף את ה-diff, מפעיל במקביל שלושה Specialist Agents (Security / Performance / Code Quality), ומפרסם תוצאות כ-GitHub PR Comment מובנה. כולו deployed, כולו אוטומטי.

### תרשים זרימה

```
GitHub PR נפתח
    ↓
Webhook → שרת FastAPI
    ↓
Orchestrator — שולף diff, מפרק לקטעים
    ↓
┌─────────────┬──────────────┬─────────────────┐
Security      Performance    Code Quality
Specialist    Specialist     Specialist
(Gemini)      (Gemini)       (Gemini)
    └─────────────┴──────────────┘
                 ↓
        Orchestrator מחבר תוצאות
                 ↓
        GitHub PR Comment
```

### דרישות טכניות

| רכיב | פרטים |
|-------|--------|
| **בנייה** | Claude Code — בנה את כל הקוד |
| **Webhook Server** | FastAPI + ngrok (dev) → Cloudflare Tunnel (prod) |
| **Orchestrator** | Python — שולף diff, מחלק, מאחד תוצאות |
| **Specialists** | 3 Gemini Agents מקבילים עם Tool Use |
| **GitHub Integration** | PyGitHub — קריאת PR, כתיבת Comment |
| **Deploy** | Cloudflare Workers — long-running FastAPI server |

### Specialist Agents — מה כל אחד בודק

**Security Specialist:**
- הרשאות שגויות, credentials hardcoded, SQL Injection, XSS
- Input validation חסר, sensitive data בלוגים
- כל ממצא: {severity: critical/high/medium, line: N, description, fix}

**Performance Specialist:**
- N+1 Queries, חוסר Pagination, חוסר Caching, Blocking I/O
- חישובים כבדים ב-main thread, objects גדולים בזיכרון
- כל ממצא: {type, estimated_impact, line, suggestion}

**Code Quality Specialist:**
- כפילות קוד, naming conventions, Magic Numbers, קוד ללא טיפול שגיאות
- פונקציות ארוכות מדי, missing docstrings ל-public APIs
- כל ממצא: {category, line, issue, refactoring_suggestion}

### שלבי הפרויקט

**שלב 1 — הקמה ו-CLAUDE.md (1 שעה)**

בקשו מ-Claude Code להקים:
- FastAPI project עם Poetry / uv
- GitHub Webhook handler עם HMAC validation
- PyGitHub connection
- Logging מובנה

**שלב 2 — GitHub Integration (2 שעות)**

בנו עם Claude Code:
```python
def fetch_pr_diff(repo_name: str, pr_number: int) -> str:
    """שולף diff של PR. מחזיר unified diff כ-string."""

def post_review_comment(repo_name: str, pr_number: int, review: ReviewResult):
    """מפרסם Comment מובנה ב-PR עם ממצאי Review."""
```

בדקו: פתחו PR אמיתי ב-repo לדוגמה, וודאו שה-diff מגיע ו-comment נכתב נכון.

**שלב 3 — Specialist Agent אחד (3 שעות)**

בנו את Security Specialist קודם:
- System Prompt מפורט עם הנחיות ספציפיות
- Vertex AI API עם `response_mime_type="application/json"` ו-Schema מוגדר
- בדיקה על diff אמיתי

רק אחרי שעובד — בנו Performance ו-Code Quality.

**שלב 4 — Orchestrator + מקביליות (3 שעות)**

```python
import asyncio

async def run_review(diff: str) -> ReviewResult:
    results = await asyncio.gather(
        run_security_specialist(diff),
        run_performance_specialist(diff),
        run_quality_specialist(diff),
        return_exceptions=True
    )
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            logger.error(f"Specialist {i} failed: {result}")
    
    return merge_results([r for r in results if not isinstance(r, Exception)])
```

בדקו שכל שלושת הסוכנים רצים ב-parallel ולא sequential.

**שלב 5 — פורמט Comment ו-Deploy (4 שעות)**

הפלט צריך להיות Comment GitHub מובנה:
```markdown
## 🤖 AI Code Review

### 🔒 Security (2 ממצאים)
| חומרה | שורה | ממצא | פתרון |
|-------|------|-------|-------|
| 🔴 Critical | 42 | ... | ... |

### ⚡ Performance (1 ממצא)
...

### 📝 Code Quality (3 ממצאים)
...

---
*נסרק על-ידי Vertex AI (gemini-2.5-flash) | זמן: 8.3 שניות | עלות: $0.003*
```

Deploy ל-Cloudflare Workers. הגדירו GitHub Webhook עם URL של Cloudflare Workers.

**שלב 6 — בדיקה End-to-End + הדגמה (3 שעות)**

הכינו PR לדוגמה עם בעיות ידועות (credentials hardcoded, N+1 Query, Magic Numbers). פתחו אותו ב-GitHub. הדגימו את ה-Comment שנוצר אוטומטית בפני הכיתה.

מדדו: כמה שניות לרוץ, כמה עולה לבדיקה ממוצעת (diff של 200 שורות).

### Checklist

- [ ] GitHub Webhook עם HMAC Validation
- [ ] שלושה Specialist Agents: Security, Performance, Code Quality
- [ ] ריצה מקבילית עם `asyncio.gather`
- [ ] Specialist שנכשל לא עוצר את האחרים
- [ ] PR Comment מובנה בפורמט Markdown
- [ ] Comment כולל: זמן ריצה + עלות
- [ ] Deployed ב-Cloudflare Workers עם Webhook פעיל
- [ ] CLAUDE.md מתאר את ארכיטקטורת הסוכנים
- [ ] הדגמה: פתיחת PR בזמן אמת ← Review מופיע תוך 15 שניות

### עלויות משוערות

| שירות | עלות |
|--------|------|
| Vertex AI (gemini-2.5-flash) (20 PRs/יום × 3 Specialists × 5K tokens) | ~$3-5/חודש |
| Cloudflare Workers | ~$5/חודש |
| **סה"כ** | **~$8-10/חודש** |

---

## קריטריונים להערכה (כל הפרויקטים)

| קריטריון | משקל | מה בודקים |
|-----------|------|-----------|
| עובד בפרודקשן | 25% | URL פעיל, הדגמה לא נופלת |
| עומק טכני | 25% | Tool Descriptions, Structured Output, Error Handling |
| שימוש ב-Claude Code | 20% | Commit History, CLAUDE.md, Code Review |
| תיעוד + עלויות | 15% | README, חישוב עלות מדויק |
| מצגת + הדגמה חיה | 15% | 10 דקות, הדגמה שעובדת בזמן אמת |

</div>
