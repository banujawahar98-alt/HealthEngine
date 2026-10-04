"""
AI Conversations and Messages Repository Layer
"""
import datetime
from typing import Optional, List, Dict, Any
from app.utils.bson_utils import ObjectId
from app.db.mongodb import get_database

class AIRepository:
    @property
    def db(self):
        return get_database()

    async def create_conversation(self, user_id: str, title: str) -> Dict[str, Any]:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        doc = {
            "user_id": user_id,
            "title": title,
            "created_at": now,
            "updated_at": now
        }
        res = await self.db.ai_conversations.insert_one(doc)
        doc["_id"] = str(res.inserted_id)
        return doc

    async def get_user_conversations(self, user_id: str) -> List[Dict[str, Any]]:
        cursor = self.db.ai_conversations.find({"user_id": user_id}).sort([("updated_at", -1)])
        convs = await cursor.to_list(length=100)
        # Populate message counts
        for c in convs:
            cid = str(c["_id"])
            cnt = await self.db.ai_messages.count_documents({"conversation_id": cid})
            c["message_count"] = cnt
        return convs

    async def get_conversation_by_id(self, conversation_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        doc = await self.db.ai_conversations.find_one({"_id": conversation_id, "user_id": user_id})
        if not doc:
            try:
                doc = await self.db.ai_conversations.find_one({"_id": ObjectId(conversation_id), "user_id": user_id})
            except Exception:
                pass
        return doc

    async def delete_conversation(self, conversation_id: str, user_id: str) -> bool:
        conv = await self.get_conversation_by_id(conversation_id, user_id)
        if not conv:
            return False
        cid = str(conv["_id"])
        await self.db.ai_messages.delete_many({"conversation_id": cid})
        res = await self.db.ai_conversations.delete_one({"_id": conv["_id"]})
        return res.deleted_count > 0

    async def add_message(self, conversation_id: str, role: str, message: str, safety_analysis: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        doc = {
            "conversation_id": conversation_id,
            "role": role,
            "message": message,
            "safety_analysis": safety_analysis,
            "created_at": now
        }
        res = await self.db.ai_messages.insert_one(doc)
        doc["_id"] = str(res.inserted_id)
        # Update conversation updated_at
        await self.db.ai_conversations.update_one({"_id": conversation_id}, {"$set": {"updated_at": now}})
        return doc

    async def get_conversation_messages(self, conversation_id: str) -> List[Dict[str, Any]]:
        cursor = self.db.ai_messages.find({"conversation_id": conversation_id}).sort([("created_at", 1)])
        return await cursor.to_list(length=500)
