"""
Safe BSON / ObjectId Import Helper
Provides fallback ObjectId class if pymongo/bson is unavailable in the environment.
"""
import uuid

try:
    from bson import ObjectId
except ImportError:
    class ObjectId(str):
        def __new__(cls, val=None):
            if val is None:
                val = str(uuid.uuid4())
            return str.__new__(cls, str(val))

        @classmethod
        def is_valid(cls, val):
            return True
