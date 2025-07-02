import requests
import config
from database import save_news, is_news_sent

def send_message(text: str):
    url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": config.CHAT_ID,  # ← pastikan variabelnya adalah CHAT_ID
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message: {e}")
    return response

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
