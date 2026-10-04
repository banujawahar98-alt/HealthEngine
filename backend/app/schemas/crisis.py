"""
Crisis Resources Schemas
"""
from typing import Optional
from pydantic import BaseModel, Field

class CrisisResourceCreate(BaseModel):
    name: str
    description: str
    phone: str
    website: Optional[str] = None
    country: str = "Global"
    availability: str = "24/7"
    source: Optional[str] = "Verified Helpline"
    active: bool = True

class CrisisResourceResponse(BaseModel):
    id: str
    name: str
    description: str
    phone: str
    website: Optional[str] = None
    country: str
    availability: str
    source: Optional[str] = None
    active: bool
    created_at: str
