import os
import json
db_file = "news_db.json"

def save_news(title, link, published):
    data = load_news()
    data[title] = {"link": link, "published": published}
    with open(db_file, "w") as f:
        json.dump(data, f)

def is_news_sent(title):
    data = load_news()
    return title in data

def load_news():
    if not os.path.exists(db_file):
        return {}
    with open(db_file, "r") as f:
        return json.load(f)
