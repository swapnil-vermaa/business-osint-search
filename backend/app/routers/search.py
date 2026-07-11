from fastapi import APIRouter, HTTPException

from app.schemas import SearchRequest
from app.services.osint import run_osint_search

router = APIRouter()


@router.post("/search")
def search_business(request: SearchRequest):
    if not request.business_name.strip() or not request.location.strip():
        raise HTTPException(status_code=400, detail="business_name and location are required")

    result = run_osint_search(
        business_name=request.business_name,
        location=request.location,
        address=request.address,
    )
    return result


@router.get("/health")
def health():
    return {"status": "ok"}