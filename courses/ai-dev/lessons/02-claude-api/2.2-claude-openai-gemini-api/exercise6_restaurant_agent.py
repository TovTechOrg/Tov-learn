import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# --- Mock Restaurant API ---
MENU = {
    "פיצה מרגריטה": 55,
    "פסטה קרבונרה": 68,
    "לזניה בולונז": 72,
    "פפרדלה ראגו": 75,
    "סלט קיסר": 48
}
INVENTORY = {
    "פיצה מרגריטה": 20,
    "פסטה קרבונרה": 15,
    "לזניה בולונז": 0,
    "פפרדלה ראגו": 10,
    "סלט קיסר": 30
}

def get_menu() -> str:
    """מחזיר את התפריט המלא של המסעדה עם מחירים."""
    print("  [Tool] get_menu()")
    return json.dumps(MENU, ensure_ascii=False)

def check_availability(dish_name: str, quantity: int) -> str:
    """בודק אם כמות מסוימת של מנה זמינה במלאי.

    Args:
        dish_name: שם המנה לבדיקה.
        quantity: הכמות המבוקשת.
    """
    print(f"  [Tool] check_availability(dish_name='{dish_name}', quantity={quantity})")
    if dish_name not in INVENTORY:
        return json.dumps({"available": False, "reason": "המנה לא נמצאה בתפריט"}, ensure_ascii=False)
    if INVENTORY[dish_name] >= quantity:
        return json.dumps({"available": True, "message": f"יש לנו {quantity} מנות במלאי"}, ensure_ascii=False)
    else:
        return json.dumps({"available": False, "reason": f"יש לנו רק {INVENTORY[dish_name]} מנות"}, ensure_ascii=False)

SYSTEM_PROMPT = """אתה עוזר הזמנות של המסעדה האיטלקית 'פסטה בנגב' בבאר שבע.
אתה אדיב, מועיל, ועונה רק בעברית.
השתמש בכלים העומדים לרשותך כדי לענות על שאלות לגבי תפריט וזמינות מנות."""

chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=[get_menu, check_availability]
    )
)

print("פסטה בנגב — בוט הזמנות 🍝  (הקלד 'יציאה' לסיום)\n")

while True:
    user_input = input("לקוח: ").strip()
    if not user_input:
        continue
    if user_input == "יציאה":
        break

    response = chat.send_message(user_input)
    print(f"בוט: {response.text}\n")
