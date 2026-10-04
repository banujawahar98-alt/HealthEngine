"""
Assessment Management & Submission Service
"""
from typing import List, Dict, Any, Optional
from app.repositories.assessment_repository import AssessmentRepository
from app.services.scoring_service import AssessmentScoringService

DISCLAIMER_TEXT = "This application provides screening and well-being support only. It does not diagnose mental-health conditions and does not replace professional medical care."

class AssessmentService:
    def __init__(self):
        self.assessment_repo = AssessmentRepository()

    async def list_active_assessments(self) -> List[Dict[str, Any]]:
        assessments = await self.assessment_repo.get_active_assessments()
        res = []
        for a in assessments:
            res.append({
                "id": str(a["_id"]),
                "name": a.get("name", ""),
                "description": a.get("description", ""),
                "version": a.get("version", "1.0"),
                "type": a.get("type", "screening"),
                "active": a.get("active", True),
                "question_count": len(a.get("questions", [])),
                "questions": a.get("questions", [])
            })
        return res

    async def get_assessment_details(self, assessment_id: str) -> Optional[Dict[str, Any]]:
        a = await self.assessment_repo.get_assessment_by_id(assessment_id)
        if not a:
            return None
        return {
            "id": str(a["_id"]),
            "name": a.get("name", ""),
            "description": a.get("description", ""),
            "version": a.get("version", "1.0"),
            "type": a.get("type", "screening"),
            "active": a.get("active", True),
            "question_count": len(a.get("questions", [])),
            "questions": a.get("questions", [])
        }

    async def submit_assessment(self, user_id: str, assessment_id: str, responses: Dict[int, int]) -> Dict[str, Any]:
        assessment = await self.assessment_repo.get_assessment_by_id(assessment_id)
        if not assessment:
            raise ValueError(f"Assessment ID '{assessment_id}' not found.")

        questions = assessment.get("questions", [])
        question_ids = {q["questionId"] for q in questions}

        # Validate that all questions are answered
        for qid in question_ids:
            if qid not in responses:
                raise ValueError(f"Missing answer for question #{qid}.")

        # 1. Deterministic score calculation
        score, max_score, severity, interpretation, next_steps = AssessmentScoringService.calculate_score(
            assessment_type=assessment.get("name", ""),
            responses=responses,
            questions=questions
        )

        # 2. Record Attempt
        attempt_doc = {
            "user_id": user_id,
            "assessment_id": str(assessment["_id"]),
            "assessment_name": assessment.get("name", ""),
            "responses": {str(k): v for k, v in responses.items()}
        }
        saved_attempt = await self.assessment_repo.save_attempt(attempt_doc)

        # 3. Check for previous result to compute neutral comparison
        latest_prev = await self.assessment_repo.get_latest_user_result(user_id, str(assessment["_id"]))
        previous_score = latest_prev.get("score") if latest_prev else None
        
        trend_summary = None
        if previous_score is not None:
            if score < previous_score:
                trend_summary = f"Your reported score has decreased compared with your previous screening ({previous_score} vs {score})."
            elif score > previous_score:
                trend_summary = f"Your reported score has increased compared with your previous screening ({previous_score} vs {score})."
            else:
                trend_summary = f"Your reported score remains identical to your previous screening ({score})."

        # 4. Save Result
        result_doc = {
            "user_id": user_id,
            "attempt_id": saved_attempt["_id"],
            "assessment_id": str(assessment["_id"]),
            "assessment_name": assessment.get("name", ""),
            "score": score,
            "max_score": max_score,
            "severity_level": severity,
            "interpretation": interpretation,
            "disclaimer": DISCLAIMER_TEXT,
            "suggested_next_steps": next_steps,
            "previous_score": previous_score,
            "trend_summary": trend_summary
        }
        saved_result = await self.assessment_repo.save_result(result_doc)

        return {
            "id": saved_result["_id"],
            "user_id": user_id,
            "assessment_id": str(assessment["_id"]),
            "assessment_name": assessment.get("name", ""),
            "score": score,
            "max_score": max_score,
            "severity_level": severity,
            "interpretation": interpretation,
            "disclaimer": DISCLAIMER_TEXT,
            "suggested_next_steps": next_steps,
            "previous_score": previous_score,
            "trend_summary": trend_summary,
            "created_at": saved_result["created_at"]
        }

    async def get_user_history(self, user_id: str) -> List[Dict[str, Any]]:
        results = await self.assessment_repo.get_user_results(user_id)
        out = []
        for r in results:
            out.append({
                "id": str(r["_id"]),
                "user_id": r["user_id"],
                "assessment_id": r.get("assessment_id", ""),
                "assessment_name": r.get("assessment_name", ""),
                "score": r.get("score", 0),
                "max_score": r.get("max_score", 0),
                "severity_level": r.get("severity_level", ""),
                "interpretation": r.get("interpretation", ""),
                "disclaimer": r.get("disclaimer", DISCLAIMER_TEXT),
                "suggested_next_steps": r.get("suggested_next_steps", []),
                "previous_score": r.get("previous_score"),
                "trend_summary": r.get("trend_summary"),
                "created_at": r.get("created_at", "")
            })
        return out

    async def get_result_by_id(self, result_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        r = await self.assessment_repo.get_result_by_id(result_id)
        if not r or r.get("user_id") != user_id:
            return None
        return {
            "id": str(r["_id"]),
            "user_id": r["user_id"],
            "assessment_id": r.get("assessment_id", ""),
            "assessment_name": r.get("assessment_name", ""),
            "score": r.get("score", 0),
            "max_score": r.get("max_score", 0),
            "severity_level": r.get("severity_level", ""),
            "interpretation": r.get("interpretation", ""),
            "disclaimer": r.get("disclaimer", DISCLAIMER_TEXT),
            "suggested_next_steps": r.get("suggested_next_steps", []),
            "previous_score": r.get("previous_score"),
            "trend_summary": r.get("trend_summary"),
            "created_at": r.get("created_at", "")
        }
