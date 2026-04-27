import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/ridhi.db")

    # Lead capture / Sheets demo integration (mock by default)
    SHEETS_MODE: str = os.getenv("SHEETS_MODE", "mock")  # "mock" | "google"
    GOOGLE_SHEETS_SPREADSHEET_ID: str = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID", "")
    GOOGLE_SHEETS_SHEET_NAME: str = os.getenv("GOOGLE_SHEETS_SHEET_NAME", "Leads")
    GOOGLE_SERVICE_ACCOUNT_FILE: str = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "")

    class Config:
        env_file = ".env"

settings = Settings()
