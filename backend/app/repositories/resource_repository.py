"""
Resource Repository Layer
"""
import datetime
from typing import Optional, List, Dict, Any
from app.utils.bson_utils import ObjectId
from app.db.mongodb import get_database

class ResourceRepository:
    @property
    def db(self):
        return get_database()

    async def get_all_resources(self, category: Optional[str] = None, tag: Optional[str] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
        query: Dict[str, Any] = {}
        if category:
            clean_cat = category.replace("+", " ").strip()
            query["category"] = {"$regex": f"^{clean_cat}$", "$options": "i"}
        if tag:
            clean_tag = tag.replace("+", " ").strip()
            query["tags"] = {"$regex": f"^{clean_tag}$", "$options": "i"}
        if search:
            query["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"description": {"$regex": search, "$options": "i"}},
                {"content": {"$regex": search, "$options": "i"}},
                {"category": {"$regex": search, "$options": "i"}},
                {"tags": {"$regex": search, "$options": "i"}}
            ]
        cursor = self.db.resources.find(query).sort([("created_at", -1)])
        return await cursor.to_list(length=200)

    async def get_resource_by_id(self, resource_id: str) -> Optional[Dict[str, Any]]:
        doc = await self.db.resources.find_one({"_id": resource_id})
        if not doc:
            try:
                doc = await self.db.resources.find_one({"_id": ObjectId(resource_id)})
            except Exception:
                pass
        return doc

    async def create_resource(self, resource_data: Dict[str, Any]) -> Dict[str, Any]:
        doc = dict(resource_data)
        doc["created_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        res = await self.db.resources.insert_one(doc)
        doc["_id"] = str(res.inserted_id)
        return doc

    async def update_resource(self, resource_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        target = await self.get_resource_by_id(resource_id)
        if not target:
            return None
        await self.db.resources.update_one({"_id": target["_id"]}, {"$set": update_data})
        return await self.get_resource_by_id(resource_id)

    async def delete_resource(self, resource_id: str) -> bool:
        target = await self.get_resource_by_id(resource_id)
        if not target:
            return False
        res = await self.db.resources.delete_one({"_id": target["_id"]})
        return res.deleted_count > 0

    async def count_resources(self) -> int:
        return await self.db.resources.count_documents({})
