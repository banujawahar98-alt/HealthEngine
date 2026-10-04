"""
Professional Directory Repository Layer
"""
import datetime
from typing import Optional, List, Dict, Any
from app.utils.bson_utils import ObjectId
from app.db.mongodb import get_database

class ProfessionalRepository:
    @property
    def db(self):
        return get_database()

    async def get_all_professionals(
        self,
        specialization: Optional[str] = None,
        location: Optional[str] = None,
        mode: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        query: Dict[str, Any] = {}
        if specialization:
            query["specialization"] = {"$regex": specialization, "$options": "i"}
        if location:
            query["location"] = {"$regex": location, "$options": "i"}
        if mode:
            query["consultation_mode"] = {"$regex": mode, "$options": "i"}
        if search:
            query["$or"] = [
                {"name": {"$regex": search, "$options": "i"}},
                {"qualification": {"$regex": search, "$options": "i"}},
                {"specialization": {"$regex": search, "$options": "i"}},
                {"location": {"$regex": search, "$options": "i"}}
            ]
        cursor = self.db.professionals.find(query).sort([("name", 1)])
        return await cursor.to_list(length=100)

    async def get_by_id(self, professional_id: str) -> Optional[Dict[str, Any]]:
        doc = await self.db.professionals.find_one({"_id": professional_id})
        if not doc:
            try:
                doc = await self.db.professionals.find_one({"_id": ObjectId(professional_id)})
            except Exception:
                pass
        return doc

    async def create_professional(self, data: Dict[str, Any]) -> Dict[str, Any]:
        doc = dict(data)
        doc["created_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        res = await self.db.professionals.insert_one(doc)
        doc["_id"] = str(res.inserted_id)
        return doc

    async def update_professional(self, professional_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        target = await self.get_by_id(professional_id)
        if not target:
            return None
        await self.db.professionals.update_one({"_id": target["_id"]}, {"$set": data})
        return await self.get_by_id(professional_id)

    async def delete_professional(self, professional_id: str) -> bool:
        target = await self.get_by_id(professional_id)
        if not target:
            return False
        res = await self.db.professionals.delete_one({"_id": target["_id"]})
        return res.deleted_count > 0

    async def count_professionals(self) -> int:
        return await self.db.professionals.count_documents({})
