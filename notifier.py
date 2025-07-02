import requests
from config import TELEGRAM_TOKEN, CHAT_ID

def send_message(text: str, chat_id=CHAT_ID):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print(f"[SEND] Pesan berhasil dikirim: {text[:60]}...")
        return response
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Gagal mengirim pesan: {e}")
        return None
