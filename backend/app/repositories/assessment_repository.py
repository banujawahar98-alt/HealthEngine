"""
Assessment Repository Layer
"""
import datetime
from typing import Optional, List, Dict, Any
from app.utils.bson_utils import ObjectId
from app.db.mongodb import get_database

class AssessmentRepository:
    @property
    def db(self):
        return get_database()

    async def get_active_assessments(self) -> List[Dict[str, Any]]:
        cursor = self.db.assessments.find({"active": True})
        return await cursor.to_list(length=100)

    async def get_assessment_by_id(self, assessment_id: str) -> Optional[Dict[str, Any]]:
        doc = await self.db.assessments.find_one({"_id": assessment_id})
        if not doc:
            try:
                doc = await self.db.assessments.find_one({"_id": ObjectId(assessment_id)})
            except Exception:
                pass
        return doc

    async def create_or_update_assessment(self, assessment_doc: Dict[str, Any]) -> Dict[str, Any]:
        doc = dict(assessment_doc)
        if "_id" not in doc:
            res = await self.db.assessments.insert_one(doc)
            doc["_id"] = str(res.inserted_id)
        else:
            aid = doc["_id"]
            await self.db.assessments.update_one({"_id": aid}, {"$set": doc}, upsert=True)
        return doc

    async def save_attempt(self, attempt_data: Dict[str, Any]) -> Dict[str, Any]:
        doc = dict(attempt_data)
        doc["created_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        res = await self.db.assessment_attempts.insert_one(doc)
        doc["_id"] = str(res.inserted_id)
        return doc

    async def save_result(self, result_data: Dict[str, Any]) -> Dict[str, Any]:
        doc = dict(result_data)
        doc["created_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        res = await self.db.assessment_results.insert_one(doc)
        doc["_id"] = str(res.inserted_id)
        return doc

    async def get_user_results(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        cursor = self.db.assessment_results.find({"user_id": user_id}).sort([("created_at", -1)]).limit(limit)
        return await cursor.to_list(length=limit)

    async def get_latest_user_result(self, user_id: str, assessment_id: str) -> Optional[Dict[str, Any]]:
        cursor = self.db.assessment_results.find({
            "user_id": user_id,
            "assessment_id": assessment_id
        }).sort([("created_at", -1)]).limit(1)
        results = await cursor.to_list(length=1)
        return results[0] if results else None

    async def get_result_by_id(self, result_id: str) -> Optional[Dict[str, Any]]:
        doc = await self.db.assessment_results.find_one({"_id": result_id})
        if not doc:
            try:
                doc = await self.db.assessment_results.find_one({"_id": ObjectId(result_id)})
            except Exception:
                pass
        return doc

    async def count_total_results(self) -> int:
        return await self.db.assessment_results.count_documents({})
