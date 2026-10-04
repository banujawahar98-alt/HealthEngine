"""
Resource Library API Routes
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from app.repositories.resource_repository import ResourceRepository
from app.api.dependencies import get_optional_user

router = APIRouter(prefix="/api/resources", tags=["Resource Library"])
resource_repo = ResourceRepository()

@router.get("")
async def list_resources(
    category: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    current_user: Optional[dict] = Depends(get_optional_user)
):
    resources = await resource_repo.get_all_resources(category=category, tag=tag, search=search)
    out = []
    for r in resources:
        out.append({
            "id": str(r["_id"]),
            "title": r.get("title", ""),
            "description": r.get("description", ""),
            "content": r.get("content", ""),
            "category": r.get("category", "General"),
            "tags": r.get("tags", []),
            "source": r.get("source"),
            "url": r.get("url"),
            "created_at": r.get("created_at", "")
        })
    return {
        "success": True,
        "message": "Resource library loaded.",
        "data": out
    }

@router.get("/{id}")
async def get_resource(id: str, current_user: Optional[dict] = Depends(get_optional_user)):
    r = await resource_repo.get_resource_by_id(id)
    if not r:
        raise HTTPException(status_code=404, detail={"success": False, "message": "Resource not found", "error_code": "NOT_FOUND"})
    return {
        "success": True,
        "message": "Resource detail loaded.",
        "data": {
            "id": str(r["_id"]),
            "title": r.get("title", ""),
            "description": r.get("description", ""),
            "content": r.get("content", ""),
            "category": r.get("category", "General"),
            "tags": r.get("tags", []),
            "source": r.get("source"),
            "url": r.get("url"),
            "created_at": r.get("created_at", "")
        }
    }
