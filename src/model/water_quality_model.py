"""
Water potability classifier: wraps a Scikit-learn RandomForestClassifier
trained on pH, turbidity, and TDS readings.
"""

import logging
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

logger = logging.getLogger(__name__)

FEATURE_COLUMNS = ["ph", "turbidity", "tds"]


class WaterQualityModel:
    def __init__(self, model_path: str = "src/model/water_quality_model.pkl"):
        self.model_path = Path(model_path)
        self.model: RandomForestClassifier | None = None

    def build(self, n_estimators: int = 200, random_state: int = 42) -> RandomForestClassifier:
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=8,
            random_state=random_state,
            class_weight="balanced",
        )
        return self.model

    def fit(self, X, y):
        if self.model is None:
            self.build()
        self.model.fit(X, y)
        return self.model

    def save(self):
        if self.model is None:
            raise RuntimeError("No trained model to save. Call fit() first.")
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, self.model_path)
        logger.info("Model saved to %s", self.model_path)

    def load(self):
        if not self.model_path.exists():
            raise FileNotFoundError(f"No model artifact at {self.model_path}")
        self.model = joblib.load(self.model_path)
        logger.info("Model loaded from %s", self.model_path)
        return self.model

    def predict_reading(self, reading: dict) -> dict:
        """Runs inference on a single sensor reading dict, e.g.
        {"ph": 7.1, "turbidity": 2.3, "tds": 210}
        """
        if self.model is None:
            self.load()

        row = pd.DataFrame([{col: reading.get(col) for col in FEATURE_COLUMNS}])
        prediction = self.model.predict(row)[0]
        probability = self.model.predict_proba(row)[0][1]

        return {
            "potable": bool(prediction),
            "confidence": round(float(probability), 4),
        }
