"""
MongoDB Connection Module with Motor & Fallback Memory Engine
"""
import logging
import asyncio
from typing import Dict, Any, List, Optional
try:
    from motor.motor_asyncio import AsyncIOMotorClient
except Exception:
    AsyncIOMotorClient = None

from app.utils.bson_utils import ObjectId
from app.core.config import settings

logger = logging.getLogger("mindcare.db")

class MemoryCollection:
    """In-memory MongoDB collection fallback for offline/development environments"""
    def __init__(self, name: str):
        self.name = name
        self.docs: List[Dict[str, Any]] = []

    async def insert_one(self, doc: Dict[str, Any]):
        doc_copy = dict(doc)
        if "_id" not in doc_copy or not doc_copy["_id"]:
            doc_copy["_id"] = str(ObjectId())
        elif isinstance(doc_copy["_id"], ObjectId):
            doc_copy["_id"] = str(doc_copy["_id"])
        self.docs.append(doc_copy)
        class InsertResult:
            def __init__(self, inserted_id):
                self.inserted_id = inserted_id
        return InsertResult(doc_copy["_id"])

    async def insert_many(self, docs: List[Dict[str, Any]]):
        ids = []
        for doc in docs:
            res = await self.insert_one(doc)
            ids.append(res.inserted_id)
        class InsertManyResult:
            def __init__(self, inserted_ids):
                self.inserted_ids = inserted_ids
        return InsertManyResult(ids)

    def find(self, filter_dict: Optional[Dict[str, Any]] = None, sort=None, limit: int = 0):
        class Cursor:
            def __init__(self, docs, filter_dict, sort_args, limit_val):
                self._docs = docs
                self._filter = filter_dict or {}
                self._sort = sort_args
                self._limit = limit_val

            def _match(self, doc):
                for k, v in self._filter.items():
                    if k == "$or" and isinstance(v, list):
                        match_any = False
                        for sub_f in v:
                            sub_match = True
                            for sk, sv in sub_f.items():
                                if isinstance(sv, dict) and "$regex" in sv:
                                    import re
                                    pattern = re.compile(sv["$regex"], re.IGNORECASE if sv.get("$options") == "i" else 0)
                                    if not pattern.search(str(doc.get(sk, ""))):
                                        sub_match = False
                                        break
                                elif doc.get(sk) != sv:
                                    sub_match = False
                                    break
                            if sub_match:
                                match_any = True
                                break
                        if not match_any:
                            return False
                        continue
                    if isinstance(v, dict) and "$regex" in v:
                        import re
                        pattern = re.compile(v["$regex"], re.IGNORECASE if v.get("$options") == "i" else 0)
                        if not pattern.search(str(doc.get(k, ""))):
                            return False
                        continue
                    if doc.get(k) != v:
                        return False
                return True

            async def to_list(self, length: Optional[int] = None):
                filtered = [dict(d) for d in self._docs if self._match(d)]
                if self._sort:
                    for sort_field, sort_dir in reversed(self._sort):
                        filtered.sort(key=lambda x: x.get(sort_field, ""), reverse=(sort_dir < 0))
                max_len = length or self._limit
                if max_len and max_len > 0:
                    filtered = filtered[:max_len]
                return filtered

            def sort(self, key_or_list, direction=None):
                if isinstance(key_or_list, list):
                    self._sort = key_or_list
                else:
                    self._sort = [(key_or_list, direction or 1)]
                return self

            def limit(self, l: int):
                self._limit = l
                return self

        return Cursor(self.docs, filter_dict, sort, limit)

    async def find_one(self, filter_dict: Optional[Dict[str, Any]] = None):
        cursor = self.find(filter_dict)
        res = await cursor.to_list(length=1)
        return res[0] if res else None

    async def update_one(self, filter_dict: Dict[str, Any], update_dict: Dict[str, Any], upsert: bool = False):
        target = await self.find_one(filter_dict)
        class UpdateResult:
            def __init__(self, modified):
                self.modified_count = modified
        if target:
            if "$set" in update_dict:
                for k, v in update_dict["$set"].items():
                    target[k] = v
            if "$inc" in update_dict:
                for k, v in update_dict["$inc"].items():
                    target[k] = target.get(k, 0) + v
            return UpdateResult(1)
        elif upsert:
            new_doc = dict(filter_dict)
            if "$set" in update_dict:
                new_doc.update(update_dict["$set"])
            await self.insert_one(new_doc)
            return UpdateResult(1)
        return UpdateResult(0)

    async def update_many(self, filter_dict: Dict[str, Any], update_dict: Dict[str, Any]):
        cursor = self.find(filter_dict)
        matched = await cursor.to_list()
        count = 0
        for doc in matched:
            if "$set" in update_dict:
                for k, v in update_dict["$set"].items():
                    doc[k] = v
            count += 1
        class UpdateResult:
            def __init__(self, modified):
                self.modified_count = modified
        return UpdateResult(count)

    async def delete_one(self, filter_dict: Dict[str, Any]):
        target = await self.find_one(filter_dict)
        class DeleteResult:
            def __init__(self, deleted):
                self.deleted_count = deleted
        if target:
            self.docs = [d for d in self.docs if d.get("_id") != target.get("_id")]
            return DeleteResult(1)
        return DeleteResult(0)

    async def delete_many(self, filter_dict: Dict[str, Any]):
        cursor = self.find(filter_dict)
        matched = await cursor.to_list()
        matched_ids = {m["_id"] for m in matched if "_id" in m}
        self.docs = [d for d in self.docs if d.get("_id") not in matched_ids]
        class DeleteResult:
            def __init__(self, deleted):
                self.deleted_count = deleted
        return DeleteResult(len(matched_ids))

    async def count_documents(self, filter_dict: Optional[Dict[str, Any]] = None):
        cursor = self.find(filter_dict)
        res = await cursor.to_list()
        return len(res)

    async def create_index(self, keys, **kwargs):
        pass

