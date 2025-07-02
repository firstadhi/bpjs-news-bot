import sqlite3
import config
from datetime import datetime, timedelta
import calendar

def get_connection():
    return sqlite3.connect(config.DATABASE)

def create_tables():
    with get_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY,
                title TEXT,
                url TEXT,
                published_at TEXT
            )
        ''')

def save_news(title, url, published_at):
    with get_connection() as conn:
        conn.execute("INSERT INTO news (title, url, published_at) VALUES (?, ?, ?)",
                     (title, url, published_at))
        conn.commit()

def is_news_sent(title):
    with get_connection() as conn:
        cursor = conn.execute("SELECT id FROM news WHERE title = ?", (title,))
        return cursor.fetchone() is not None

def get_news_by_date(date):
    with get_connection() as conn:
        return conn.execute("SELECT * FROM news WHERE date(published_at) = ?", (date.isoformat(),)).fetchall()

def get_news_last_week():
    today = datetime.today().date()
    week_ago = today - timedelta(days=7)
    with get_connection() as conn:
        return conn.execute("SELECT * FROM news WHERE date(published_at) BETWEEN ? AND ?",
                            (week_ago.isoformat(), today.isoformat())).fetchall()

def get_news_by_month(month_name, year):
    month = list(calendar.month_name).index(month_name.capitalize())
    start = datetime(year, month, 1).date()
    end_day = calendar.monthrange(year, month)[1]
    end = datetime(year, month, end_day).date()
    with get_connection() as conn:
        return conn.execute("SELECT * FROM news WHERE date(published_at) BETWEEN ? AND ?",
                            (start.isoformat(), end.isoformat())).fetchall()

create_tables()
