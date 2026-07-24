import requests
import json

# הגדרת נקודת הקצה והמפתח
api_key = "YOUR_API_KEY_HERE" # <--- החליפו במפתח שלכם מ-aistudio.google.com
api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"

# הגדרת ה-Headers לבקשה (Gemini לא צריך Authorization header)
headers = {
    "Content-Type": "application/json"
}

# הגדרת גוף הבקשה (payload)
payload = {
  "contents": [
    {
      "parts": [
        {
          "text": "מהם 3 היתרונות המרכזיים של שימוש ב-API בעולם העסקי?"
        }
      ]
    }
  ]
}

# שליחת בקשת POST
response = requests.post(api_url, headers=headers, data=json.dumps(payload))

# בדיקת תקינות התשובה והדפסתה
if response.status_code == 200:
    response_data = response.json()
    # הדפסת התוכן של התשובה הראשונה מהמודל
    print(response_data['candidates'][0]['content']['parts'][0]['text'])
else:
    print(f"Error: {response.status_code}")
    print(response.text)
