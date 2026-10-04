"""
Well-being Dashboard API Routes
"""
from fastapi import APIRouter, Depends
from app.services.dashboard_service import DashboardService
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])
dash_service = DashboardService()

@router.get("/summary")
async def get_dashboard_summary(current_user: dict = Depends(get_current_user)):
    summary = await dash_service.get_dashboard_summary(current_user["id"])
    return {
        "success": True,
        "message": "Dashboard summary retrieved.",
        "data": summary
    }

@router.get("/trends")
async def get_dashboard_trends(current_user: dict = Depends(get_current_user)):
    trends = await dash_service.get_dashboard_trends(current_user["id"])
    return {
        "success": True,
        "message": "Dashboard trends loaded.",
        "data": trends
    }