class MemoryDatabase:
    """In-memory MongoDB database emulator"""
    def __init__(self, name: str):
        self.name = name
        self._collections: Dict[str, MemoryCollection] = {}

    def get_collection(self, name: str) -> MemoryCollection:
        if name not in self._collections:
            self._collections[name] = MemoryCollection(name)
        return self._collections[name]

    def __getitem__(self, name: str) -> MemoryCollection:
        return self.get_collection(name)

    def __getattr__(self, name: str) -> MemoryCollection:
        if name.startswith("_"):
            raise AttributeError(f"'MemoryDatabase' object has no attribute '{name}'")
        return self.get_collection(name)

class DatabaseManager:
    client: Optional[AsyncIOMotorClient] = None
    db = None
    is_mock: bool = False

db_manager = DatabaseManager()

async def connect_to_mongo():
    logger.info("Connecting to MongoDB at: %s", settings.MONGODB_URI)
    if AsyncIOMotorClient is None:
        logger.warning("Motor/PyMongo client not available. Initializing in-memory Mongo database engine fallback.")
        db_manager.client = None
        db_manager.db = MemoryDatabase(settings.DATABASE_NAME)
        db_manager.is_mock = True
        return

    try:
        # Try connecting with short timeout to detect if live Mongo is available
        client = AsyncIOMotorClient(settings.MONGODB_URI, serverSelectionTimeoutMS=2500)
        # Verify connection
        await client.admin.command('ping')
        db_manager.client = client
        db_manager.db = client[settings.DATABASE_NAME]
        db_manager.is_mock = False
        logger.info("Successfully connected to MongoDB Atlas / Local MongoDB: %s", settings.DATABASE_NAME)
    except Exception as e:
        logger.warning("Could not connect to MongoDB server (%s). Initializing in-memory Mongo database engine fallback.", e)
        db_manager.client = None
        db_manager.db = MemoryDatabase(settings.DATABASE_NAME)
        db_manager.is_mock = True

async def close_mongo_connection():
    if db_manager.client:
        db_manager.client.close()
        logger.info("Closed MongoDB connection.")

def get_database():
    if db_manager.db is None:
        # Fallback sync init if requested before lifespan startup
        db_manager.db = MemoryDatabase(settings.DATABASE_NAME)
        db_manager.is_mock = True
    return db_manager.db
