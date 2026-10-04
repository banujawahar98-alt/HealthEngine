"""
Mood Repository Layer
"""
import datetime
from typing import Optional, List, Dict, Any
from app.utils.bson_utils import ObjectId
from app.db.mongodb import get_database

class MoodRepository:
    @property
    def db(self):
        return get_database()

    async def create_entry(self, user_id: str, entry_data: Dict[str, Any]) -> Dict[str, Any]:
        doc = dict(entry_data)
        doc["user_id"] = user_id
        doc["created_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        res = await self.db.mood_entries.insert_one(doc)
        doc["_id"] = str(res.inserted_id)
        return doc

    async def update_entry(self, entry_id: str, user_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        target = await self.get_entry_by_id(entry_id)
        if not target or target.get("user_id") != user_id:
            return None
        
        update_doc = dict(update_data)
        update_doc["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        await self.db.mood_entries.update_one({"_id": target["_id"]}, {"$set": update_doc})
        return await self.get_entry_by_id(entry_id)

    async def delete_entry(self, entry_id: str, user_id: str) -> bool:
        target = await self.get_entry_by_id(entry_id)
        if not target or target.get("user_id") != user_id:
            return False
        res = await self.db.mood_entries.delete_one({"_id": target["_id"]})
        return res.deleted_count > 0

    async def get_user_entries(self, user_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        cursor = self.db.mood_entries.find({"user_id": user_id}).sort([("created_at", -1)]).limit(limit)
        return await cursor.to_list(length=limit)

    async def get_entry_by_id(self, entry_id: str) -> Optional[Dict[str, Any]]:
        doc = await self.db.mood_entries.find_one({"_id": entry_id})
        if not doc:
            try:
                doc = await self.db.mood_entries.find_one({"_id": ObjectId(entry_id)})
            except Exception:
                pass
        return doc
