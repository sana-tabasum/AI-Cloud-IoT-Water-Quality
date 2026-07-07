"""
Entry point: wires together MQTT ingestion, ThingSpeak live dashboarding,
AWS S3 archival, and ML-based potability inference.

Usage:
    python main.py
"""

import logging

import yaml

from src.cloud.aws_s3_handler import S3TelemetryHandler
from src.data_ingestion.mqtt_client import MQTTIngestionClient
from src.data_ingestion.thingspeak_uploader import ThingSpeakUploader
from src.model.water_quality_model import WaterQualityModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def load_config(path: str = "config/config.yaml") -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def main():
    config = load_config()

    thingspeak = ThingSpeakUploader(
        write_api_key=config["thingspeak"]["write_api_key"],
        update_url=config["thingspeak"]["update_url"],
    )
    s3_handler = S3TelemetryHandler(
        bucket=config["aws"]["s3_bucket"],
        prefix=config["aws"]["s3_prefix"],
        region=config["aws"]["region"],
    )
    model = WaterQualityModel(model_path=config["model"]["artifact_path"])

    def handle_reading(reading: dict) -> None:
        logger.info("New reading: %s", reading)
        thingspeak.upload(reading)
        s3_handler.upload_reading(reading)
        try:
            result = model.predict_reading(reading)
            status = "POTABLE ✅" if result["potable"] else "UNSAFE ⚠️"
            logger.info("Prediction: %s (confidence=%.2f)", status, result["confidence"])
        except FileNotFoundError:
            logger.warning("No trained model found yet — run src/model/train.py first.")

    client = MQTTIngestionClient(
        broker_host=config["mqtt"]["broker_host"],
        broker_port=config["mqtt"]["broker_port"],
        topic=config["mqtt"]["topic"],
        client_id=config["mqtt"]["client_id"],
        keepalive=config["mqtt"]["keepalive"],
    )
    client.register_handler(handle_reading)

    logger.info("Starting water quality monitoring pipeline...")
    client.start(blocking=True)


if __name__ == "__main__":
    main()
