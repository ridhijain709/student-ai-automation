"""
backend/config_prod.py
Production-specific settings for the Ridhi Command Center backend.

Import via:
    from backend.config_prod import get_settings
    settings = get_settings()
"""

import logging
import os
import sys
from functools import lru_cache

from pydantic_settings import BaseSettings


class ProductionSettings(BaseSettings):
    # ── Gemini AI ────────────────────────────────────────────────────────────
    GEMINI_API_KEY: str

    # ── Database ─────────────────────────────────────────────────────────────
    # Defaults to a file-based SQLite DB inside the container.
    # Override with a Cloud SQL connection string for persistent storage.
    DATABASE_URL: str = "sqlite:////app/data/ridhi.db"

    # ── Server ports ─────────────────────────────────────────────────────────
    BACKEND_PORT: int = 8000

    # ── Application URL ──────────────────────────────────────────────────────
    APP_URL: str = ""

    # ── CORS ─────────────────────────────────────────────────────────────────
    # Comma-separated list of allowed origins.
    # Falls back to APP_URL when not explicitly set.
    ALLOWED_ORIGINS: str = ""

    # ── SQLAlchemy connection-pool settings ──────────────────────────────────
    # These settings apply to non-SQLite databases (e.g. PostgreSQL / Cloud SQL).
    # SQLite does not support connection pooling; when DATABASE_URL starts with
    # "sqlite", the application should use NullPool (handled in db setup code).
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30

    # ── Logging ──────────────────────────────────────────────────────────────
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    # ── Helpers ──────────────────────────────────────────────────────────────
    @property
    def cors_origins(self) -> list[str]:
        """Return a list of allowed CORS origins."""
        raw = self.ALLOWED_ORIGINS or self.APP_URL
        if not raw:
            return []
        return [o.strip() for o in raw.split(",") if o.strip()]

    @property
    def is_sqlite(self) -> bool:
        return self.DATABASE_URL.startswith("sqlite")


@lru_cache(maxsize=1)
def get_settings() -> ProductionSettings:
    """Return a cached singleton of the production settings."""
    return ProductionSettings()


def configure_logging(settings: ProductionSettings | None = None) -> None:
    """Configure structured logging for production."""
    if settings is None:
        settings = get_settings()

    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    logging.basicConfig(
        stream=sys.stdout,
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s – %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    # Quiet down noisy third-party loggers
    for noisy in ("uvicorn.access", "sqlalchemy.engine"):
        logging.getLogger(noisy).setLevel(logging.WARNING)
