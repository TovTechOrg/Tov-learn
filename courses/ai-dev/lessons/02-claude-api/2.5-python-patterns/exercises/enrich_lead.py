# enrich_lead.py
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# --- Lead Information ---
lead_name = "רוני מאור"
lead_company = "סאפיינס טכנולוגיות"
lead_title = "מנהלת פרויקטים בכירה"

# 1. Initialize the Gemini client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 2. Create the prompt
prompt = f"""
אני צריך לכתוב מייל קר לליד בשם {lead_name}, שעובד/ת כ-{lead_title} בחברת {lead_company}.
אנא נסח עבורי משפט פתיחה קצר (עד 20 מילים) למייל, שיהיה מקצועי, מותאם אישית לתפקיד ולחברה, ובטון ישראלי.
"""

# 3. Call the API
print("מייצר משפט פתיחה עם Gemini...")
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

# 4. Print the result
print(f"הצעה למשפט פתיחה:\n{response.text}")
