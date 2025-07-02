from flask import Flask, request
import config
from database import get_news_by_date, get_news_last_week, get_news_by_month
from scraper import scrape_news
from notifier import send_message
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import os

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
            reply = "<b>Berita Hari Ini:</b>\n\n" + "\n\n".join([f"📰 <b>{n[1]}</b>\n{n[2]}" for n in news])
        else:
            reply = "Tidak ada berita hari ini."

    elif text == "/week":
        news = get_news_last_week()
        if news:
            reply = "<b>Berita 1 Minggu Terakhir:</b>\n\n" + "\n\n".join([f"📰 <b>{n[1]}</b>\n{n[2]}" for n in news])
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
                reply = f"<b>Berita Bulan {month} {year}:</b>\n\n" + "\n\n".join([f"📰 <b>{n[1]}</b>\n{n[2]}" for n in news])
            else:
                reply = f"Tidak ada berita pada bulan {month} {year}."
        except:
            reply = "Format salah. Gunakan: /bulan Juli 2025"

    elif text == "/refresh":
        send_message("🔄 Memproses update berita terbaru...", chat_id=message.get("chat", {}).get("id"))
        try:
            scrape_news()
            send_message("✅ Berita terbaru berhasil diambil.", chat_id=message.get("chat", {}).get("id"))
        except Exception as e:
            send_message(f"⚠️ Gagal mengambil berita: {e}", chat_id=message.get("chat", {}).get("id"))
        return "ok"

    else:
        reply = (
            "Perintah tidak dikenali.\n\n"
            "Gunakan salah satu perintah:\n"
            "📆 /today – Berita hari ini\n"
            "📅 /week – Berita 1 minggu terakhir\n"
            "🗓️ /bulan <Bulan Tahun> – Berita bulanan (cth: /bulan Juli 2025)\n"
            "♻️ /refresh – Ambil berita terbaru sekarang"
        )

    send_message(reply, chat_id=message.get("chat", {}).get("id"))
    return "ok"


@app.route("/")
def index():
    return "✅ Bot aktif dan berjalan dengan webhook."

@app.route("/refresh", methods=["GET"])
def refresh_manual():
    try:
        scrape_news()
        return "🔄 Proses scraping manual selesai", 200
    except Exception as e:
        return f"❌ Gagal: {e}", 500


# === Scheduler: otomatis scraping tiap 10 menit ===
scheduler = BackgroundScheduler()
scheduler.add_job(scrape_news, 'interval', minutes=10)
scheduler.start()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
