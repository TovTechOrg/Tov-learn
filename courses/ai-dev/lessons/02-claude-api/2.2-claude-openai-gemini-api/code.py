import os
from dotenv import load_dotenv
import openai
import anthropic
from google import genai

# Load API keys from .env file
load_dotenv()

# --- 1. OpenAI Client ---
client_openai = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_openai_response(prompt):
    response = client_openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# --- 2. Anthropic Client ---
client_anthropic = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def get_claude_response(prompt):
    # Your code here: Call Anthropic's API
    # Hint: client_anthropic.messages.create(
    #           model="claude-sonnet-4-6",
    #           max_tokens=1024,                      # שימו לב: max_tokens חובה ב-Claude
    #           messages=[{"role": "user", "content": prompt}])
    #       והטקסט נמצא ב-response.content[0].text
    pass

# --- 3. Gemini Client ---
client_gemini = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def get_gemini_response(prompt):
    response = client_gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text


# --- Main execution ---
main_prompt = "כתוב פוסט קצר וקליט לפייסבוק באורך 3-4 משפטים על תערובת קפה חדשה בשם 'תערובת חיפה'. הדגש את הארומה המיוחדת והטעם העשיר. הפוסט צריך להיות מנוסח בעברית, בסגנון צעיר ומזמין."

print("--- OpenAI Response ---")
# print(get_openai_response(main_prompt))

print("\n--- Claude Response ---")
# print(get_claude_response(main_prompt))

print("\n--- Gemini Response ---")
print(get_gemini_response(main_prompt))