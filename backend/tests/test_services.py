"""
Comprehensive Unit Tests for Services and Scoring Engine
"""
import pytest
import asyncio
from app.services.scoring_service import AssessmentScoringService
from app.services.safety_service import SafetyService
from app.services.ml_service import MLResearchService
from app.services.report_service import ReportService
from app.services.rag_service import RAGService

def test_phq9_scoring_minimal():
    responses = {1: 0, 2: 1, 3: 0, 4: 1, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
    score, max_s, severity, interp, steps = AssessmentScoringService.calculate_score("PHQ-9", responses, [])
    assert score == 2
    assert max_s == 27
    assert "Minimal" in severity

def test_phq9_scoring_severe():
    responses = {1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3, 7: 3, 8: 3, 9: 3}
    score, max_s, severity, interp, steps = AssessmentScoringService.calculate_score("PHQ-9", responses, [])
    assert score == 27
    assert max_s == 27
    assert "Severe" in severity

def test_gad7_scoring():
    responses = {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2}
    score, max_s, severity, interp, steps = AssessmentScoringService.calculate_score("GAD-7", responses, [])
    assert score == 14
    assert max_s == 21
    assert "Moderate" in severity

def test_pss10_scoring():
    responses = {1: 2, 2: 2, 3: 2, 4: 4, 5: 4, 6: 2, 7: 4, 8: 4, 9: 2, 10: 2}
    score, max_s, severity, interp, steps = AssessmentScoringService.calculate_score("PSS-10", responses, [])
    assert score == 12
    assert max_s == 40
    assert "Low" in severity

def test_who5_scoring():
    responses = {1: 5, 2: 5, 3: 5, 4: 5, 5: 5}
    score, max_s, severity, interp, steps = AssessmentScoringService.calculate_score("WHO-5", responses, [])
    assert score == 25
    assert max_s == 25
    assert "High" in severity or "Good" in severity

def test_safety_service_normal():
    safety = SafetyService()
    res = asyncio.run(safety.analyze_message("How can I improve my study routine?"))
    assert res["risk_level"] == "NORMAL"
    assert res["is_crisis"] is False
    assert res["safety_message"] is None

def test_safety_service_high_risk_distress():
    safety = SafetyService()
    res = asyncio.run(safety.analyze_message("I am feeling hopeless and crying all day"))
    assert res["risk_level"] == "HIGH_RISK"
    assert res["is_crisis"] is False

def test_safety_service_crisis():
    safety = SafetyService()
    res = asyncio.run(safety.analyze_message("I want to end my life and hurt myself"))
    assert res["risk_level"] == "IMMEDIATE_SAFETY_CONCERN"
    assert res["is_crisis"] is True
    assert "immediate safety" in res["safety_message"].lower()

def test_ml_research_service_predict():
    features = {
        "sleep_hours": 7.5,
        "stress_level": 2.0,
        "mood": 4.0,
        "energy_level": 4.0,
        "physical_activity": 3.0,
        "study_hours": 5.0,
        "social_interaction": 4.0
    }
    pred = MLResearchService.predict_wellbeing_tier(features)
    assert "predicted_tier" in pred
    assert "class_probabilities" in pred
    assert "disclaimer" in pred

def test_ml_research_service_evaluation():
    eval_res = MLResearchService.get_model_evaluation()
    assert eval_res["algorithm"] == "Random Forest Classifier"
    assert "accuracy" in eval_res
    assert "f1_score" in eval_res
    assert isinstance(eval_res["confusion_matrix"], list)

def test_report_service_pdf_generation():
    result_data = {
        "assessment_name": "PHQ-9",
        "created_at": "2026-10-04T12:00:00",
        "score": 8,
        "max_score": 27,
        "severity_level": "Mild Depressive Symptoms",
        "interpretation": "Your score falls in the mild range.",
        "previous_score": 10,
        "trend_summary": "Your score decreased from 10 to 8.",
        "suggested_next_steps": ["Maintain regular sleep routine", "Engage in light physical exercise"]
    }
    pdf_bytes = ReportService.generate_assessment_pdf(result_data, "John Doe")
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 500
    assert pdf_bytes.startswith(b"%PDF")

def test_rag_service_retrieve():
    rag = RAGService()
    docs = asyncio.run(rag.retrieve_context("exam stress and study tips", top_k=2))
    assert len(docs) > 0
    assert "content" in docs[0]
