import telebot
import datetime
import config
from database import get_news_by_date, get_news_last_week, get_news_by_month
from scraper import scrape_news

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    bot.reply_to(message, "Perintah tersedia: /today, /week, /bulan <Juli 2025>, /refresh")

@bot.message_handler(commands=['today'])
def handle_today(message):
    today = datetime.date.today()
    news = get_news_by_date(today)
    reply = format_news_list(news, "Hari Ini")
    bot.send_message(message.chat.id, reply, parse_mode="HTML")

@bot.message_handler(commands=['week'])
def handle_week(message):
    news = get_news_last_week()
    reply = format_news_list(news, "1 Minggu Terakhir")
    bot.send_message(message.chat.id, reply, parse_mode="HTML")

@bot.message_handler(commands=['bulan'])
def handle_bulan(message):
    try:
        args = message.text.split()
        if len(args) != 3:
            raise ValueError
        bulan, tahun = args[1], int(args[2])
        news = get_news_by_month(bulan, tahun)
        reply = format_news_list(news, f"Bulan {bulan} {tahun}")
    except:
        reply = "Format salah. Gunakan: /bulan Juli 2025"
    bot.send_message(message.chat.id, reply, parse_mode="HTML")

@bot.message_handler(commands=['refresh'])
def handle_refresh(message):
    bot.send_message(message.chat.id, "🔄 Memproses berita terbaru...")
    scrape_news()
    bot.send_message(message.chat.id, "✅ Selesai update berita.")

def format_news_list(news, title):
    if not news:
        return f"Tidak ada berita untuk {title}"
    return f"<b>Berita {title}:</b>\n\n" + "\n\n".join([f"📰 {n[1]}\n{n[2]}" for n in news])

if __name__ == "__main__":
    print("Bot Telegram aktif...")
    bot.infinity_polling()
