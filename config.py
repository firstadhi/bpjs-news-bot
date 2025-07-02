import os
from dotenv import load_dotenv

# Muat .env jika dijalankan secara lokal
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
DATABASE = os.getenv("DATABASE", "news.json")
NEWS_KEYWORD = os.getenv("NEWS_KEYWORD", "BPJS Ketenagakerjaan")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
