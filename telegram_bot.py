from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from database import get_news_by_date, get_news_last_week, get_news_by_month
from scraper import scrape_news
import datetime
import config

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.date.today()
    news = get_news_by_date(today)
    reply = format_news_list(news, "Hari Ini")
    await update.message.reply_text(reply, parse_mode="HTML")

async def week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    news = get_news_last_week()
    reply = format_news_list(news, "1 Minggu Terakhir")
    await update.message.reply_text(reply, parse_mode="HTML")

async def bulan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        month, year = context.args
        news = get_news_by_month(month, int(year))
        reply = format_news_list(news, f"Bulan {month} {year}")
    except:
        reply = "Format salah. Gunakan: /bulan Juli 2025"
    await update.message.reply_text(reply, parse_mode="HTML")

async def refresh(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Memproses berita terbaru...")
    scrape_news()
    await update.message.reply_text("✅ Update selesai.")

def format_news_list(news, title):
    if not news:
        return f"Tidak ada berita untuk {title}"
    return f"<b>Berita {title}:</b>\n\n" + "\n\n".join([f"📰 {n[1]}\n{n[2]}" for n in news])

def run_bot():
    app = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("today", today))
    app.add_handler(CommandHandler("week", week))
    app.add_handler(CommandHandler("bulan", bulan))
    app.add_handler(CommandHandler("refresh", refresh))
    app.run_polling()

if __name__ == "__main__":
    run_bot()
