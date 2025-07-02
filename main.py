from flask import Flask, request
import config
from database import get_news_by_date, get_news_last_week, get_news_by_month
from scraper import scrape_news
from notifier import send_message
import datetime

app = Flask(__name__)

@app.route(f"/{config.TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()
    message = update.get("message", {})
    text = message.get("text", "").lower()

    if text == "/today":
        today = datetime.date.today()
        news = get_news_by_date(today)
        if news:
            reply = "<b>Berita Hari Ini:</b>\n\n" + "\n\n".join([f"📰 {n[1]}\n{n[2]}" for n in news])
        else:
            reply = "Tidak ada berita hari ini."
    elif text == "/week":
        news = get_news_last_week()
        if news:
            reply = "<b>Berita 1 Minggu Terakhir:</b>\n\n" + "\n\n".join([f"📰 {n[1]}\n{n[2]}" for n in news])
        else:
            reply = "Tidak ada berita 1 minggu terakhir."
    elif text.startswith("/bulan "):
        try:
            parts = text.replace("/bulan ", "").split()
            if len(parts) != 2:
                raise ValueError
            month, year = parts
            news = get_news_by_month(month, int(year))
            if news:
                reply = f"<b>Berita Bulan {month} {year}:</b>\n\n" + "\n\n".join([f"📰 {n[1]}\n{n[2]}" for n in news])
            else:
                reply = f"Tidak ada berita pada bulan {month} {year}."
        except:
            reply = "Format salah. Gunakan: /bulan Juli 2025"
    elif text == "/refresh":
        print("📥 Bot menerima perintah /refresh")
        send_message("🔄 Memproses update berita terbaru...")
        scrape_news()
        print("✅ Selesai scraping semua sumber")
        return "ok"
    else:
        reply = (
            "Perintah tidak dikenali.\n"
            "Gunakan salah satu:\n"
            "/today - Berita hari ini\n"
            "/week - Berita 1 minggu terakhir\n"
            "/bulan <Bulan Tahun> - Berita bulanan\n"
            "/refresh - Ambil berita terbaru"
        )

    send_message(reply)
    return "ok"

@app.route("/")
def index():
    return "✅ Bot aktif dan berjalan dengan webhook."

from apscheduler.schedulers.background import BackgroundScheduler
from scraper import scrape_news

scheduler = BackgroundScheduler()
scheduler.add_job(scrape_news, 'interval', minutes=10)  # tiap 10 menit
scheduler.start()


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
