"""Constants for the Oura Ring integration."""
from typing import Final

DOMAIN: Final = "oura"
CONF_ACCESS_TOKEN: Final = "access_token"

# Default update interval (in seconds)
DEFAULT_SCAN_INTERVAL: Final = 300  # 5 minutes

# Base URL for Oura API v2
API_BASE_URL: Final = "https://api.ouraring.com/v2"

# Sensor types
SENSOR_SLEEP: Final = "sleep"
SENSOR_READINESS: Final = "readiness"
SENSOR_ACTIVITY: Final = "activity"
