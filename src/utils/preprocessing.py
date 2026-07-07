"""
Cleaning, feature engineering, and rule-based labeling utilities for
water-quality sensor data.
"""

import pandas as pd

FEATURE_COLUMNS = ["ph", "turbidity", "tds"]


def load_and_clean(csv_path: str) -> pd.DataFrame:
    """Loads sensor data from CSV, drops nulls/duplicates, and clips
    values to physically plausible ranges.
    """
    df = pd.read_csv(csv_path)
    df = df.dropna(subset=FEATURE_COLUMNS).drop_duplicates()

    df["ph"] = df["ph"].clip(0, 14)
    df["turbidity"] = df["turbidity"].clip(lower=0)
    df["tds"] = df["tds"].clip(lower=0)

    return df.reset_index(drop=True)


def label_potability(df: pd.DataFrame, ph_min: float = 6.5, ph_max: float = 8.5,
                      turbidity_max: float = 5.0, tds_max: float = 500.0) -> pd.DataFrame:
    """Adds a binary 'potable' column using WHO-style safe-range thresholds.
    Useful for bootstrapping labels when historical ground truth isn't available.
    """
    df = df.copy()
    df["potable"] = (
        df["ph"].between(ph_min, ph_max)
        & (df["turbidity"] <= turbidity_max)
        & (df["tds"] <= tds_max)
    ).astype(int)
    return df


def train_test_frames(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42):
    from sklearn.model_selection import train_test_split

    X = df[FEATURE_COLUMNS]
    y = df["potable"]
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)
