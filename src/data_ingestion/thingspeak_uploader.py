"""
Pushes each sensor reading to a ThingSpeak channel for live dashboarding.
ThingSpeak field mapping (adjust to match your channel):
  field1 -> pH
  field2 -> turbidity (NTU)
  field3 -> TDS (ppm)
"""

import logging

import requests

logger = logging.getLogger(__name__)


class ThingSpeakUploader:
    def __init__(self, write_api_key: str, update_url: str = "https://api.thingspeak.com/update"):
        self.write_api_key = write_api_key
        self.update_url = update_url

    def upload(self, reading: dict) -> bool:
        params = {
            "api_key": self.write_api_key,
            "field1": reading.get("ph"),
            "field2": reading.get("turbidity"),
            "field3": reading.get("tds"),
        }
        try:
            response = requests.get(self.update_url, params=params, timeout=10)
            response.raise_for_status()
            entry_id = response.text
            if entry_id == "0":
                logger.warning("ThingSpeak rejected update (rate limit or bad key).")
                return False
            logger.info("Uploaded to ThingSpeak, entry_id=%s", entry_id)
            return True
        except requests.RequestException as exc:
            logger.error("ThingSpeak upload failed: %s", exc)
            return False
