"""
AI Assistant Service Orchestrator
"""
from typing import Dict, Any, List, Optional
from app.repositories.ai_repository import AIRepository
from app.services.safety_service import SafetyService
from app.services.rag_service import RAGService
from app.ai.llm_client import LLMClient

class AIService:
    def __init__(self):
        self.ai_repo = AIRepository()
        self.safety_service = SafetyService()
        self.rag_service = RAGService()

    async def handle_chat_message(self, user_id: str, message: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        # 1. Create conversation if new
        if not conversation_id:
            title_snippet = message[:30] + ("..." if len(message) > 30 else "")
            conv = await self.ai_repo.create_conversation(user_id, title_snippet)
            conversation_id = conv["_id"]
        else:
            conv = await self.ai_repo.get_conversation_by_id(conversation_id, user_id)
            if not conv:
                conv = await self.ai_repo.create_conversation(user_id, message[:30])
                conversation_id = conv["_id"]

        # 2. Safety Analysis
        safety_res = await self.safety_service.analyze_message(message)

        # Record user message in DB
        await self.ai_repo.add_message(conversation_id, "user", message)

        # 3. If IMMEDIATE_SAFETY_CONCERN, suppress LLM response
        if safety_res["risk_level"] == "IMMEDIATE_SAFETY_CONCERN":
            bot_msg = safety_res["safety_message"]
            saved_bot_msg = await self.ai_repo.add_message(
                conversation_id,
                "assistant",
                bot_msg,
                safety_analysis=safety_res
            )
            return {
                "id": saved_bot_msg["_id"],
                "conversation_id": conversation_id,
                "role": "assistant",
                "message": bot_msg,
                "created_at": saved_bot_msg["created_at"],
                "safety_analysis": safety_res
            }

        # 4. RAG Retrieval & LLM Generation
        history_msgs = await self.ai_repo.get_conversation_messages(conversation_id)
        rag_docs = await self.rag_service.retrieve_context(message, top_k=2)

        bot_reply = await LLMClient.generate_response(message, history_msgs, rag_docs)

        saved_bot_msg = await self.ai_repo.add_message(
            conversation_id,
            "assistant",
            bot_reply,
            safety_analysis=safety_res
        )

        return {
            "id": saved_bot_msg["_id"],
            "conversation_id": conversation_id,
            "role": "assistant",
            "message": bot_reply,
            "created_at": saved_bot_msg["created_at"],
            "safety_analysis": safety_res
        }

    async def get_user_conversations(self, user_id: str) -> List[Dict[str, Any]]:
        convs = await self.ai_repo.get_user_conversations(user_id)
        out = []
        for c in convs:
            out.append({
                "id": str(c["_id"]),
                "user_id": c["user_id"],
                "title": c.get("title", "Conversation"),
                "created_at": c.get("created_at", ""),
                "updated_at": c.get("updated_at", ""),
                "message_count": c.get("message_count", 0)
            })
        return out

    async def get_conversation_messages(self, conversation_id: str, user_id: str) -> List[Dict[str, Any]]:
        conv = await self.ai_repo.get_conversation_by_id(conversation_id, user_id)
        if not conv:
            return []
        msgs = await self.ai_repo.get_conversation_messages(conversation_id)
        out = []
        for m in msgs:
            out.append({
                "id": str(m["_id"]),
                "conversation_id": m["conversation_id"],
                "role": m["role"],
                "message": m["message"],
                "created_at": m["created_at"],
                "safety_analysis": m.get("safety_analysis")
            })
        return out

    async def delete_conversation(self, conversation_id: str, user_id: str) -> bool:
        return await self.ai_repo.delete_conversation(conversation_id, user_id)
