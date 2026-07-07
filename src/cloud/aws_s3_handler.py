"""
Archives water-quality telemetry to AWS S3 for long-term storage and
batch analysis. Credentials are picked up from the standard AWS
credential chain (environment variables, ~/.aws/credentials, or IAM role) —
never hardcode secrets here.
"""

import json
import logging
from datetime import datetime, timezone

import boto3
from botocore.exceptions import BotoCoreError, ClientError

logger = logging.getLogger(__name__)


class S3TelemetryHandler:
    def __init__(self, bucket: str, prefix: str = "raw-readings/", region: str = "ap-south-1"):
        self.bucket = bucket
        self.prefix = prefix.rstrip("/") + "/"
        self.s3 = boto3.client("s3", region_name=region)

    def upload_reading(self, reading: dict) -> bool:
        """Uploads a single reading as a timestamped JSON object."""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
        key = f"{self.prefix}{timestamp}.json"

        try:
            self.s3.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=json.dumps(reading).encode("utf-8"),
                ContentType="application/json",
            )
            logger.info("Uploaded reading to s3://%s/%s", self.bucket, key)
            return True
        except (BotoCoreError, ClientError) as exc:
            logger.error("Failed to upload reading to S3: %s", exc)
            return False

    def list_readings(self, limit: int = 100):
        """Lists recent reading objects under the configured prefix."""
        try:
            response = self.s3.list_objects_v2(
                Bucket=self.bucket, Prefix=self.prefix, MaxKeys=limit
            )
            return [obj["Key"] for obj in response.get("Contents", [])]
        except (BotoCoreError, ClientError) as exc:
            logger.error("Failed to list S3 readings: %s", exc)
            return []
