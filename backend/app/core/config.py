"""
Core Configuration Module
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Powered Mental Health Assessment & Well-being Support Engine"
    MONGODB_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "mental_health_engine"
    
    JWT_SECRET: str = "mindcare_super_secret_jwt_key_2026_mental_health_engine"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440 # 24 hours
    
    AI_API_KEY: str = "mock_or_openai_api_key"
    GEMINI_API_KEY: str = ""  # Google Gemini API key
    
    FRONTEND_URL: str = "http://localhost:5173"
    BACKEND_URL: str = "http://localhost:8000"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
