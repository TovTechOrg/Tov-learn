import hmac
import hashlib
from flask import Flask, request

app = Flask(__name__)

SECRET_KEY = "MySuperSecretKeyForZap"

@app.route('/webhook', methods=['POST'])
def webhook():
    signature = request.headers.get('X-Zap-Signature')
    if not signature:
        return "Unauthorized", 401

    body = request.data
    expected_signature = hmac.new(SECRET_KEY.encode(), body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected_signature):
        return "Unauthorized", 401

    data = request.get_json()
    print("=========================")
    print("🔔 ליד חדש התקבל מדפי זהב! 🔔")
    print("שם מלא:", data['customer_details']['full_name'])
    print("טלפון:", data['customer_details']['phone'])
    print("הודעה:", data['message'])
    print("=========================")
    return "OK", 200

if __name__ == '__main__':
    app.run(port=5000)
