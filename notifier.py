from scraper_google import search_bpjs_news

def handle_google_search(update, context):
    articles = search_bpjs_news()
    if not articles:
        update.message.reply_text("Tidak ditemukan berita terbaru.")
        return

    for article in articles:
        text = f"📰 {article['title']}\n{article['url']}\n\n{article['content'][:300]}..."
        update.message.reply_text(text)
