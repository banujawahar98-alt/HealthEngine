"""
Professional Support Directory Schemas
"""
from typing import List, Optional
from pydantic import BaseModel, Field

class ProfessionalCreate(BaseModel):
    name: str = Field(..., min_length=2)
    qualification: str
    specialization: str
    experience: str
    location: str
    consultation_mode: str = Field(..., description="Online, In-Person, or Both")
    availability: str
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    bio: Optional[str] = None
    is_mock: bool = True

class ProfessionalUpdate(BaseModel):
    name: Optional[str] = None
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    experience: Optional[str] = None
    location: Optional[str] = None
    consultation_mode: Optional[str] = None
    availability: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    bio: Optional[str] = None

class ProfessionalResponse(BaseModel):
    id: str
    name: str
    qualification: str
    specialization: str
    experience: str
    location: str
    consultation_mode: str
    availability: str
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    bio: Optional[str] = None
    is_mock: bool = True
    created_at: str
