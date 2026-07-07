"""
Trains the water potability classifier from a CSV of historical/sample
sensor readings and saves the resulting model artifact.

Usage:
    python src/model/train.py --data data/sample_sensor_data.csv
"""

import argparse
import logging

from sklearn.metrics import classification_report, f1_score

from src.model.water_quality_model import WaterQualityModel
from src.utils.preprocessing import label_potability, load_and_clean, train_test_frames

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Train the water quality classifier.")
    parser.add_argument("--data", required=True, help="Path to CSV of sensor readings.")
    parser.add_argument("--model-out", default="src/model/water_quality_model.pkl")
    args = parser.parse_args()

    logger.info("Loading and cleaning data from %s", args.data)
    df = load_and_clean(args.data)

    if "potable" not in df.columns:
        logger.info("No 'potable' label column found — deriving labels from safe-range thresholds.")
        df = label_potability(df)

    X_train, X_test, y_train, y_test = train_test_frames(df)

    model_wrapper = WaterQualityModel(model_path=args.model_out)
    model_wrapper.fit(X_train, y_train)

    y_pred = model_wrapper.model.predict(X_test)
    logger.info("\n%s", classification_report(y_test, y_pred, target_names=["Unsafe", "Potable"]))
    logger.info("F1-score: %.4f", f1_score(y_test, y_pred))

    model_wrapper.save()


if __name__ == "__main__":
    main()
