from app.services.query_builder import build_queries
from app.services.google_search import search_google
from app.services.extractor import fetch_page
from app.utils import (
    get_domain, is_social, is_review_site,
    get_path_length, is_probably_not_business_site,
    extract_sector_number, extract_all_sector_numbers,
    detect_business_type,
)

MAX_BUSINESS_CANDIDATES_TO_FETCH = 6


def _get_business_keywords(business_name: str) -> list[str]:
    stopwords = {"the", "and", "of", "a", "an"}
    words = business_name.strip().lower().split()
    return [w for w in words if w not in stopwords and len(w) > 2]


def _is_relevant(url: str, title: str, description: str, keywords: list[str], target_sector) -> bool:
    """Ab ye function HAR result type (social, review, search) pe lagta hai —
    taaki koi bhi generic/unrelated page kisi bhi section mein na dikhe."""
    domain = get_domain(url)
    text = f"{domain} {title} {description}".lower()

    if target_sector is not None:
        mentioned_sectors = extract_all_sector_numbers(text)
        if mentioned_sectors and target_sector not in mentioned_sectors:
            return False

    if not keywords:
        return True

    return any(keyword in text for keyword in keywords)


def _build_ai_summary(business_name, business_type, location, social_media, business_website) -> str:
    parts = []

    type_label = business_type.lower() if business_type else "business"
    parts.append(f"{business_name} appears to be a {type_label} located in {location}.")

    if social_media:
        platforms = sorted(set(s["platform"] for s in social_media))
        parts.append(f"Active public presence was found on {', '.join(platforms)}.")

    if business_website:
        parts.append("An official website was identified among public search results.")

    if len(parts) == 1:
        parts.append("Limited additional public information was found for this business.")

    return " ".join(parts)


def run_osint_search(business_name: str, location: str, address: str = None) -> dict:
    queries = build_queries(business_name, location, address)

    all_results = []
    for query in queries:
        all_results.extend(search_google(query))

    seen_urls = set()
    unique_results = []
    for item in all_results:
        if item["url"] not in seen_urls:
            seen_urls.add(item["url"])
            unique_results.append(item)

    keywords = _get_business_keywords(business_name)
    target_sector = extract_sector_number(location) or (
        extract_sector_number(address) if address else None
    )

    # Sabse pehle: HAR result (chahe wo social ho, review ho, ya normal)
    # relevance check se guzarna zaroori hai
    filtered_results = [
        item for item in unique_results
        if _is_relevant(item["url"], item["title"], item["snippet"], keywords, target_sector)
    ]

    # Agar filter itna strict ho gaya ki kuch bacha hi nahi (bahut generic
    # business name ke case mein), toh safety net ke roop mein sab dikha do
    if not filtered_results:
        filtered_results = unique_results

    social_seen = set()
    social_media = []
    reviews = []
    other_results = []

    for item in filtered_results:
        url = item["url"]
        domain = get_domain(url)
        platform = is_social(domain)
        review_source = is_review_site(domain)

        if platform:
            base_url = url.split("?")[0]
            if base_url in social_seen:
                continue
            social_seen.add(base_url)
            social_media.append({
                "platform": platform,
                "url": url,
                "title": item["title"] or url,
            })
        elif review_source:
            reviews.append({
                "source": review_source,
                "url": url,
                "snippet": item["snippet"],
            })
        else:
            other_results.append({
                "url": url,
                "domain": domain,
                "title": item["title"] or url,
                "description": item["snippet"],
                "path_length": get_path_length(url),
            })

    search_results = [
        {"title": r["title"], "url": r["url"], "description": r["description"]}
        for r in other_results
    ]

    keyword_matches = [r for r in other_results if any(k in r["domain"] for k in keywords)]
    fallback_matches = [
        r for r in other_results
        if r not in keyword_matches and not is_probably_not_business_site(r["domain"])
    ]

    candidates = (
        sorted(keyword_matches, key=lambda x: x["path_length"])
        + sorted(fallback_matches, key=lambda x: x["path_length"])
    )

    business_website = None
    business_email = None
    business_phone = None

    for candidate in candidates[:MAX_BUSINESS_CANDIDATES_TO_FETCH]:
        page_data = fetch_page(candidate["url"])

        if business_website is None:
            business_website = candidate["url"]

        if business_email is None and page_data["emails"]:
            business_email = page_data["emails"][0]

        if business_phone is None and page_data["phones"]:
            business_phone = page_data["phones"][0]

        if business_email and business_phone:
            break

    verified_website = business_website is not None and any(
        km["url"] == business_website for km in keyword_matches
    )

    combined_text_parts = [business_name]
    combined_text_parts += [r["snippet"] for r in reviews]
    combined_text_parts += [r["description"] for r in other_results]
    combined_text_parts += [s["title"] for s in social_media]
    combined_text = " ".join(combined_text_parts)

    business_type = detect_business_type(business_name, fuzzy=True)
    if business_type is None:
        business_type = detect_business_type(combined_text)

    snapshot = {
        "business_type": business_type or "Not classified",
        "location": address or location,
        "verified_website": verified_website,
    }

    ai_summary = _build_ai_summary(
        business_name, business_type, address or location,
        social_media, business_website,
    )

    return {
        "business": {
            "name": business_name,
            "website": business_website,
            "phone": business_phone,
            "email": business_email,
        },
        "snapshot": snapshot,
        "ai_summary": ai_summary,
        "social_media": social_media,
        "reviews": reviews,
        "search_results": search_results,
    }