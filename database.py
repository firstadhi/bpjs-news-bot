import os
import json
from config import DATABASE
db_file = DATABASE

def save_news(title, link, published):
    print(f"[DB] Menyimpan: {title} - {url}")
    data = load_news()
    data[title] = {"link": link, "published": published}
    with open(db_file, "w") as f:
        json.dump(data, f)

def is_news_sent(title, url):
    cursor.execute("SELECT 1 FROM news WHERE title = ? AND url = ?", (title, url))
    return cursor.fetchone() is not None

def load_news():
    if not os.path.exists(db_file):
        return {}
    with open(db_file, "r") as f:
        return json.load(f)

from datetime import datetime, timedelta

def get_news_by_date(date):
    data = load_news()
    result = []
    for title, val in data.items():
        pub_date = datetime.fromisoformat(val["published"]).date()
        if pub_date == date:
            result.append((pub_date, title, val["link"]))
    return sorted(result)

def get_news_last_week():
    today = datetime.today().date()
    last_week = today - timedelta(days=7)
    data = load_news()
    result = []
    for title, val in data.items():
        pub_date = datetime.fromisoformat(val["published"]).date()
        if last_week <= pub_date <= today:
            result.append((pub_date, title, val["link"]))
    return sorted(result)

def get_news_by_month(month_str, year):
    from calendar import month_name
    month_lookup = {m.lower(): i for i, m in enumerate(month_name) if m}
    month = month_lookup.get(month_str.lower())
    if not month:
        return []
    data = load_news()
    result = []
    for title, val in data.items():
        pub_date = datetime.fromisoformat(val["published"])
        if pub_date.month == month and pub_date.year == year:
            result.append((pub_date, title, val["link"]))
    return sorted(result)
