"""
RAG (Retrieval-Augmented Generation) Knowledge Base Service
Searches curated mental-health knowledge base articles to provide evidence-informed context to the LLM assistant.
"""
import math
import re
from typing import List, Dict, Any
from app.repositories.resource_repository import ResourceRepository

DEFAULT_RAG_KNOWLEDGE_BASE = [
    {
        "title": "Academic & Exam Stress Management",
        "description": "Evidence-informed strategies for handling academic burnout, time management, and test anxiety.",
        "content": "Break large studying goals into 25-minute Pomodoro sessions. Practice active recall and spaced repetition. Take 5-minute movement breaks.",
        "category": "Academic Pressure",
        "tags": ["exam", "stress", "academic", "study", "burnout"]
    },
    {
        "title": "Sleep Hygiene & Circadian Health",
        "description": "Guidelines for improving sleep quality, falling asleep faster, and reducing insomnia symptoms.",
        "content": "Maintain a consistent sleep and wake schedule. Avoid blue-light screen exposure 60 minutes before bed. Keep bedroom cool and quiet.",
        "category": "Sleep",
        "tags": ["sleep", "insomnia", "bedtime", "rest", "fatigue"]
    },
    {
        "title": "5-4-3-2-1 Sensory Grounding Technique",
        "description": "Immediate somatic technique to reduce acute anxiety, panic symptoms, and emotional overwhelm.",
        "content": "Acknowledge 5 things you see around you, 4 things you can physically feel, 3 things you hear, 2 things you smell, and 1 deep conscious breath.",
        "category": "Relaxation",
        "tags": ["anxiety", "grounding", "panic", "calm", "mindfulness"]
    }
]

class RAGService:
    def __init__(self):
        self.resource_repo = ResourceRepository()

    async def retrieve_context(self, user_query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        resources = await self.resource_repo.get_all_resources()
        if not resources:
            resources = DEFAULT_RAG_KNOWLEDGE_BASE

        query_tokens = set(re.findall(r'\w+', user_query.lower()))
        if not query_tokens:
            return resources[:top_k]

        scored_resources = []
        for r in resources:
            text = f"{r.get('title', '')} {r.get('description', '')} {r.get('content', '')} {' '.join(r.get('tags', []))}".lower()
            doc_tokens = set(re.findall(r'\w+', text))
            intersection = query_tokens.intersection(doc_tokens)
            score = len(intersection)
            if score > 0:
                scored_resources.append((score, r))

        scored_resources.sort(key=lambda x: x[0], reverse=True)
        results = [item[1] for item in scored_resources[:top_k]]
        return results if results else resources[:top_k]
