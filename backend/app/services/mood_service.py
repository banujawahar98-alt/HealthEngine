"""
Mood Service
"""
from typing import List, Dict, Any, Optional
from app.repositories.mood_repository import MoodRepository

class MoodService:
    def __init__(self):
        self.mood_repo = MoodRepository()

    async def add_mood_entry(self, user_id: str, mood: int, stress_level: int, energy_level: int, sleep_hours: float, note: Optional[str] = None) -> Dict[str, Any]:
        doc = {
            "mood": mood,
            "stress_level": stress_level,
            "energy_level": energy_level,
            "sleep_hours": sleep_hours,
            "note": note
        }
        res = await self.mood_repo.create_entry(user_id, doc)
        return {
            "id": str(res["_id"]),
            "user_id": res["user_id"],
            "mood": res["mood"],
            "stress_level": res["stress_level"],
            "energy_level": res["energy_level"],
            "sleep_hours": res["sleep_hours"],
            "note": res.get("note"),
            "created_at": res["created_at"]
        }

    async def get_user_mood_entries(self, user_id: str, limit: int = 60) -> List[Dict[str, Any]]:
        entries = await self.mood_repo.get_user_entries(user_id, limit)
        out = []
        for e in entries:
            out.append({
                "id": str(e["_id"]),
                "user_id": e["user_id"],
                "mood": e["mood"],
                "stress_level": e["stress_level"],
                "energy_level": e["energy_level"],
                "sleep_hours": e["sleep_hours"],
                "note": e.get("note"),
                "created_at": e["created_at"]
            })
        return out

    async def update_mood_entry(self, entry_id: str, user_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        clean_update = {k: v for k, v in update_data.items() if v is not None}
        updated = await self.mood_repo.update_entry(entry_id, user_id, clean_update)
        if not updated:
            return None
        return {
            "id": str(updated["_id"]),
            "user_id": updated["user_id"],
            "mood": updated["mood"],
            "stress_level": updated["stress_level"],
            "energy_level": updated["energy_level"],
            "sleep_hours": updated["sleep_hours"],
            "note": updated.get("note"),
            "created_at": updated["created_at"]
        }

    async def delete_mood_entry(self, entry_id: str, user_id: str) -> bool:
        return await self.mood_repo.delete_entry(entry_id, user_id)
