import hmac
import hashlib
from datetime import datetime
from flask import Flask, request

app = Flask(__name__)

SECRET_KEY = "MyShufersalSecretKey"

@app.route('/shufersal-orders', methods=['POST'])
def shufersal_orders():
    signature = request.headers.get('X-Shufersal-Signature')
    if not signature:
        return "Unauthorized", 401

    body = request.data
    expected_signature = hmac.new(SECRET_KEY.encode(), body, hashlib.sha256).hexdigest()
    print("RECEIVED :", signature)
    print("EXPECTED :", expected_signature)
    print("BODY     :", body[:100])
    if not hmac.compare_digest(signature, expected_signature):
        return "Unauthorized", 401

    data = request.get_json()

    if data.get('status') != 'paid_and_ready_for_collection':
        return "OK", 200

    order_id = data['order_id']
    customer_name = data['customer']['name']
    city = data['delivery_address']['city']
    item_count = data['item_count']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    log_line = f"[{timestamp}] - New Task: Order #{order_id} for {customer_name} to {city}. Items: {item_count}.\n"

    with open('delivery_tasks.log', 'a', encoding='utf-8') as f:
        f.write(log_line)

    print(log_line.strip())
    return "OK", 200

if __name__ == '__main__':
    app.run(port=5000)