from app.services.query_builder import build_queries
from app.services.google_search import search_google
from app.services.extractor import fetch_page
from app.utils import get_domain, is_pdf, is_social, is_review_site


def run_osint_search(business_name: str, location: str, address: str = None) -> dict:
    queries = build_queries(business_name, location, address)

    all_urls = []
    for query in queries:
        all_urls.extend(search_google(query))

    seen = set()
    unique_urls = []
    for url in all_urls:
        if url not in seen:
            seen.add(url)
            unique_urls.append(url)

    business_website = None
    business_phone = None
    business_email = None
    business_description = None

    social_media = []
    documents = []
    reviews = []
    search_results = []

    # business name ka pehla shabd nikala, official site dhundne ke liye
    business_keyword = business_name.strip().split()[0].lower()

    for url in unique_urls[:25]:
        domain = get_domain(url)

        if is_pdf(url):
            documents.append({"title": url.split("/")[-1] or "Document", "url": url})
            continue

        platform = is_social(domain)
        review_source = is_review_site(domain)

        page_data = fetch_page(url)
        title = page_data["title"] or url
        description = page_data["description"]

        if platform:
            social_media.append({"platform": platform, "url": url, "title": title})
        elif review_source:
            reviews.append({"source": review_source, "url": url, "snippet": description})
        else:
            search_results.append({"title": title, "url": url, "description": description})

            # sirf tabhi email/phone business ka maano, jab domain mein
            # business ka naam ho (taaki third-party sites ka data na aaye)
            if business_keyword in domain:
                if business_website is None:
                    business_website = url
                    business_description = description
                if page_data["emails"] and not business_email:
                    business_email = page_data["emails"][0]
                if page_data["phones"] and not business_phone:
                    business_phone = page_data["phones"][0]

    return {
        "business": {
            "name": business_name,
            "website": business_website,
            "address": address or location,
            "phone": business_phone,
            "email": business_email,
            "description": business_description,
        },
        "social_media": social_media,
        "documents": documents,
        "reviews": reviews,
        "search_results": search_results,
    }