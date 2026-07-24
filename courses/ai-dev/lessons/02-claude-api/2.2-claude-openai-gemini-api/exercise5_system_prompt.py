import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def get_styled_response(system_prompt, user_prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
        config=types.GenerateContentConfig(system_instruction=system_prompt)
    )
    return response.text

professional_prompt = "אתה נציג שירות טכני בכיר בחברת פלאפון. עליך לספק תשובות מדויקות, רשמיות ומפורטות. השתמש בטרמינולוגיה טכנית והימנע מסלנג או אימוג'ים."
friendly_prompt = "אתה 'פלאפי', העוזר הדיגיטלי והחברותי של פלאפון! דבר עם הלקוחות כמו חבר, בגובה העיניים. השתמש בסגנון קליל, הומור, ואל תהסס להוסיף אימוג'ים! 😎"

user_query = "האינטרנט הסלולרי שלי ממש איטי היום, מה אני יכול לעשות?"

print("--- תגובה מקצועית ---")
print(get_styled_response(professional_prompt, user_query))

print("\n--- תגובה חברותית ---")
print(get_styled_response(friendly_prompt, user_query))
