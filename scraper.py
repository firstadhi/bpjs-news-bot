import feedparser
import datetime
from database import save_news, is_news_sent
from notifier import send_message  # <- perubahan penting
from apscheduler.schedulers.background import BackgroundScheduler
import config

def scrape_news():
    print("🔄 Mulai scraping berita...")
    feed_url = f"https://news.google.com/rss/search?q={config.NEWS_KEYWORD.replace(' ', '%20')}"
    feed = feedparser.parse(feed_url)
    found = False
    for entry in feed.entries[:10]:
        title = entry.title
        url = entry.link
        published_at = datetime.datetime(*entry.published_parsed[:6]).isoformat()
        if not is_news_sent(title):
            save_news(title, url, published_at)
            send_message(f"📰 {title}\n{url}")
            print(f"📬 Kirim berita: {title}")
            found = True
    if not found:
        print("📭 Tidak ada berita baru.")

def schedule_scraping():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scrape_news, 'interval', minutes=30)
    scheduler.start()
