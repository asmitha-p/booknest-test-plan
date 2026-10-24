"""Central configuration. Values can be overridden with environment variables,
e.g.  BASE_URL=https://staging.example.com HEADLESS=false pytest
"""
import os

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000").rstrip("/")
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
BROWSER = os.getenv("BROWSER", "chrome").lower()          # chrome | firefox
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10"))  # seconds, explicit waits
START_MOCK_SERVER = os.getenv("START_MOCK_SERVER", "true").lower() == "true"

# Test data (never hard-code credentials inside test bodies)
VALID_USER = {"username": "testuser", "password": "Password123!"}
