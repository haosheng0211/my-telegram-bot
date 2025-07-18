from flask import Flask, request, jsonify
import requests
import os

TOKEN = os.environ.get('BOT_TOKEN')
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    message = data.get('message', {})
    text = (message.get('text') or '').lower()
    chat_id = message.get('chat', {}).get('id')
    user_message_id = message.get('message_id')
    reply_to = message.get('reply_to_message', {})
    reply_to_message_id = reply_to.get('message_id')

    if text == 'd' and chat_id:
        # 刪除被回覆的訊息
        if reply_to_message_id:
            try:
                requests.post(f"{TELEGRAM_API}/deleteMessage", json={
                    "chat_id": chat_id,
                    "message_id": reply_to_message_id
                })
            except Exception as e:
                print(f"Failed to delete replied message: {e}")

        # 刪除用戶自己這則訊息
        try:
            requests.post(f"{TELEGRAM_API}/deleteMessage", json={
                "chat_id": chat_id,
                "message_id": user_message_id
            })
        except Exception as e:
            print(f"Failed to delete user message: {e}")

    return jsonify({"ok": True})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
