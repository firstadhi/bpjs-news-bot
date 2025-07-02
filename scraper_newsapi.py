import requests
from datetime import datetime, timedelta
from config import NEWSAPI_KEY, NEWS_KEYWORD
from database import save_news, is_news_sent
from notifier import send_message

def scrape_newsapi():
    today = datetime.utcnow()
    yesterday = today - timedelta(days=1)

    url = (
        f"https://newsapi.org/v2/everything?q={NEWS_KEYWORD}&language=id"
        f"&from={yesterday.isoformat()}&to={today.isoformat()}"
        f"&sortBy=publishedAt&pageSize=10&apiKey={NEWSAPI_KEY}"
    )

    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        print(f"[ERROR] NewsAPI failed: {e}")
        return

    for article in data.get("articles", []):
        title = article["title"]
        url = article["url"]
        published = article["publishedAt"]

        if not is_news_sent(title):
            print(f"[NEW] NewsAPI: {title}")
            save_news(title, url, published)
            send_message(f"📰 <b>{title}</b>\n{url}")
        else:
            print(f"[SKIP] {title}")
