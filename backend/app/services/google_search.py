import time
from ddgs import DDGS


def search_google(query: str, num_results: int = 6) -> list[dict]:
    """Har result ab ek dictionary hai: url, title, snippet.
    Isse humein social/review links ke liye alag se website fetch
    nahi karni padti — search engine khud hi title/description de deta hai."""
    results = []
    try:
        with DDGS() as ddgs:
            raw_results = ddgs.text(query, max_results=num_results)
            for r in raw_results:
                if "href" in r:
                    results.append({
                        "url": r["href"],
                        "title": r.get("title", ""),
                        "snippet": r.get("body", ""),
                    })
    except Exception as exc:
        print(f"Search failed for query '{query}': {exc}")

    time.sleep(0.3)
    return results