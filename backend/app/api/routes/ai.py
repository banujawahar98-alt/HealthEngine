"""
AI Assistant & RAG Chat Routes
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.ai import ChatMessageRequest
from app.services.ai_service import AIService
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/api/ai", tags=["AI Assistant"])
ai_service = AIService()

@router.post("/chat")
async def chat_message(req: ChatMessageRequest, current_user: dict = Depends(get_current_user)):
    try:
        reply = await ai_service.handle_chat_message(
            user_id=current_user["id"],
            message=req.message,
            conversation_id=req.conversation_id
        )
        return {
            "success": True,
            "message": "AI assistant response generated.",
            "data": reply
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={"success": False, "message": f"AI processing error: {str(e)}", "error_code": "AI_ERROR"})

@router.get("/conversations")
async def list_conversations(current_user: dict = Depends(get_current_user)):
    convs = await ai_service.get_user_conversations(current_user["id"])
    return {
        "success": True,
        "message": "Conversations list loaded.",
        "data": convs
    }

@router.get("/conversations/{id}")
async def get_conversation(id: str, current_user: dict = Depends(get_current_user)):
    msgs = await ai_service.get_conversation_messages(id, current_user["id"])
    return {
        "success": True,
        "message": "Conversation messages loaded.",
        "data": msgs
    }

@router.delete("/conversations/{id}")
async def delete_conversation(id: str, current_user: dict = Depends(get_current_user)):
    success = await ai_service.delete_conversation(id, current_user["id"])
    if not success:
        raise HTTPException(status_code=404, detail={"success": False, "message": "Conversation not found or unauthorized", "error_code": "NOT_FOUND"})
    return {
        "success": True,
        "message": "Conversation deleted.",
        "data": None
    }
