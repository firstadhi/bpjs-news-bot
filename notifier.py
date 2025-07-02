import requests
import config

def send_message(message):
    url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"
    payload = {
    "chat_id": config.CHAT_ID,
    "text": message,
    "parse_mode": "HTML"
}

    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Failed to send message:", e)
