"""
Assessments & Screening API Routes
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Response
from app.schemas.assessment import AssessmentSubmitRequest
from app.services.assessment_service import AssessmentService
from app.services.report_service import ReportService
from app.api.dependencies import get_current_user, get_optional_user

router = APIRouter(tags=["Assessments"])
assessment_service = AssessmentService()

@router.get("/api/assessments")
async def list_assessments(current_user: Optional[dict] = Depends(get_optional_user)):
    items = await assessment_service.list_active_assessments()
    return {
        "success": True,
        "message": "Assessments retrieved.",
        "data": items
    }

@router.get("/api/assessments/history")
async def get_assessment_history(current_user: dict = Depends(get_current_user)):
    history = await assessment_service.get_user_history(current_user["id"])
    return {
        "success": True,
        "message": "Assessment history retrieved.",
        "data": history
    }

@router.get("/api/assessments/{id}")
async def get_assessment(id: str, current_user: Optional[dict] = Depends(get_optional_user)):
    detail = await assessment_service.get_assessment_details(id)
    if not detail:
        raise HTTPException(status_code=404, detail={"success": False, "message": "Assessment not found", "error_code": "NOT_FOUND"})
    return {
        "success": True,
        "message": "Assessment loaded.",
        "data": detail
    }

@router.post("/api/assessments/{id}/submit")
async def submit_assessment(id: str, req: AssessmentSubmitRequest, current_user: dict = Depends(get_current_user)):
    try:
        result = await assessment_service.submit_assessment(
            user_id=current_user["id"],
            assessment_id=id,
            responses=req.responses
        )
        return {
            "success": True,
            "message": "Assessment completed successfully.",
            "data": result
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"success": False, "message": str(e), "error_code": "SUBMISSION_FAILED"})

@router.get("/api/assessment-results/{id}")
async def get_assessment_result(id: str, current_user: dict = Depends(get_current_user)):
    res = await assessment_service.get_result_by_id(id, current_user["id"])
    if not res:
        raise HTTPException(status_code=404, detail={"success": False, "message": "Assessment result not found", "error_code": "NOT_FOUND"})
    return {
        "success": True,
        "message": "Assessment result loaded.",
        "data": res
    }

@router.get("/api/assessment-results/{id}/pdf")
async def download_assessment_pdf(id: str, current_user: dict = Depends(get_current_user)):
    res = await assessment_service.get_result_by_id(id, current_user["id"])
    if not res:
        raise HTTPException(status_code=404, detail={"success": False, "message": "Assessment result not found", "error_code": "NOT_FOUND"})

    pdf_bytes = ReportService.generate_assessment_pdf(res, current_user["name"])
    filename = f"Mental_Health_Report_{res.get('assessment_name', 'Screening')}_{res.get('created_at')[:10]}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
