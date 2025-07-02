from scraper_newsapi import scrape_newsapi
from scraper_google import search_bpjs_news
from database import save_news, is_news_sent
from notifier import send_message
from datetime import datetime

def scrape_news():
    scrape_newsapi()

    # 🔁 Ambil dari Google CSE juga
    try:
        results = google_search("BPJS Ketenagakerjaan site:.go.id OR site:.com OR site:.id OR site:.co.id")
        for r in results:
            title = r["title"]
            url = r["url"]
            content = r["content"]
            published = datetime.utcnow().date().isoformat()

            if not is_news_sent(title):
                print(f"[NEW] Google CSE: {title}")  # log berita baru
                save_news(title, url, published)
                send_message(f"📰 {title}\n{url}", chat_id=config.CHAT_ID)
    except Exception as e:
        print(f"[ERROR] Google CSE failed: {e}")
