import requests
import os

def search_bpjs_news():
    api_key = os.getenv("GOOGLE_API_KEY")
    cx = os.getenv("GOOGLE_CSE_ID")
    query = "BPJS Ketenagakerjaan"

    if not api_key or not cx:
        print("[ERROR] GOOGLE_API_KEY atau GOOGLE_CSE_ID belum diset.")
        return []

    url = (
        f"https://www.googleapis.com/customsearch/v1"
        f"?q={query}&cx={cx}&key={api_key}"
        f"&dateRestrict=d2&sort=date"  # berita 2 hari terakhir dan disortir terbaru
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"[ERROR] Gagal fetch dari Google CSE: {e}")
        return []

    results = []
    for item in data.get("items", []):
        title = item.get("title")
        link = item.get("link")
        snippet = item.get("snippet", "")

        results.append({
            "title": title,
            "url": link,
            "content": snippet,
            "published": snippet[:10]  # opsional, asumsi ada tanggal di awal
        })

    print(f"[INFO] Google CSE mengembalikan {len(results)} hasil.")
    return results
