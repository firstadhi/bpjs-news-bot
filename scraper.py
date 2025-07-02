import requests
from bs4 import BeautifulSoup
from database import save_news, is_news_sent
from telegram_bot import send_message
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import config

def scrape_news():
    try:
        response = requests.get(config.NEWS_SITE)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.select('article h3 a')

        for a in articles[:10]:
            title = a.text.strip()
            url = 'https://news.google.com' + a['href'][1:]
            published_at = datetime.datetime.now().isoformat()
            if not is_news_sent(title):
                save_news(title, url, published_at)
                send_message(f"📰 {title}\n{url}")
    except Exception as e:
        print(f"Scraping failed: {e}")

def schedule_scraping():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scrape_news, 'interval', minutes=30)
    scheduler.start()
