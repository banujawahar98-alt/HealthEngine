"""
Machine Learning Experimental Research Routes
"""
from typing import Dict, Any
from fastapi import APIRouter, Depends
from app.services.ml_service import MLResearchService
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/api/ml", tags=["ML Academic Research"])

@router.post("/predict")
async def predict_wellbeing(features: Dict[str, float], current_user: dict = Depends(get_current_user)):
    res = MLResearchService.predict_wellbeing_tier(features)
    return {
        "success": True,
        "message": "Experimental ML prediction generated.",
        "data": res
    }

@router.get("/evaluation")
async def get_model_evaluation(current_user: dict = Depends(get_current_user)):
    metrics = MLResearchService.get_model_evaluation()
    return {
        "success": True,
        "message": "Academic model evaluation metrics.",
        "data": metrics
    }
