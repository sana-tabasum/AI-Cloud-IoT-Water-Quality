"""
MQTT subscriber that listens for sensor telemetry published by the
ESP32/Arduino node (see hardware/sensor_reader.ino) and forwards each
reading to registered downstream handlers (ThingSpeak, AWS S3, ML model).
"""

import json
import logging
from typing import Callable, List

import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)


class MQTTIngestionClient:
    """Subscribes to a water-quality telemetry topic and dispatches
    each parsed reading to a list of callback handlers.
    """

    def __init__(self, broker_host: str, broker_port: int, topic: str,
                 client_id: str = "water-quality-subscriber", keepalive: int = 60):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.topic = topic
        self.keepalive = keepalive
        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self._handlers: List[Callable[[dict], None]] = []

    def register_handler(self, handler: Callable[[dict], None]) -> None:
        """Register a callback invoked with each parsed reading (dict)."""
        self._handlers.append(handler)

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to MQTT broker %s:%s", self.broker_host, self.broker_port)
            client.subscribe(self.topic)
            logger.info("Subscribed to topic: %s", self.topic)
        else:
            logger.error("MQTT connection failed with code %s", rc)

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            logger.warning("Skipping malformed message on %s: %s", msg.topic, exc)
            return

        if not self._validate_reading(payload):
            logger.warning("Skipping reading with missing fields: %s", payload)
            return

        for handler in self._handlers:
            try:
                handler(payload)
            except Exception:  # noqa: BLE001 - keep the loop alive even if one handler fails
                logger.exception("Handler failed while processing reading: %s", payload)

    @staticmethod
    def _validate_reading(payload: dict) -> bool:
        required_fields = {"ph", "turbidity", "tds"}
        return required_fields.issubset(payload.keys())

    def start(self, blocking: bool = True) -> None:
        self.client.connect(self.broker_host, self.broker_port, self.keepalive)
        if blocking:
            self.client.loop_forever()
        else:
            self.client.loop_start()

    def stop(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()
