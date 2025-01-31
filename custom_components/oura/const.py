"""Constants for the Oura Ring integration."""

DOMAIN = "oura"
CONF_ACCESS_TOKEN = "access_token"
CONF_SENSORS = "sensors"  # Required to store selected sensors

# Default update interval (in seconds)
DEFAULT_SCAN_INTERVAL = 300  # 5 minutes

# Base URL for Oura API v2
API_BASE_URL = "https://api.ouraring.com/v2"

# Sensor types
SENSOR_SLEEP = "sleep_score"
SENSOR_READINESS = "readiness_score"
SENSOR_ACTIVITY = "activity_score"
SENSOR_CV_AGE = "cardiovascular_age"
SENSOR_RESILIENCE = "resilience"
SENSOR_SPO2 = "spo2"
SENSOR_STRESS = "stress"
SENSOR_HEARTRATE = "heartrate"
SENSOR_REST_MODE = "rest_mode"

# Available sensor options
SENSOR_OPTIONS = {
    SENSOR_SLEEP: "Sleep Score",
    SENSOR_READINESS: "Readiness Score",
    SENSOR_ACTIVITY: "Activity Score",
    SENSOR_CV_AGE: "Cardiovascular Age",
    SENSOR_RESILIENCE: "Resilience",
    SENSOR_SPO2: "SpO2",
    SENSOR_STRESS: "Stress",
    SENSOR_HEARTRATE: "Heart Rate",
    SENSOR_REST_MODE: "Rest Mode",
}
