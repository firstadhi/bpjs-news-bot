import datetime
from database import get_news_by_date, get_news_last_week, get_news_by_month
from scraper import scrape_news
from notifier import send_message

def handle_update(update, context):
    message = update.message
    if not message:
        return

    text = message.text.lower()

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
        send_message(chat_id=update.effective_chat.id, text="🔄 Memproses update berita terbaru...")
        scrape_news()
        return
    else:
        reply = "Perintah tidak dikenal. Gunakan: /today, /week, /bulan <bulan tahun>, /refresh"

    # 🛠️ Perbaikan disini:
    send_message(chat_id=update.effective_chat.id, text=reply)

def format_news_list(news, title):
    if not news:
        return f"Tidak ada berita untuk {title}"
    return f"<b>Berita {title}:</b>\n
