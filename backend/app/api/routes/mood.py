"""
Mood Tracker API Routes
"""
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.mood import MoodEntryCreate, MoodEntryUpdate
from app.services.mood_service import MoodService
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/api/mood", tags=["Mood Tracking"])
mood_service = MoodService()

@router.post("")
async def create_mood_entry(req: MoodEntryCreate, current_user: dict = Depends(get_current_user)):
    entry = await mood_service.add_mood_entry(
        user_id=current_user["id"],
        mood=req.mood,
        stress_level=req.stress_level,
        energy_level=req.energy_level,
        sleep_hours=req.sleep_hours,
        note=req.note
    )
    return {
        "success": True,
        "message": "Mood entry recorded.",
        "data": entry
    }

@router.get("")
async def list_mood_entries(current_user: dict = Depends(get_current_user)):
    entries = await mood_service.get_user_mood_entries(current_user["id"])
    return {
        "success": True,
        "message": "Mood history retrieved.",
        "data": entries
    }

@router.put("/{id}")
async def update_mood_entry(id: str, req: MoodEntryUpdate, current_user: dict = Depends(get_current_user)):
    updated = await mood_service.update_mood_entry(
        entry_id=id,
        user_id=current_user["id"],
        update_data=req.model_dump(exclude_unset=True)
    )
    if not updated:
        raise HTTPException(status_code=404, detail={"success": False, "message": "Mood entry not found or unauthorized", "error_code": "NOT_FOUND"})
    return {
        "success": True,
        "message": "Mood entry updated.",
        "data": updated
    }

@router.delete("/{id}")
async def delete_mood_entry(id: str, current_user: dict = Depends(get_current_user)):
    success = await mood_service.delete_mood_entry(id, current_user["id"])
    if not success:
        raise HTTPException(status_code=404, detail={"success": False, "message": "Mood entry not found or unauthorized", "error_code": "NOT_FOUND"})
    return {
        "success": True,
        "message": "Mood entry deleted.",
        "data": None
    }
