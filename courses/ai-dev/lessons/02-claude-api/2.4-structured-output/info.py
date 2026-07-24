import json

# ── תרגיל 1 — חילוץ מידע מ-JSON string ──────────────────────────────────────
raw_payload = '{"event": "message_received", "from": "972501234567", "message": {"text": "שלום, אני מעוניין במוצר", "timestamp": 1751400000}, "contact": {"name": "דוד כהן", "is_new": true}}'

data = json.loads(raw_payload)

print("Full Name:", data['contact']['name'])
print("message:", data['message']['text'])

# ── תרגיל 2 — כתיבה לקובץ עם עברית תקינה ────────────────────────────────────
product = {"שם": "במבה", "מחיר": 2.90, "תיאור": "חטיף בוטנים קלאסי"}

with open("product.json", "w", encoding="utf-8") as f:
    json.dump(product, f, indent=4, ensure_ascii=False)

print("\nתוכן הקובץ שנשמר:")
print(json.dumps(product, indent=4, ensure_ascii=False))

# ── תרגיל 3 — Webhook תשלום אמיתי ────────────────────────────────────



webhook_str = '{"event_type": "transaction.succeeded", "data": {"transaction_id": "tr_a8b2c1d3", "amount": 249.90, "currency": "ILS", "payment_details": {"card_type": "Visa", "last_4_digits": "4242"}}}'

def process_payment(payload_str):
    data = json.loads(payload_str)
    if data['event_type'] == 'transaction.succeeded':
        transaction_id = data['data']['transaction_id']
        amount = data['data']['amount']
        currency = data['data']['currency']
        card_type = data['data']['payment_details']['card_type']
        last_4_digits = data['data']['payment_details']['last_4_digits']

        print(f"Transaction ID: {transaction_id}")
        print(f"Amount: {amount} {currency}")
        print(f"Card Type: {card_type}")
        print(f"Last 4 Digits: {last_4_digits}")
    else:
        print("Unhandled event type:", data['event_type'])

process_payment(webhook_str)


# תרגיל 6 — Pydantic Validation
from pydantic import BaseModel, ValidationError
from typing import List
import json

llm_messy_response = """
{
  "recommendations": [
    {"name": "האחים", "cuisine": "ישראלי", "rating": 4.5},
    {"name": "טאיזו", "cuisine": "אסייאתי", "rating": "4.8"},
    {"name": "פורט סעיד", "cuisine": "ים תיכוני", "rating": 4}
  ]
}
"""
# 1. הגדירו את המודלים של Pydantic
class Restaurant(BaseModel):
    name: str
    cuisine: str
    rating: float


class Response(BaseModel):
    recommendations: List[Restaurant]


# 2. פענחו את ה-JSON וצרו אובייקט Pydantic
try:
    data = json.loads(llm_messy_response)
    # Your code here: צרו אובייקט RecommendationsResponse מה-data
    result = Response(**data)
    
    # 3. אם הוולידציה הצליחה, הדפיסו את המידע
    print(type(result.recommendations[1].rating))
    print(result.recommendations[1].rating)

    
except ValidationError as e:
    print("שגיאת ולידציה:", e)