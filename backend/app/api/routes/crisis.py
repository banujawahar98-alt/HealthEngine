"""
Crisis Resources API Routes
"""
from typing import Optional
from fastapi import APIRouter, Query
from app.repositories.crisis_repository import CrisisRepository

router = APIRouter(prefix="/api/crisis-resources", tags=["Crisis Helplines"])
crisis_repo = CrisisRepository()

@router.get("")
async def list_crisis_resources(country: Optional[str] = Query(None)):
    resources = await crisis_repo.get_active_crisis_resources(country=country)
    out = []
    for r in resources:
        out.append({
            "id": str(r["_id"]),
            "name": r.get("name", ""),
            "description": r.get("description", ""),
            "phone": r.get("phone", ""),
            "website": r.get("website"),
            "country": r.get("country", "Global"),
            "availability": r.get("availability", "24/7"),
            "source": r.get("source"),
            "active": r.get("active", True),
            "created_at": r.get("created_at", "")
        })
    return {
        "success": True,
        "message": "Crisis resources loaded.",
        "data": out
    }
