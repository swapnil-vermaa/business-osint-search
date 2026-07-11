import time
from ddgs import DDGS


def search_google(query: str, num_results: int = 5) -> list[str]:
    urls: list[str] = []
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=num_results)
            for result in results:
                if "href" in result:
                    urls.append(result["href"])

    except Exception as exc:
        print(f"Search failed for query '{query}': {exc}")

    time.sleep(1)
    return urls