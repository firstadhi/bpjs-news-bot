import requests
import os

def search_bpjs_news():
    api_key = os.getenv("GOOGLE_API_KEY")
    cx = os.getenv("GOOGLE_CSE_ID")  # contoh: "40c862fcde8f54d7d"
    query = "BPJS Ketenagakerjaan"
    
    url = (
        f"https://www.googleapis.com/customsearch/v1"
        f"?q={query}&cx={cx}&key={api_key}"
        f"&dateRestrict=d2&sort=date"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()  # 🚨 Penting untuk deteksi error HTTP
        data = response.json()
    except Exception as e:
        print(f"[ERROR] Gagal fetch dari Google CSE: {e}")
        return []

    results = []
    for item in data.get("items", []):
        results.append({
            "title": item["title"],
            "url": item["link"],
            "content": item.get("snippet", ""),
            "published": None  # ⚠️ Tidak bisa tebak tanggal dari snippet, jadi biarkan kosong
        })

    print(f"[DEBUG] Google CSE return {len(results)} berita")
    return results
