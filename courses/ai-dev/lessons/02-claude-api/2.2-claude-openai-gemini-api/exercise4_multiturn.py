import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

SYSTEM_PROMPT = "אתה עוזר וירטואלי באתר 'מחסני חשמל'. ענה על שאלות לגבי מוצרים, מחירים ומבצעים. היה אדיב ומקצועי."

# יצירת session שיחה — Gemini שומר את ההיסטוריה אוטומטית
chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
)

print("עוזר מחסני חשמל — הקלד 'יציאה' לסיום\n")

while True:
    user_input = input("אתה: ")
    if user_input == "יציאה":
        break

    response = chat.send_message(user_input)
    print(f"בוט: {response.text}\n")

    # הדפסת כמות ההודעות בזיכרון (להמחשה)
    print(f"  [זיכרון: {len(chat.get_history())} הודעות בהיסטוריה]\n")
