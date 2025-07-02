from scraper_newsapi import scrape_newsapi
from scraper_google import search_bpjs_news
from database import save_news, is_news_sent
from notifier import send_message
from datetime import datetime
import config

def scrape_news():
    print("⏳ Mulai scrape dari NewsAPI...")
    scrape_newsapi()
    print("✅ Selesai scrape NewsAPI, lanjut ke Google CSE...")

    try:
        results = search_bpjs_news()
        print(f"📄 Google CSE menemukan {len(results)} hasil.")

        if not results:
            print("[INFO] Tidak ada hasil dari Google CSE.")
            return

        for r in results:
            title = r["title"]
            url = r["url"]
            content = r["content"]
            published = r.get("published", datetime.utcnow().isoformat())

            print(f"[DEBUG] Cek judul: {title}")
            if not is_news_sent(title):
                print(f"[NEW] Google CSE: {title}")
                save_news(title, url, published)
                send_message(f"📰 {title}\n{url}", chat_id=config.CHAT_ID)
            else:
                print(f"[SKIP] Sudah dikirim sebelumnya: {title}")

    except Exception as e:
        print(f"[ERROR] Google CSE gagal: {e}")
