import requests
from config import GOOGLE_CSE_API_KEY, GOOGLE_CSE_CX
from bs4 import BeautifulSoup

def google_search(query, max_results=5):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_CSE_API_KEY,
        "cx": GOOGLE_CSE_CX,
        "q": query,
        "num": max_results,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def extract_article_text(url):
    try:
        page = requests.get(url, timeout=10)
        soup = BeautifulSoup(page.content, "html.parser")
        paragraphs = soup.find_all('p')
        text = " ".join([p.get_text() for p in paragraphs])
        return text.strip()
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

def search_bpjs_news():
    results = google_search("BPJS Ketenagakerjaan site:.go.id OR site:.com")
    news = []
    for item in results.get("items", []):
        title = item["title"]
        link = item["link"]
        snippet = extract_article_text(link)[:500]  # ambil 500 karakter pertama
        news.append({
            "title": title,
            "url": link,
            "content": snippet
        })
    return news
