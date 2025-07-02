import requests
import os
from datetime import datetime

def search_bpjs_news():
    api_key = os.getenv("GOOGLE_API_KEY")
    cx = os.getenv("GOOGLE_CSE_ID")
    query = "BPJS Ketenagakerjaan"
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={cx}&key={api_key}&sort=date"

    try:
        response = requests.get(url)
        data = response.json()
        items = data.get("items", [])
    except Exception as e:
        print(f"[ERROR] Google CSE failed: {e}")
        return []

    results = []
    for item in items:
        results.append({
            "title": item["title"],
            "url": item["link"],
            "content": item.get("snippet", ""),
            "published": datetime.utcnow().isoformat()  # fallback
        })

    return results
