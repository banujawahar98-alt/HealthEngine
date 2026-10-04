"""
AI Assistant & RAG Pydantic Schemas
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ChatMessageRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    conversation_id: Optional[str] = None

class SafetyAnalysisResult(BaseModel):
    risk_level: str # NORMAL, DISTRESS, HIGH_RISK, IMMEDIATE_SAFETY_CONCERN
    is_crisis: bool
    safety_message: Optional[str] = None
    crisis_helplines: Optional[List[Dict[str, Any]]] = None

class ChatMessageResponse(BaseModel):
    id: str
    conversation_id: str
    role: str
    message: str
    created_at: str
    safety_analysis: Optional[SafetyAnalysisResult] = None

class ConversationResponse(BaseModel):
    id: str
    user_id: str
    title: str
    created_at: str
    updated_at: str
    message_count: int
