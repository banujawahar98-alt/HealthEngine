"""
Crisis Resources Repository Layer
"""
import datetime
from typing import Optional, List, Dict, Any
from app.utils.bson_utils import ObjectId
from app.db.mongodb import get_database

class CrisisRepository:
    @property
    def db(self):
        return get_database()

    async def get_active_crisis_resources(self, country: Optional[str] = None) -> List[Dict[str, Any]]:
        query: Dict[str, Any] = {"active": True}
        if country:
            query["$or"] = [{"country": country}, {"country": "Global"}]
        cursor = self.db.crisis_resources.find(query).sort([("name", 1)])
        return await cursor.to_list(length=100)

    async def get_by_id(self, crisis_id: str) -> Optional[Dict[str, Any]]:
        doc = await self.db.crisis_resources.find_one({"_id": crisis_id})
        if not doc:
            try:
                doc = await self.db.crisis_resources.find_one({"_id": ObjectId(crisis_id)})
            except Exception:
                pass
        return doc

    async def create_crisis_resource(self, data: Dict[str, Any]) -> Dict[str, Any]:
        doc = dict(data)
        doc["created_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        res = await self.db.crisis_resources.insert_one(doc)
        doc["_id"] = str(res.inserted_id)
        return doc

    async def update_crisis_resource(self, crisis_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        target = await self.get_by_id(crisis_id)
        if not target:
            return None
        await self.db.crisis_resources.update_one({"_id": target["_id"]}, {"$set": data})
        return await self.get_by_id(crisis_id)

    async def delete_crisis_resource(self, crisis_id: str) -> bool:
        target = await self.get_by_id(crisis_id)
        if not target:
            return False
        res = await self.db.crisis_resources.delete_one({"_id": target["_id"]})
        return res.deleted_count > 0
