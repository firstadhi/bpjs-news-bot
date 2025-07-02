from dotenv import load_dotenv
import os

# Load dari file .env (di local / render.com environment)
load_dotenv()

# Variabel penting dari lingkungan
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
DATABASE = os.getenv("DATABASE", "news_db.json")
NEWS_KEYWORD = os.getenv("NEWS_KEYWORD", "BPJS Ketenagakerjaan")

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

# Validasi
required = {
    "TELEGRAM_TOKEN": TELEGRAM_TOKEN,
    "CHAT_ID": CHAT_ID,
    "NEWSAPI_KEY": NEWSAPI_KEY,
    "GOOGLE_API_KEY": GOOGLE_API_KEY,
    "GOOGLE_CSE_ID": GOOGLE_CSE_ID,
}

missing = [k for k, v in required.items() if not v]
if missing:
    raise EnvironmentError(f"❌ ENV belum lengkap: {', '.join(missing)}")
