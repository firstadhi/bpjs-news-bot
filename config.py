import os

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
DATABASE = os.getenv('DATABASE', 'news.db')
NEWS_KEYWORD = os.getenv('NEWS_KEYWORD', 'BPJS Ketenagakerjaan')
NEWS_SITE = f"https://news.google.com/search?q={NEWS_KEYWORD.replace(' ', '%20')}"
NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')
GOOGLE_CSE_API_KEY = os.getenv('GOOGLE_CSE_API_KEY')
GOOGLE_CSE_CX = os.getenv('GOOGLE_CSE_CX')
