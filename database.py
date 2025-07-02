import os
import json
from config import DATABASE
from datetime import datetime, timedelta

db_file = DATABASE

def load_news():
    if not os.path.exists(db_file):
        return {}
    with open(db_file, "r") as f:
        return json.load(f)

def save_news(title, url, published):
    data = load_news()
    data[title] = {"url": url, "published": published}
    with open(db_file, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[DB] Saved: {title}")

def is_news_sent(title):
    data = load_news()
    return title in data

def get_news_by_date(date):
    data = load_news()
    return [(datetime.fromisoformat(v["published"]), t, v["url"])
            for t, v in data.items()
            if datetime.fromisoformat(v["published"]).date() == date]

def get_news_last_week():
    today = datetime.utcnow().date()
    one_week_ago = today - timedelta(days=7)
    data = load_news()
    return [(datetime.fromisoformat(v["published"]), t, v["url"])
            for t, v in data.items()
            if one_week_ago <= datetime.fromisoformat(v["published"]).date() <= today]

def get_news_by_month(month_str, year):
    from calendar import month_name
    month_lookup = {m.lower(): i for i, m in enumerate(month_name) if m}
    month = month_lookup.get(month_str.lower())
    if not month:
        return []
    data = load_news()
    return [(datetime.fromisoformat(v["published"]), t, v["url"])
            for t, v in data.items()
            if datetime.fromisoformat(v["published"]).month == month and datetime.fromisoformat(v["published"]).year == year]
