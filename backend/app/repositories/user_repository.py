"""
User Repository Layer
"""
import datetime
from typing import Optional, Dict, Any, List
from app.utils.bson_utils import ObjectId
from app.db.mongodb import get_database

class UserRepository:
    @property
    def db(self):
        return get_database()

    async def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        return await self.db.users.find_one({"email": email.lower().strip()})

    async def get_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        # Try both string _id and ObjectId
        doc = await self.db.users.find_one({"_id": user_id})
        if not doc:
            try:
                doc = await self.db.users.find_one({"_id": ObjectId(user_id)})
            except Exception:
                pass
        return doc

    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        user_doc = dict(user_data)
        user_doc["email"] = user_doc["email"].lower().strip()
        user_doc["created_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        user_doc["updated_at"] = user_doc["created_at"]
        res = await self.db.users.insert_one(user_doc)
        user_doc["_id"] = str(res.inserted_id)
        return user_doc

    async def update_user(self, user_id: str, update_data: Dict[str, Any]) -> bool:
        update_doc = dict(update_data)
        update_doc["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        res = await self.db.users.update_one({"_id": user_id}, {"$set": update_doc})
        if res.modified_count == 0:
            try:
                res = await self.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_doc})
            except Exception:
                pass
        return res.modified_count > 0

    async def delete_user(self, user_id: str) -> bool:
        res = await self.db.users.delete_one({"_id": user_id})
        if res.deleted_count == 0:
            try:
                res = await self.db.users.delete_one({"_id": ObjectId(user_id)})
            except Exception:
                pass
        return res.deleted_count > 0

    async def count_users(self) -> int:
        return await self.db.users.count_documents({})
