import logging
import time

from fastapi import APIRouter, HTTPException

from app.schemas import SearchRequest
from app.services.osint import run_osint_search

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/search")
def search_business(request: SearchRequest):
    if not request.business_name.strip() or not request.location.strip():
        logger.warning("Rejected request — missing business_name/location: %s", request.dict())
        raise HTTPException(status_code=400, detail="business_name and location are required")

    logger.info("🔍 New search: '%s' @ '%s'", request.business_name, request.location)
    start = time.time()

    try:
        result = run_osint_search(
            business_name=request.business_name,
            location=request.location,
            address=request.address,
        )
    except Exception:
        logger.exception("Search failed for '%s'", request.business_name)
        raise HTTPException(status_code=500, detail="Internal error while running search")

    elapsed = time.time() - start
    logger.info(
        "✅ Done in %.2fs — website=%s, social=%d, reviews=%d, other=%d",
        elapsed,
        bool(result["business"]["website"]),
        len(result["social_media"]),
        len(result["reviews"]),
        len(result["search_results"]),
    )
    return result


@router.get("/health")
def health():
    logger.debug("Health check hit")
    return {"status": "ok"}