import requests
import os

def search_bpjs_news():
    api_key = os.getenv("GOOGLE_API_KEY")
    cx = os.getenv("GOOGLE_CSE_ID")  # contoh: "40c862fcde8f54d7d"
    query = "BPJS Ketenagakerjaan"
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={cx}&key={api_key}&dateRestrict=d2&sort=date"

    response = requests.get(url)
    data = response.json()

    results = []
    for item in data.get("items", []):
        results.append({
            "title": item["title"],
            "url": item["link"],
            "content": item.get("snippet", ""),
            "published": item.get("snippet", "")[:10]  # optional, jika tersedia tanggal di snippet
        })

    return results
