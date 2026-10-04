"""
User Profile & Data Export Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import ProfileUpdateRequest
from app.repositories.user_repository import UserRepository
from app.repositories.assessment_repository import AssessmentRepository
from app.repositories.mood_repository import MoodRepository
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/api/users", tags=["Users"])
user_repo = UserRepository()
assessment_repo = AssessmentRepository()
mood_repo = MoodRepository()

@router.put("/profile")
async def update_profile(req: ProfileUpdateRequest, current_user: dict = Depends(get_current_user)):
    update_dict = {}
    if req.name is not None:
        update_dict["name"] = req.name
    if req.age_range is not None:
        update_dict["age_range"] = req.age_range

    if update_dict:
        await user_repo.update_user(current_user["id"], update_dict)

    updated_user = await user_repo.get_by_id(current_user["id"])
    return {
        "success": True,
        "message": "Profile updated successfully.",
        "data": {
            "id": str(updated_user["_id"]),
            "name": updated_user["name"],
            "email": updated_user["email"],
            "role": updated_user["role"],
            "age_range": updated_user.get("age_range"),
            "created_at": updated_user.get("created_at", "")
        }
    }

@router.get("/export-data")
async def export_user_data(current_user: dict = Depends(get_current_user)):
    uid = current_user["id"]
    assessments = await assessment_repo.get_user_results(uid, limit=500)
    moods = await mood_repo.get_user_entries(uid, limit=500)

    export_payload = {
        "user_profile": {
            "name": current_user["name"],
            "email": current_user["email"],
            "role": current_user["role"],
            "age_range": current_user.get("age_range"),
            "created_at": current_user.get("created_at")
        },
        "assessment_results": assessments,
        "mood_entries": moods,
        "disclaimer": "Exported mental health screening and well-being tracking data."
    }

    return {
        "success": True,
        "message": "User data exported successfully.",
        "data": export_payload
    }
