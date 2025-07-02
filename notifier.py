from scraper_google import search_bpjs_news

def handle_google_search(update, context):
    articles = search_bpjs_news()
    if not articles:
        update.message.reply_text("Tidak ditemukan berita terbaru.")
        return

    for article in articles:
        text = f"📰 {article['title']}\n{article['url']}\n\n{article['content'][:300]}..."
        update.message.reply_text(text)
def send_message(text: str):
    import requests
    from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=payload)
    return response
