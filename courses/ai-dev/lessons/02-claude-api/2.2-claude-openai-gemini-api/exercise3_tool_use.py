import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 1. הפונקציה האמיתית — קוד Python רגיל
def calculate_final_price(base_price: float) -> float:
    """מחשב מחיר סופי כולל מע"מ של 17 אחוז.

    Args:
        base_price: המחיר המקורי לפני מע"מ בשקלים.
    """
    result = round(base_price * 1.17, 2)
    print(f"  [Tool Executed] {base_price}₪ + מע\"מ = {result}₪")
    return result

# 2. שולחים את הפונקציה כ-tool — Gemini מחליט מתי לקרוא לה
user_prompt = "אני רוצה לקנות אוזניות שעולות 350 שקלים. כמה זה יצא לי סך הכל?"
print(f"משתמש: {user_prompt}\n")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=user_prompt,
    config=types.GenerateContentConfig(tools=[calculate_final_price])
)

print(f"Gemini: {response.text}")
