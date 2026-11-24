"""Small configuration module for the Device Service."""

import os

SERVICE_NAME = "CyberNet Device Service"
INSTANCE_ID = os.getenv("INSTANCE_ID", "device-service-1")