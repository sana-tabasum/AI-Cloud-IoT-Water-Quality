"""
Unit tests for preprocessing and the water quality classifier.
Run with: pytest tests/
"""

import pandas as pd
import pytest

from src.model.water_quality_model import WaterQualityModel
from src.utils.preprocessing import label_potability, load_and_clean


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "ph": [7.0, 4.0, 9.5, 6.8],
            "turbidity": [1.0, 10.0, 0.5, 2.0],
            "tds": [200, 800, 150, 300],
        }
    )


def test_label_potability_flags_unsafe_rows(sample_df):
    labeled = label_potability(sample_df)
    assert labeled.loc[0, "potable"] == 1  # within safe ranges
    assert labeled.loc[1, "potable"] == 0  # pH too low, turbidity too high, TDS too high
    assert labeled.loc[2, "potable"] == 1  # within safe ranges
    assert labeled.loc[3, "potable"] == 1  # within safe ranges


def test_load_and_clean_removes_out_of_range_ph(tmp_path):
    csv_path = tmp_path / "test_data.csv"
    pd.DataFrame({"ph": [7.0, 20.0], "turbidity": [1.0, 2.0], "tds": [100, 200]}).to_csv(
        csv_path, index=False
    )
    df = load_and_clean(str(csv_path))
    assert df["ph"].max() <= 14


def test_model_predict_reading_returns_expected_keys(sample_df, tmp_path):
    labeled = label_potability(sample_df)
    X = labeled[["ph", "turbidity", "tds"]]
    y = labeled["potable"]

    model_path = tmp_path / "test_model.pkl"
    model = WaterQualityModel(model_path=str(model_path))
    model.fit(X, y)

    result = model.predict_reading({"ph": 7.1, "turbidity": 1.2, "tds": 210})
    assert "potable" in result
    assert "confidence" in result
    assert isinstance(result["potable"], bool)
    assert 0.0 <= result["confidence"] <= 1.0
