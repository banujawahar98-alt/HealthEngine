"""
AI Safety & Crisis Layer Service
Analyzes incoming user messages for safety concerns:
- NORMAL: standard emotional or general mental health query
- DISTRESS: expressed mild to moderate sadness, anxiety, exam stress, fatigue
- HIGH_RISK: intense distress, feeling hopeless or overwhelmed
- IMMEDIATE_SAFETY_CONCERN: self-harm keywords, suicidal ideation, intent to harm self or others

If IMMEDIATE_SAFETY_CONCERN is detected, the standard LLM response is SUPPRESSED,
and an immediate safety message with verified crisis resources is returned.
"""
import re
from typing import Dict, Any, List, Optional
from app.repositories.crisis_repository import CrisisRepository

HIGH_RISK_KEYWORDS = [
    r"\bsuicide\b", r"\bsuicidal\b", r"\bkill myself\b", r"\bend my life\b",
    r"\bwant to die\b", r"\bself harm\b", r"\bcutting myself\b", r"\bhurt myself\b",
    r"\bno reason to live\b", r"\bcan't go on\b", r"\boverdose\b"
]

DISTRESS_KEYWORDS = [
    r"\bhopeless\b", r"\bhelpless\b", r"\bcrying all day\b", r"\bpanic attack\b",
    r"\bcant cope\b", r"\bcan't cope\b", r"\bbreakdown\b", r"\bworthless\b"
]

class SafetyService:
    def __init__(self):
        self.crisis_repo = CrisisRepository()

    async def analyze_message(self, message: str) -> Dict[str, Any]:
        text = message.lower().strip()

        # Check for immediate safety concerns
        for kw in HIGH_RISK_KEYWORDS:
            if re.search(kw, text):
                helplines = await self.crisis_repo.get_active_crisis_resources()
                return {
                    "risk_level": "IMMEDIATE_SAFETY_CONCERN",
                    "is_crisis": True,
                    "safety_message": (
                        "We are concerned about your immediate safety.\n\n"
                        "This application provides well-being screening and support only, and cannot provide emergency medical care.\n\n"
                        "If you or someone you know is in immediate danger or experiencing a life-threatening emergency, "
                        "please contact your local emergency service (e.g., 911, 112, 999), call/text the 988 Suicide & Crisis Lifeline, "
                        "or reach out immediately to a trusted person or qualified professional."
                    ),
                    "crisis_helplines": helplines
                }

        # Check for elevated distress
        for kw in DISTRESS_KEYWORDS:
            if re.search(kw, text):
                return {
                    "risk_level": "HIGH_RISK",
                    "is_crisis": False,
                    "safety_message": (
                        "It sounds like you are going through a very difficult moment. "
                        "Remember that you do not have to carry this alone. Please consider speaking with a supportive professional or trusted person."
                    ),
                    "crisis_helplines": None
                }

        return {
            "risk_level": "NORMAL",
            "is_crisis": False,
            "safety_message": None,
            "crisis_helplines": None
        }
