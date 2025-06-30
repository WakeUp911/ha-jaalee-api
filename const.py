"""Constants for the Jaalee API integration."""

DOMAIN = "jaalee_api"
PLATFORMS = ["sensor"]

# --- Configuration ---
CONF_EMAIL = "email"
CONF_TOKEN = "token"

# --- API URLs ---
API_TIMEOUT = 20
BASE_URL = "https://sensor.jaalee.com/v1/open"
GET_CODE_URL = f"{BASE_URL}/code"
LOGIN_URL = f"{BASE_URL}/login"
GET_ALL_DATA_URL = f"{BASE_URL}/data/all"

# --- Device Type Mapping ---
DEVICE_TYPE_MAP = {
    "F523": "Bluetooth temperature, humidity, pressure, ultraviolet light intensity meter, second generation",
    "F525": "Bluetooth Temperature and Humidity Monitor",
    "F526": "Bluetooth Probe Thermometer",
    "F527": "Wi-Fi Waterproof Probe Temperature and Humidity Monitor",
    "F528": "Wi-Fi CH₂O Detector",
    "F530": "Wi-Fi PM2.5 and PM10 Detectors",
    "F534": "Wi-Fi Type K Thermocouple Thermometer",
    "F535": "Wi-Fi PT100 Thermometer",
    "F536": "Wi-Fi CO₂ Detector",
    "F537": "Wi-Fi Light Intensity Meter",
    "F538": "Wi-Fi Barometer",
    "F539": "Wi-Fi Waterproof Probe Temperature and Humidity Monitor 2",
    "F53A": "Wi-Fi VOC Detector",
    "F53B": "Wi-Fi TVOC Detector",
    "F53C": "Wi-Fi O₃ detector",
    "F53D": "Wi-Fi O₃ detector",
    "F53E": "Wi-Fi Positive and Negative Pressure Gauge",
    "F53F": "Wi-Fi Pressure gauge"
}
