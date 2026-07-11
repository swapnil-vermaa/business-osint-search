from pydantic import BaseModel
from typing import Optional


class SearchRequest(BaseModel):
    business_name: str
    location: str
    address: Optional[str] = None