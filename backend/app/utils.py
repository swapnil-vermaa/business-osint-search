import re
from urllib.parse import urlparse

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_REGEX = re.compile(r"(\+\d{1,3}[-.\s]?)?\(?\d{3,4}\)?[-.\s]\d{3,4}[-.\s]?\d{0,4}")

PLATFORM_DOMAINS = {
    "linkedin.com": "LinkedIn",
    "facebook.com": "Facebook",
    "instagram.com": "Instagram",
    "twitter.com": "X (Twitter)",
    "x.com": "X (Twitter)",
    "youtube.com": "YouTube",
    "github.com": "GitHub",
    "crunchbase.com": "Crunchbase",
    "wikipedia.org": "Wikipedia",
}

REVIEW_DOMAINS = {
    "glassdoor.com": "Glassdoor",
    "glassdoor.co.in": "Glassdoor",
    "glassdoor.ie": "Glassdoor",
    "indeed.com": "Indeed",
    "trustpilot.com": "Trustpilot",
    "ambitionbox.com": "AmbitionBox",
}


def extract_emails(text: str) -> list[str]:
    return list(set(EMAIL_REGEX.findall(text)))


def extract_phones(text: str) -> list[str]:
    results = []
    for match in PHONE_REGEX.finditer(text):
        value = match.group().strip()
        digits_only = re.sub(r"\D", "", value)

        # date jaisa pattern reject karo (e.g. 20251215 se bana koi number)
        if re.match(r"^\d{4}\d{2}\d{2}$", digits_only):
            continue

        if 8 <= len(digits_only) <= 13:
            results.append(value)

    return list(set(results))


def get_domain(url: str) -> str:
    try:
        netloc = urlparse(url).netloc.lower()
        return netloc.replace("www.", "")
    except Exception:
        return ""


def is_pdf(url: str) -> bool:
    return url.lower().endswith(".pdf")


def _domain_matches(domain: str, target: str) -> bool:
    return domain == target or domain.endswith("." + target)


def is_social(domain: str):
    for d, platform in PLATFORM_DOMAINS.items():
        if _domain_matches(domain, d):
            return platform
    return None


def is_review_site(domain: str):
    for d, source in REVIEW_DOMAINS.items():
        if _domain_matches(domain, d):
            return source
    return None