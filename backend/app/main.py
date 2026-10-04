"""
FastAPI Main Application Entry Point
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.db.mongodb import connect_to_mongo, close_mongo_connection
from app.db.indexes import create_db_indexes
from app.db.seed_data import seed_initial_data

from app.api.routes import (
    auth,
    users,
    assessments,
    mood,
    dashboard,
    ai,
    resources,
    professionals,
    crisis,
    admin,
    ml
)

setup_logging()
logger = logging.getLogger("mindcare.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing Mental Health Engine backend...")
    await connect_to_mongo()
    await create_db_indexes()
    await seed_initial_data()
    yield
    logger.info("Shutting down Mental Health Engine backend...")
    await close_mongo_connection()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-Powered Mental Health Screening, Assessment, Tracking, and Well-being Support Platform.",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow local React dev server and configured FRONTEND_URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(assessments.router)
app.include_router(mood.router)
app.include_router(dashboard.router)
app.include_router(ai.router)
app.include_router(resources.router)
app.include_router(professionals.router)
app.include_router(crisis.router)
app.include_router(admin.router)
app.include_router(ml.router)

# Global Exception Handler (prevents exposing raw Python stack traces)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception on %s: %s", request.url, exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "An unexpected server error occurred. Please try again later.",
            "error_code": "INTERNAL_SERVER_ERROR"
        }
    )

@app.get("/")
async def root():
    return {
        "success": True,
        "message": "AI-Powered Mental Health Assessment & Well-being Support Engine API is running.",
        "disclaimer": "This application provides screening and well-being support only. It does not diagnose mental-health conditions and does not replace professional medical care."
    }
