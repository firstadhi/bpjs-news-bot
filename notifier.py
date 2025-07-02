import requests
from config import TELEGRAM_TOKEN, CHAT_ID  # pastikan CHAT_ID dibaca

def send_message(text: str, chat_id=CHAT_ID):  # pakai default dari config
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message: {e}")
        return None
