"""
Mood Tracking Pydantic Schemas
"""
from typing import Optional
from pydantic import BaseModel, Field

class MoodEntryCreate(BaseModel):
    mood: int = Field(..., ge=1, le=5, description="1 - Very Low to 5 - Very Good")
    stress_level: int = Field(..., ge=1, le=5, description="1 - Very Low to 5 - Very High")
    energy_level: int = Field(..., ge=1, le=5, description="1 - Very Low to 5 - Very High")
    sleep_hours: float = Field(..., ge=0, le=24, description="Hours slept")
    note: Optional[str] = Field(None, max_length=500, description="Optional daily note")

class MoodEntryUpdate(BaseModel):
    mood: Optional[int] = Field(None, ge=1, le=5)
    stress_level: Optional[int] = Field(None, ge=1, le=5)
    energy_level: Optional[int] = Field(None, ge=1, le=5)
    sleep_hours: Optional[float] = Field(None, ge=0, le=24)
    note: Optional[str] = None

class MoodEntryResponse(BaseModel):
    id: str
    user_id: str
    mood: int
    stress_level: int
    energy_level: int
    sleep_hours: float
    note: Optional[str] = None
    created_at: str
