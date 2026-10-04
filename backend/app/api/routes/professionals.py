"""
Professional Support Directory Routes
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from app.repositories.professional_repository import ProfessionalRepository
from app.api.dependencies import get_optional_user

router = APIRouter(prefix="/api/professionals", tags=["Professional Directory"])
prof_repo = ProfessionalRepository()

@router.get("")
async def list_professionals(
    specialization: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    mode: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    current_user: Optional[dict] = Depends(get_optional_user)
):
    profs = await prof_repo.get_all_professionals(
        specialization=specialization,
        location=location,
        mode=mode,
        search=search
    )
    out = []
    for p in profs:
        out.append({
            "id": str(p["_id"]),
            "name": p.get("name", ""),
            "qualification": p.get("qualification", ""),
            "specialization": p.get("specialization", ""),
            "experience": p.get("experience", ""),
            "location": p.get("location", ""),
            "consultation_mode": p.get("consultation_mode", "Online & In-Person"),
            "availability": p.get("availability", ""),
            "contact_email": p.get("contact_email"),
            "contact_phone": p.get("contact_phone"),
            "bio": p.get("bio"),
            "is_mock": p.get("is_mock", True),
            "created_at": p.get("created_at", "")
        })
    return {
        "success": True,
        "message": "Professionals directory retrieved.",
        "data": out
    }

@router.get("/{id}")
async def get_professional(id: str, current_user: Optional[dict] = Depends(get_optional_user)):
    p = await prof_repo.get_by_id(id)
    if not p:
        raise HTTPException(status_code=404, detail={"success": False, "message": "Professional profile not found", "error_code": "NOT_FOUND"})
    return {
        "success": True,
        "message": "Professional profile loaded.",
        "data": {
            "id": str(p["_id"]),
            "name": p.get("name", ""),
            "qualification": p.get("qualification", ""),
            "specialization": p.get("specialization", ""),
            "experience": p.get("experience", ""),
            "location": p.get("location", ""),
            "consultation_mode": p.get("consultation_mode", "Online & In-Person"),
            "availability": p.get("availability", ""),
            "contact_email": p.get("contact_email"),
            "contact_phone": p.get("contact_phone"),
            "bio": p.get("bio"),
            "is_mock": p.get("is_mock", True),
            "created_at": p.get("created_at", "")
        }
    }
