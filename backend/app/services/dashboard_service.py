"""
Dashboard Service for user summary metrics and Recharts trends
"""
from typing import Dict, Any, List
from app.repositories.assessment_repository import AssessmentRepository
from app.repositories.mood_repository import MoodRepository

class DashboardService:
    def __init__(self):
        self.assessment_repo = AssessmentRepository()
        self.mood_repo = MoodRepository()

    async def get_dashboard_summary(self, user_id: str) -> Dict[str, Any]:
        results = await self.assessment_repo.get_user_results(user_id, limit=50)
        moods = await self.mood_repo.get_user_entries(user_id, limit=30)

        latest_assessment = results[0] if results else None
        latest_mood = moods[0] if moods else None

        avg_sleep = 0.0
        if moods:
            sleep_vals = [m["sleep_hours"] for m in moods if m.get("sleep_hours") is not None]
            if sleep_vals:
                avg_sleep = round(sum(sleep_vals) / len(sleep_vals), 1)

        summary_cards = {
            "latest_assessment": {
                "name": latest_assessment.get("assessment_name", "N/A") if latest_assessment else "None Taken",
                "score": latest_assessment.get("score") if latest_assessment else 0,
                "severity_level": latest_assessment.get("severity_level", "N/A") if latest_assessment else "No Data",
                "date": latest_assessment.get("created_at") if latest_assessment else None
            },
            "latest_stress_level": latest_mood.get("stress_level", 0) if latest_mood else 0,
            "current_mood": latest_mood.get("mood", 0) if latest_mood else 0,
            "average_sleep": avg_sleep,
            "assessments_completed": len(results)
        }
        return summary_cards

    async def get_dashboard_trends(self, user_id: str) -> Dict[str, Any]:
        results = await self.assessment_repo.get_user_results(user_id, limit=30)
        moods = await self.mood_repo.get_user_entries(user_id, limit=30)

        # Reverse for chronological chart display (oldest to newest)
        results_chronological = list(reversed(results))
        moods_chronological = list(reversed(moods))

        mood_trends = []
        for m in moods_chronological:
            date_str = m.get("created_at", "")[:10]
            mood_trends.append({
                "date": date_str,
                "mood": m.get("mood", 0),
                "stress_level": m.get("stress_level", 0),
                "energy_level": m.get("energy_level", 0),
                "sleep_hours": m.get("sleep_hours", 0.0),
                "note": m.get("note", "")
            })

        assessment_trends = []
        for r in results_chronological:
            date_str = r.get("created_at", "")[:10]
            assessment_trends.append({
                "date": date_str,
                "assessment_name": r.get("assessment_name", "Screening"),
                "score": r.get("score", 0),
                "max_score": r.get("max_score", 100),
                "severity_level": r.get("severity_level", "")
            })

        return {
            "mood_trends": mood_trends,
            "assessment_trends": assessment_trends
        }
