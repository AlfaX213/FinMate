import os
from dotenv import load_dotenv  # type: ignore

load_dotenv()

APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8000"))

WAHA_BASE_URL = os.getenv("WAHA_BASE_URL", "http://127.0.0.1:3000")
WAHA_SESSION = os.getenv("WAHA_SESSION", "default")

GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "FinMate Data")
GOOGLE_CREDENTIALS_PATH = os.getenv(
    "GOOGLE_CREDENTIALS_PATH",
    "credentials/google-service-account.json"
    )
GOOGLE_WORKSHEET_NAME = os.getenv("GOOGLE_WORKSHEET_NAME", "Transactions")