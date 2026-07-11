import requests
from bs4 import BeautifulSoup

from app.utils import extract_emails, extract_phones

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}


def fetch_page(url: str) -> dict:
    result = {"url": url, "title": "", "description": "", "emails": [], "phones": []}

    try:
        response = requests.get(url, headers=HEADERS, timeout=6)

        if response.status_code != 200:
            return result

        soup = BeautifulSoup(response.text, "lxml")

        if soup.title and soup.title.string:
            result["title"] = soup.title.string.strip()

        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            result["description"] = meta_desc["content"].strip()

        page_text = soup.get_text(" ", strip=True)[:5000]
        result["emails"] = extract_emails(page_text)
        result["phones"] = extract_phones(page_text)

    except Exception as exc:
        print(f"Could not fetch {url}: {exc}")

    return result