import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def chat_with_streaming(user_input):
    response = client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=user_input
    )
    for chunk in response:
        print(chunk.text, end='', flush=True)
    print()

print("צ'אטבוט Gemini עם Streaming — הקלד 'יציאה' לסיום\n")

while True:
    user_input = input("אתה: ")
    if user_input == "יציאה":
        break
    print("Gemini: ", end='')
    chat_with_streaming(user_input)
    print()
