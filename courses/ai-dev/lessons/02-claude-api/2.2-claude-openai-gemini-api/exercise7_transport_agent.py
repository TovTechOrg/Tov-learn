import os
import random
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# --- Mock Transport API ---

def get_next_bus(station_id: int, city: str) -> str:
    """מחזיר את זמן הגעת האוטובוס הבא לתחנה נתונה.

    Args:
        station_id: מספר התחנה.
        city: שם העיר.
    """
    print(f"  [Tool] get_next_bus(station_id={station_id}, city='{city}')")
    supported = ["תל אביב", "ירושלים", "חיפה"]
    if city not in supported:
        return json.dumps({"error": f"אין נתונים עבור העיר {city}"}, ensure_ascii=False)
    minutes = random.randint(5, 15)
    return json.dumps({"station_id": station_id, "city": city, "minutes_until_arrival": minutes}, ensure_ascii=False)

def plan_trip(origin: str, destination: str) -> str:
    """מתכנן מסלול נסיעה בתחבורה ציבורית בין שתי ערים.

    Args:
        origin: עיר המוצא.
        destination: עיר היעד.
    """
    print(f"  [Tool] plan_trip(origin='{origin}', destination='{destination}')")
    if origin == "תל אביב" and destination == "ירושלים":
        return json.dumps({
            "route": "קו 480",
            "departure": "תחנה מרכזית תל אביב",
            "arrival": "תחנה מרכזית ירושלים",
            "duration_minutes": 60
        }, ensure_ascii=False)
    return json.dumps({"error": f"לא נמצא מסלול מ-{origin} ל-{destination}"}, ensure_ascii=False)

# --- Agent ---

SYSTEM_PROMPT = """אתה ריילי, עוזר תכנון נסיעות חכם וידידותי של "רב-קו אונליין".
אתה עוזר למשתמשים לתכנן נסיעות בתחבורה ציבורית בישראל.
עליך לזכור את הקשר השיחה — אם המשתמש אמר "משם" או "שם", הבן על מה הוא מדבר מתוך ההיסטוריה.
ענה תמיד בעברית, בסגנון ידידותי וקצר."""

chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=[get_next_bus, plan_trip]
    )
)

print("ריילי — עוזר תחבורה ציבורית 🚌  (הקלד 'יציאה' לסיום)\n")

while True:
    user_input = input("אתה: ").strip()
    if not user_input:
        continue
    if user_input == "יציאה":
        break

    response = chat.send_message(user_input)
    print(f"ריילי: {response.text}\n")
