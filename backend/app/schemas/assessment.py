"""
Assessment Pydantic Schemas
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class AssessmentOption(BaseModel):
    label: str
    score: int

class Question(BaseModel):
    questionId: int
    text: str
    order: int
    options: List[AssessmentOption]

class AssessmentResponse(BaseModel):
    id: str
    name: str
    description: str
    version: str
    type: str
    active: bool
    question_count: int
    questions: Optional[List[Question]] = None

class AssessmentSubmitRequest(BaseModel):
    responses: Dict[int, int] # { questionId: selectedOptionScore }
    ack_consent: bool = True

class AssessmentResultResponse(BaseModel):
    id: str
    user_id: str
    assessment_id: str
    assessment_name: str
    score: int
    max_score: int
    severity_level: str
    interpretation: str
    disclaimer: str
    suggested_next_steps: List[str]
    previous_score: Optional[int] = None
    trend_summary: Optional[str] = None
    created_at: str
