import requests
import config
import datetime
from database import get_news_by_date, get_news_last_week, get_news_by_month

def send_message(text):
    url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": config.CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload)

def handle_update(update):
    message = update.get("message", {})
    text = message.get("text", "").lower()

    if text == "/today":
        today = datetime.date.today()
        news = get_news_by_date(today)
        reply = format_news_list(news, "Hari Ini")
    elif text == "/week":
        news = get_news_last_week()
        reply = format_news_list(news, "1 Minggu Terakhir")
    elif text.startswith("/bulan "):
        try:
            month_year = text.replace("/bulan ", "")
            month, year = month_year.split()
            news = get_news_by_month(month, int(year))
            reply = format_news_list(news, f"Bulan {month} {year}")
        except:
            reply = "Format salah. Gunakan: /bulan Juli 2025"
    else:
        reply = "Perintah tidak dikenal. Gunakan: /today, /week, /bulan <bulan tahun>"

    send_message(reply)

def format_news_list(news, title):
    if not news:
        return f"Tidak ada berita untuk {title}"
    return f"<b>Berita {title}:</b>\n\n" + "\n\n".join([f"📰 {n[1]}\n{n[2]}" for n in news])
