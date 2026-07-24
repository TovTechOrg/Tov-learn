import hmac, hashlib, json, requests

SECRET_KEY = "MyShufersalSecretKey"
payload = {
    "order_id": 987654,
    "timestamp": "2026-05-10T18:00:00Z",
    "status": "paid_and_ready_for_collection",
    "customer": {"name": "דנה כהן", "phone": "052-7654321"},
    "delivery_address": {"street": "הרצל 15", "city": "גבעתיים", "zip_code": "5344512"},
    "items": [
        {"sku": "729000000001", "name": "חלב 3%", "quantity": 2},
        {"sku": "729000000002", "name": "לחם אחיד", "quantity": 1},
        {"sku": "729000000003", "name": "קוטג' 5%", "quantity": 3}
    ],
    "item_count": 6
}
body = json.dumps(payload, ensure_ascii=False).encode()
signature = hmac.new(SECRET_KEY.encode(), body, hashlib.sha256).hexdigest()

response = requests.post(
    "http://localhost:5000/shufersal-orders",
    data=body,
    headers={"Content-Type": "application/json", "X-Shufersal-Signature": signature}
)
print(response.status_code, response.text)
