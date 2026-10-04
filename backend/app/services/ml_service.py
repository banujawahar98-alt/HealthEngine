"""
Optional Academic Machine Learning Research Module
Provides well-being tier prediction using Scikit-Learn.
DISCLAIMER: Experimental research model for academic purposes only. Does not provide medical diagnoses.
"""
import numpy as np
from typing import Dict, Any, List
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

class MLResearchService:
    _model = None
    _is_trained = False

    @classmethod
    def _train_dummy_model(cls):
        # Generate synthetic training set representing student / adult wellness parameters
        np.random.seed(42)
        N = 500
        # Features: [sleep_hours (0-12), stress (1-5), mood (1-5), energy (1-5), physical_activity (0-5), study_hours (0-12), social_interaction (1-5)]
        sleep = np.random.uniform(4, 9, N)
        stress = np.random.randint(1, 6, N)
        mood = np.random.randint(1, 6, N)
        energy = np.random.randint(1, 6, N)
        activity = np.random.randint(0, 6, N)
        study = np.random.uniform(1, 10, N)
        social = np.random.randint(1, 6, N)

        X = np.column_stack([sleep, stress, mood, energy, activity, study, social])

        # Target: 0 = Low Risk / High Well-being, 1 = Moderate Risk, 2 = Elevated Risk
        score_idx = (stress * 2) - mood - (sleep / 2.0) - (energy / 2.0)
        y = np.where(score_idx < 1, 0, np.where(score_idx < 4, 1, 2))

        clf = RandomForestClassifier(n_estimators=50, random_state=42)
        clf.fit(X, y)
        cls._model = clf
        cls._is_trained = True

    @classmethod
    def predict_wellbeing_tier(cls, features: Dict[str, float]) -> Dict[str, Any]:
        if not cls._is_trained:
            cls._train_dummy_model()

        sleep = float(features.get("sleep_hours", 7.0))
        stress = float(features.get("stress_level", 3.0))
        mood = float(features.get("mood", 3.0))
        energy = float(features.get("energy_level", 3.0))
        activity = float(features.get("physical_activity", 2.0))
        study = float(features.get("study_hours", 4.0))
        social = float(features.get("social_interaction", 3.0))

        X_input = np.array([[sleep, stress, mood, energy, activity, study, social]])
        pred = cls._model.predict(X_input)[0]
        probs = cls._model.predict_proba(X_input)[0]

        tier_map = {
            0: "Low Risk / Balanced Well-being",
            1: "Moderate Stress Risk",
            2: "Elevated Risk - Self-Care Recommended"
        }

        return {
            "predicted_tier": tier_map.get(pred, "Moderate Risk"),
            "class_probabilities": {
                "low_risk": float(probs[0]) if len(probs) > 0 else 0.0,
                "moderate_risk": float(probs[1]) if len(probs) > 1 else 0.0,
                "elevated_risk": float(probs[2]) if len(probs) > 2 else 0.0
            },
            "disclaimer": "Experimental research model for academic purposes only. This model is not a diagnostic tool."
        }

    @classmethod
    def get_model_evaluation(cls) -> Dict[str, Any]:
        if not cls._is_trained:
            cls._train_dummy_model()

        np.random.seed(99)
        N_test = 100
        sleep = np.random.uniform(4, 9, N_test)
        stress = np.random.randint(1, 6, N_test)
        mood = np.random.randint(1, 6, N_test)
        energy = np.random.randint(1, 6, N_test)
        activity = np.random.randint(0, 6, N_test)
        study = np.random.uniform(1, 10, N_test)
        social = np.random.randint(1, 6, N_test)
        X_test = np.column_stack([sleep, stress, mood, energy, activity, study, social])

        score_idx = (stress * 2) - mood - (sleep / 2.0) - (energy / 2.0)
        y_test = np.where(score_idx < 1, 0, np.where(score_idx < 4, 1, 2))

        y_pred = cls._model.predict(X_test)

        acc = float(accuracy_score(y_test, y_pred))
        prec = float(precision_score(y_test, y_pred, average="weighted", zero_division=0))
        rec = float(recall_score(y_test, y_pred, average="weighted", zero_division=0))
        f1 = float(f1_score(y_test, y_pred, average="weighted", zero_division=0))
        cm = confusion_matrix(y_test, y_pred).tolist()

        return {
            "algorithm": "Random Forest Classifier",
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1_score": round(f1, 4),
            "confusion_matrix": cm,
            "disclaimer": "Experimental research model evaluation for academic presentation."
        }
