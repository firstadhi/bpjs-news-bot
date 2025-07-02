import requests
from notifier import send_message
from database import save_news, is_news_sent
import config

def scrape_newsapi():
    api_key = config.NEWSAPI_KEY
    query = config.NEWS_KEYWORD
    url = (f"https://newsapi.org/v2/everything?q={query}&language=id"
           f"&sortBy=publishedAt&pageSize=10&apiKey={api_key}")
    response = requests.get(url)
    data = response.json()
    for article in data.get("articles", []):
        title = article["title"]
        link = article["url"]
        published = article["publishedAt"]
        if not is_news_sent(title):
            save_news(title, link, published)
            send_message(f"📰 {title}\n{link}")
