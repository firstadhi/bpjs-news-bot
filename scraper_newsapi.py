import requests
import config
from database import save_news, is_news_sent
from notifier import send_message
from datetime import datetime, timedelta

def scrape_newsapi():
    api_key = config.NEWSAPI_KEY
    query = config.NEWS_KEYWORD

    # Hitung waktu 24 jam ke belakang
    today = datetime.utcnow()
    yesterday = today - timedelta(days=1)

    url = (
        f"https://newsapi.org/v2/everything?q={query}&language=id"
        f"&from={yesterday.isoformat()}&to={today.isoformat()}"
        f"&sortBy=publishedAt&pageSize=10&apiKey={api_key}"
    )

response = requests.get(url)
if response.status_code != 200:
    print(f"[ERROR] NewsAPI failed: {response.status_code} {response.text}")
    return

data = response.json()

    for article in data.get("articles", []):
        title = article["title"]
        link = article["url"]
        published = article["publishedAt"]

        if not is_news_sent(title):
            save_news(title, link, published)
            send_message(f"📰 {title}\n{link}")
