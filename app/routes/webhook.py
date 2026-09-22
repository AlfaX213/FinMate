import requests
from flask import Blueprint, request, jsonify

webhook_bp = Blueprint("webhook", __name__)

WAHA_URL = "http://localhost:3000"
WAHA_API_KEY = "finmate123"

def send_message(chat_id, text):
    url = "http://127.0.0.1:3000/api/sendText"

    payload = {
        "session": "finmate",
        "chatId": chat_id,
        "text": text
    }

    headers = {
        "X-Api-Key": "finmate123"
    }

    response = requests.post(url, json=payload, headers=headers)

    print("WAHA response:", response.status_code, response.text)

@webhook_bp.route("/waha", methods=["GET", "POST"])
def receive_webhook():
    if request.method == "GET":
        return jsonify({"status": "ok"}), 200

    data = request.get_json(silent=True)

    if not data:
        print("EMPTY PAYLOAD")
        print("RAW DATA:", request.data)
        return jsonify({"status": "ignored"}), 200

    print("Incoming webhook data:", data)

    try:
        payload = data.get("payload", {})

        chat_id = payload.get("from")
        message = payload.get("body")

        if not chat_id or not message:
            print("Missing chat_id or message")
            return jsonify({"status": "ignored"}), 200

        reply = f"FinMate received: {message}"
        send_message(chat_id, reply)

    except Exception as e:
        print("ERROR:", e)

    return jsonify({"status": "received"}), 200