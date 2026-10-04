"""
Assessment Scoring Engine Service
Deterministic scoring logic for validated mental health screening questionnaires:
- PHQ-9 (Patient Health Questionnaire)
- GAD-7 (Generalized Anxiety Disorder)
- PSS (Perceived Stress Scale)
- WHO-5 (WHO Well-Being Index)

NOTE: Screening scores are calculated ONLY deterministically by this service. LLMs NEVER calculate screening scores.
"""
from typing import Dict, Any, List, Tuple, Optional

class AssessmentScoringService:
    @staticmethod
    def calculate_score(assessment_type: str, responses: Dict[int, int], questions: List[Dict[str, Any]]) -> Tuple[int, int, str, str, List[str]]:
        """
        Returns: (score, max_score, severity_level, interpretation, suggested_next_steps)
        """
        type_clean = assessment_type.upper().strip()

        if "PHQ" in type_clean or "PHQ-9" in type_clean:
            return AssessmentScoringService._score_phq9(responses, questions)
        elif "GAD" in type_clean or "GAD-7" in type_clean:
            return AssessmentScoringService._score_gad7(responses, questions)
        elif "PSS" in type_clean:
            return AssessmentScoringService._score_pss(responses, questions)
        elif "WHO" in type_clean or "WHO-5" in type_clean:
            return AssessmentScoringService._score_who5(responses, questions)
        else:
            # Generic default accumulator
            total_score = sum(responses.values())
            max_possible = len(questions) * 3 if questions else 30
            return (
                total_score,
                max_possible,
                "Completed",
                f"Completed screening questionnaire with a score of {total_score}.",
                ["Maintain healthy daily routines", "Track your mood regularly", "Reach out to support resources if needed"]
            )

    @staticmethod
    def _score_phq9(responses: Dict[int, int], questions: List[Dict[str, Any]]) -> Tuple[int, int, str, str, List[str]]:
        # 9 questions, each scored 0 to 3. Max score 27
        score = sum(responses.values())
        max_score = 27

        if score <= 4:
            severity = "Minimal Depression Symptoms"
            interpretation = "Your responses indicate minimal or no depressive symptoms at this time."
            next_steps = [
                "Continue practicing your current healthy well-being habits.",
                "Maintain consistent sleep schedule, physical activity, and social connections.",
                "Log your daily mood to stay mindful of your emotional baseline."
            ]
        elif score <= 9:
            severity = "Mild Depression Symptoms"
            interpretation = "Your responses suggest mild depressive symptoms that may benefit from supportive well-being practices."
            next_steps = [
                "Engage in regular physical activity and daily outdoor light exposure.",
                "Practice mindfulness or deep-breathing exercises when feeling low.",
                "Connect with supportive friends or family members.",
                "Re-assess your well-being in 2 weeks."
            ]
        elif score <= 14:
            severity = "Moderate Depression Symptoms"
            interpretation = "Your responses indicate moderate depressive symptoms. Well-being support and self-care strategies are recommended."
            next_steps = [
                "Establish structured daily routines for sleep, nutrition, and rest.",
                "Try evidence-based self-help modules or mindfulness guides in our Resource Library.",
                "Consider consulting a licensed mental health professional for personalized guidance.",
                "Reach out to someone you trust about how you are feeling."
            ]
        elif score <= 19:
            severity = "Moderately Severe Depression Symptoms"
            interpretation = "Your responses indicate moderately severe depressive symptoms. Professional consultation is strongly advised."
            next_steps = [
                "Consider scheduling an appointment with a qualified healthcare or mental health professional.",
                "Utilize our 'Find Support' directory to locate local or online professionals.",
                "Inform a trusted friend, family member, or healthcare provider about your symptoms.",
                "Establish a supportive safety and routine plan."
            ]
        else:
            severity = "Severe Depression Symptoms"
            interpretation = "Your responses suggest severe depressive symptoms. Prompt professional evaluation is strongly encouraged."
            next_steps = [
                "We strongly encourage speaking with a medical or mental health professional promptly.",
                "Explore available professional support options or community helplines.",
                "If you feel overwhelmed or unsafe, access immediate crisis resources in our Crisis section."
            ]

        return score, max_score, severity, interpretation, next_steps

    @staticmethod
    def _score_gad7(responses: Dict[int, int], questions: List[Dict[str, Any]]) -> Tuple[int, int, str, str, List[str]]:
        # 7 questions, each scored 0 to 3. Max score 21
        score = sum(responses.values())
        max_score = 21

        if score <= 4:
            severity = "Minimal Anxiety Symptoms"
            interpretation = "Your responses indicate minimal or low anxiety symptoms."
            next_steps = [
                "Maintain your regular self-care and relaxation practices.",
                "Keep tracking your stress and sleep to foster ongoing resilience."
            ]
        elif score <= 9:
            severity = "Mild Anxiety Symptoms"
            interpretation = "Your responses indicate mild anxiety symptoms."
            next_steps = [
                "Practice progressive muscle relaxation or guided meditation.",
                "Limit excessive caffeine and screen time before sleep.",
                "Break large stressors into smaller, manageable steps."
            ]
        elif score <= 14:
            severity = "Moderate Anxiety Symptoms"
            interpretation = "Your responses suggest moderate anxiety symptoms that may impact your daily comfort."
            next_steps = [
                "Implement daily stress reduction techniques such as 4-7-8 breathing or grounding exercises.",
                "Review stress management articles in the Resource Library.",
                "Consider consulting a professional for guided coping strategies."
            ]
        else:
            severity = "Severe Anxiety Symptoms"
            interpretation = "Your responses indicate severe anxiety symptoms. Professional guidance is recommended."
            next_steps = [
                "Consider consulting a licensed counselor or mental health specialist.",
                "Reach out to a trusted person in your support network.",
                "Explore professional support resources in our directory."
            ]

        return score, max_score, severity, interpretation, next_steps

    @staticmethod
    def _score_pss(responses: Dict[int, int], questions: List[Dict[str, Any]]) -> Tuple[int, int, str, str, List[str]]:
        # PSS-10: 10 items, 0-4 each. Max score 40.
        # Questions 4, 5, 7, 8 are reverse-scored (0->4, 1->3, 2->2, 3->1, 4->0)
        reverse_q_ids = {4, 5, 7, 8}
        score = 0
        for q_id, val in responses.items():
            if q_id in reverse_q_ids:
                score += (4 - val)
            else:
                score += val
        max_score = 40

        if score <= 13:
            severity = "Low Perceived Stress"
            interpretation = "Your score reflects low perceived stress levels."
            next_steps = [
                "Continue maintaining a healthy balance between work, study, and rest.",
                "Keep up your current coping strategies."
            ]
        elif score <= 26:
            severity = "Moderate Perceived Stress"
            interpretation = "Your score indicates moderate perceived stress."
            next_steps = [
                "Identify specific ongoing stressors and explore time-management or task-prioritization methods.",
                "Integrate short daily breaks and relaxation practices into your routine.",
                "Utilize our mood tracking to monitor stress triggers."
            ]
        else:
            severity = "High Perceived Stress"
            interpretation = "Your score indicates high perceived stress levels."
            next_steps = [
                "Prioritize stress recovery: sleep hygiene, physical activity, and setting firm boundaries.",
                "Consider seeking support from a professional or counselor.",
                "Utilize guided relaxation modules in our Resource Library."
            ]

        return score, max_score, severity, interpretation, next_steps

    @staticmethod
    def _score_who5(responses: Dict[int, int], questions: List[Dict[str, Any]]) -> Tuple[int, int, str, str, List[str]]:
        # WHO-5: 5 items, scored 0 to 5 each. Max raw score 25. Percentage score = raw * 4 (0-100%)
        raw_score = sum(responses.values())
        max_score = 25
        percentage_score = raw_score * 4

        if percentage_score >= 50:
            severity = "Good Well-being"
            interpretation = f"Your WHO-5 well-being percentage score is {percentage_score}%, indicating good overall well-being."
            next_steps = [
                "Keep maintaining your positive daily activities and social engagements.",
                "Continue tracking your mood and sleep routine."
            ]
        else:
            severity = "Low Well-being"
            interpretation = f"Your WHO-5 well-being percentage score is {percentage_score}%, indicating reduced subjective well-being."
            next_steps = [
                "Focus on restorative practices such as sleep hygiene, physical activity, and social connection.",
                "Consider taking a depression screening (such as PHQ-9) for further insight.",
                "Explore resources on emotional well-being and stress reduction."
            ]

        return raw_score, max_score, severity, interpretation, next_steps
