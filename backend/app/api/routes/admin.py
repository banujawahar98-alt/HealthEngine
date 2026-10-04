"""
Admin Management & Anonymized Analytics Routes
"""
from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException
from app.repositories.user_repository import UserRepository
from app.repositories.assessment_repository import AssessmentRepository
from app.repositories.resource_repository import ResourceRepository
from app.repositories.professional_repository import ProfessionalRepository
from app.repositories.crisis_repository import CrisisRepository
from app.schemas.resource import ResourceCreate, ResourceUpdate
from app.schemas.professional import ProfessionalCreate, ProfessionalUpdate
from app.schemas.crisis import CrisisResourceCreate
from app.api.dependencies import get_current_admin

router = APIRouter(prefix="/api/admin", tags=["Admin Portal"])

user_repo = UserRepository()
assessment_repo = AssessmentRepository()
resource_repo = ResourceRepository()
prof_repo = ProfessionalRepository()
crisis_repo = CrisisRepository()

@router.post("/seed")
async def trigger_seed():
    """Re-run database seeding (safe to call multiple times - uses upsert)."""
    from app.db.seed_data import seed_initial_data
    await seed_initial_data()
    return {"success": True, "message": "Database seeded successfully.", "data": None}

@router.get("/analytics")
async def get_admin_analytics(admin_user: dict = Depends(get_current_admin)):
    total_users = await user_repo.count_users()
    total_assessments = await assessment_repo.count_total_results()
    total_resources = await resource_repo.count_resources()
    total_professionals = await prof_repo.count_professionals()

    # Calculate anonymized screening severity breakdown
    db = assessment_repo.db
    cursor = db.assessment_results.find({})
    results = await cursor.to_list(length=1000)

    severity_counts: Dict[str, int] = {}
    type_counts: Dict[str, int] = {}

    for r in results:
        sev = r.get("severity_level", "Unknown")
        name = r.get("assessment_name", "Screening")
        severity_counts[sev] = severity_counts.get(sev, 0) + 1
        type_counts[name] = type_counts.get(name, 0) + 1

    return {
        "success": True,
        "message": "Aggregated admin analytics loaded.",
        "data": {
            "summary_cards": {
                "total_users": total_users,
                "total_assessments_completed": total_assessments,
                "active_resources": total_resources,
                "verified_professionals": total_professionals
            },
            "anonymized_analytics": {
                "severity_distribution": [{"severity": k, "count": v} for k, v in severity_counts.items()],
                "assessment_type_distribution": [{"type": k, "count": v} for k, v in type_counts.items()]
            }
        }
    }

# Resource CRUD
@router.post("/resources")
async def create_resource(req: ResourceCreate, admin_user: dict = Depends(get_current_admin)):
    res = await resource_repo.create_resource(req.model_dump())
    return {"success": True, "message": "Resource created.", "data": res}

@router.put("/resources/{id}")
async def update_resource(id: str, req: ResourceUpdate, admin_user: dict = Depends(get_current_admin)):
    updated = await resource_repo.update_resource(id, req.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Resource not found")
    return {"success": True, "message": "Resource updated.", "data": updated}

@router.delete("/resources/{id}")
async def delete_resource(id: str, admin_user: dict = Depends(get_current_admin)):
    success = await resource_repo.delete_resource(id)
    if not success:
        raise HTTPException(status_code=404, detail="Resource not found")
    return {"success": True, "message": "Resource deleted.", "data": None}

# Professional CRUD
@router.post("/professionals")
async def create_professional(req: ProfessionalCreate, admin_user: dict = Depends(get_current_admin)):
    prof = await prof_repo.create_professional(req.model_dump())
    return {"success": True, "message": "Professional profile created.", "data": prof}

@router.put("/professionals/{id}")
async def update_professional(id: str, req: ProfessionalUpdate, admin_user: dict = Depends(get_current_admin)):
    updated = await prof_repo.update_professional(id, req.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Professional not found")
    return {"success": True, "message": "Professional updated.", "data": updated}

@router.delete("/professionals/{id}")
async def delete_professional(id: str, admin_user: dict = Depends(get_current_admin)):
    success = await prof_repo.delete_professional(id)
    if not success:
        raise HTTPException(status_code=404, detail="Professional not found")
    return {"success": True, "message": "Professional deleted.", "data": None}

# Crisis Resource CRUD
@router.post("/crisis-resources")
async def create_crisis_resource(req: CrisisResourceCreate, admin_user: dict = Depends(get_current_admin)):
    c = await crisis_repo.create_crisis_resource(req.model_dump())
    return {"success": True, "message": "Crisis resource created.", "data": c}

@router.delete("/crisis-resources/{id}")
async def delete_crisis_resource(id: str, admin_user: dict = Depends(get_current_admin)):
    success = await crisis_repo.delete_crisis_resource(id)
    if not success:
        raise HTTPException(status_code=404, detail="Crisis resource not found")
    return {"success": True, "message": "Crisis resource deleted.", "data": None}
