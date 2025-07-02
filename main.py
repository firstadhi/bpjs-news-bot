from flask import Flask, request
import config
import datetime
from database import get_news_by_date, get_news_last_week, get_news_by_month
from scraper import scrape_news
from notifier import send_message

app = Flask(__name__)

def format_news_list(news, title):
    if not news:
        return f"Tidak ada berita untuk {title}"
    return f"<b>Berita {title}:</b>\n\n" + "\n\n".join([f"📰 {n[1]}\n{n[2]}" for n in news])

@app.route(f"/{config.TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()
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
    elif text == "/refresh":
        send_message("🔄 Sedang memproses update berita terbaru...")
        scrape_news()
        return "ok"
    else:
        reply = "Perintah tidak dikenal. Gunakan: /today, /week, /bulan <bulan tahun>, /refresh"

    send_message(reply)
    return "ok"

@app.route("/")
def index():
    return "✅ Bot is running with webhook."

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
