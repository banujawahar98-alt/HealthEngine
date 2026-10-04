"""
User Pydantic Schemas
"""
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

class UserRegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, example="Jane Doe")
    email: str = Field(..., example="jane@example.com")
    password: str = Field(..., min_length=6, example="Password123!")
    confirm_password: str = Field(..., min_length=6, example="Password123!")
    age_range: Optional[str] = Field(None, example="25-34")
    role: Optional[str] = Field("USER", example="USER")

class UserLoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    age_range: Optional[str] = None
    created_at: str
    updated_at: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class ProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    age_range: Optional[str] = None

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=6)
