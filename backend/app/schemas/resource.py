"""
Resource Library Pydantic Schemas
"""
from typing import List, Optional
from pydantic import BaseModel, Field

class ResourceCreate(BaseModel):
    title: str = Field(..., min_length=2)
    description: str
    content: str
    category: str
    tags: List[str] = []
    source: Optional[str] = None
    url: Optional[str] = None

class ResourceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    source: Optional[str] = None
    url: Optional[str] = None

class ResourceResponse(BaseModel):
    id: str
    title: str
    description: str
    content: str
    category: str
    tags: List[str]
    source: Optional[str] = None
    url: Optional[str] = None
    created_at: str
