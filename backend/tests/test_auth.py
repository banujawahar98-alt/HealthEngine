"""
Unit Tests for Authentication and Assessment Scoring
"""
import pytest
from app.services.scoring_service import AssessmentScoringService

def test_phq9_scoring_minimal():
    responses = {1: 0, 2: 1, 3: 0, 4: 1, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
    score, max_s, severity, interp, steps = AssessmentScoringService.calculate_score("PHQ-9", responses, [])
    assert score == 2
    assert max_s == 27
    assert "Minimal" in severity

def test_phq9_scoring_moderate():
    responses = {1: 2, 2: 2, 3: 1, 4: 2, 5: 1, 6: 1, 7: 1, 8: 1, 9: 0}
    score, max_s, severity, interp, steps = AssessmentScoringService.calculate_score("PHQ-9", responses, [])
    assert score == 11
    assert "Moderate" in severity

def test_gad7_scoring_mild():
    responses = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 0}
    score, max_s, severity, interp, steps = AssessmentScoringService.calculate_score("GAD-7", responses, [])
    assert score == 6
    assert "Mild" in severity

def test_pss10_reverse_scoring():
    # Questions 4, 5, 7, 8 are reverse scored.
    # Suppose Q4 is answered 4 (Very Often) -> reverse score is 0. Q1 is answered 3 -> score 3.
    responses = {1: 3, 2: 2, 3: 2, 4: 4, 5: 4, 6: 2, 7: 4, 8: 4, 9: 2, 10: 2}
    score, max_s, severity, interp, steps = AssessmentScoringService.calculate_score("PSS-10", responses, [])
    # 3 + 2 + 2 + (4-4=0) + (4-4=0) + 2 + (4-4=0) + (4-4=0) + 2 + 2 = 13
    assert score == 13
    assert max_s == 40
    assert "Low" in severity

def test_who5_scoring():
    responses = {1: 4, 2: 4, 3: 3, 4: 3, 5: 4} # sum = 18 raw
    score, max_s, severity, interp, steps = AssessmentScoringService.calculate_score("WHO-5", responses, [])
    assert score == 18
    assert max_s == 25
    assert "72%" in interp or "Good" in severity
