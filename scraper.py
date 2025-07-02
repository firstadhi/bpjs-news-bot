from scraper_newsapi import scrape_newsapi
from scraper_google import search_bpjs_news
from database import save_news, is_news_sent
from notifier import send_message
from datetime import datetime
import config

def scrape_news():
    print("⏳ Mulai scrape dari NewsAPI...")
    scrape_newsapi()

    print("✅ Selesai NewsAPI, lanjut ke Google CSE...")
    try:
        results = search_bpjs_news()
        print(f"[INFO] Google CSE menemukan {len(results)} hasil.")
        for r in results:
            title = r["title"]
            url = r["url"]
            published = r["published"]

            if not is_news_sent(title):
                print(f"[NEW] {title}")
                save_news(title, url, published)
                send_message(f"📰 <b>{title}</b>\n{url}")
            else:
                print(f"[SKIP] {title}")
    except Exception as e:
        print(f"[ERROR] Gagal Google CSE: {e}")
