import json, os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LEADS_FILE = os.path.join(SCRIPT_DIR, 'leads.json')

def classify_leads(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        leads = json.load(f)

    classified_leads = []  # <-- רשימה אחת, מחוץ ללולאה

    for lead in leads:
        try:
            company = lead["company"]
            prompt = f"בהתבסס על שם החברה '{company}', מהו תחום הפעילות המרכזי שלה? (לדוגמה: פיננסים, קמעונאות, סייבר, פארמה). החזר אך ורק מילה או שתיים, ללא הסברים וללא תהליך חשיבה."
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_budget=0)
                )
            )
            lead["industry"] = response.text.strip()
            classified_leads.append(lead)
        except KeyError:
            print(f"שגיאה בעיבוד ליד: {lead.get('name', 'לא ידוע')}. שדה חסר.")

    with open(os.path.join(SCRIPT_DIR, 'classified_leads.json'), 'w', encoding='utf-8') as f:
        json.dump(classified_leads, f, ensure_ascii=False, indent=4)

    print("עיבוד לידים הושלם.")

classify_leads(LEADS_FILE)
