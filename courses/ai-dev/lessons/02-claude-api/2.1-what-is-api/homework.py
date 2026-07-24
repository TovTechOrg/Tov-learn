import requests
import json

api_key = "YOUR_API_KEY_HERE" # <--- החליפו במפתח שלכם מ-aistudio.google.com
# api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={api_key}"



def generate_marketing_description(product_info: str) -> str:
    prompt = f"""כתוב תיאור שיווקי של בדיוק 100 מילים עבור המוצר הבא.
התיאור חייב לכלול:
1. שלושה יתרונות מרכזיים ללקוח
2. שפה ברורה, מושכת ומקצועית
3. קריאה לפעולה ברורה בסוף

מוצר: {product_info}"""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(api_url, headers={"Content-Type": "application/json"}, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"שגיאה: {response.status_code} - {response.text}"


if __name__ == "__main__":
    my_product = (
        "אפליקציית מובייל ישראלית חדשה לניהול תקציב אישי. "
        "האפליקציה מתממשקת אוטומטית לחשבונות בנק וכרטיסי אשראי, "
        "מזהה הוצאות חריגות באמצעות AI, ומציעה טיפים לחיסכון."
    )

    description = generate_marketing_description(my_product)
    print(description)
