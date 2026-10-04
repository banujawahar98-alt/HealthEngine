"""
MongoDB Index Creation
"""
import logging
from app.db.mongodb import get_database

logger = logging.getLogger("mindcare.db.indexes")

async def create_db_indexes():
    db = get_database()
    logger.info("Ensuring database indexes...")
    try:
        # users
        await db.users.create_index("email", unique=True)
        # assessment_attempts
        await db.assessment_attempts.create_index("user_id")
        await db.assessment_attempts.create_index("assessment_id")
        await db.assessment_attempts.create_index("created_at")
        # assessment_results
        await db.assessment_results.create_index("user_id")
        await db.assessment_results.create_index("attempt_id")
        # mood_entries
        await db.mood_entries.create_index("user_id")
        await db.mood_entries.create_index("created_at")
        # ai_conversations
        await db.ai_conversations.create_index("user_id")
        # ai_messages
        await db.ai_messages.create_index("conversation_id")
        # resources
        await db.resources.create_index("category")
        await db.resources.create_index("tags")
        logger.info("Indexes successfully ensured.")
    except Exception as e:
        logger.warning("Error creating indexes (non-fatal): %s", e)
