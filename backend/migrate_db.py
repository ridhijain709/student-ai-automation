"""
backend/migrate_db.py
Database initialisation / migration script for the Ridhi Command Center.

Run once on startup (or call from a Cloud Run job) to create all tables:
    python -m backend.migrate_db

The script is idempotent – it is safe to run multiple times.
"""

import logging
import os
import sys
from pathlib import Path

from sqlalchemy import create_engine, inspect, text

# Allow running the script both as a module and directly.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.models import Base  # noqa: E402 – must come after path fix

logger = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)


def get_database_url() -> str:
    """Return the database URL from the environment or fall back to the default."""
    url = os.getenv("DATABASE_URL", "sqlite:///./data/ridhi.db")
    # Ensure the directory for a file-based SQLite DB exists.
    if url.startswith("sqlite:///"):
        # sqlite:////abs/path  → 4 slashes → absolute path
        # sqlite:///./rel/path → 3 slashes + dot → relative path
        raw_path = url[len("sqlite:///"):]   # strip the scheme prefix
        db_path = Path(raw_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)
    return url


def run_migrations(database_url: str | None = None) -> None:
    """Create all tables that do not yet exist."""
    url = database_url or get_database_url()
    logger.info("Connecting to database: %s", url)

    connect_args = {}
    if url.startswith("sqlite"):
        connect_args["check_same_thread"] = False

    engine = create_engine(url, connect_args=connect_args)

    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())
    expected_tables = set(Base.metadata.tables.keys())

    missing = expected_tables - existing_tables
    if missing:
        logger.info("Creating missing tables: %s", ", ".join(sorted(missing)))
    else:
        logger.info("All tables already exist – nothing to create.")

    # create_all is idempotent; it skips tables that already exist.
    Base.metadata.create_all(bind=engine)

    # Verify
    inspector = inspect(engine)
    created = set(inspector.get_table_names())
    still_missing = expected_tables - created
    if still_missing:
        logger.error("Tables still missing after migration: %s", still_missing)
        sys.exit(1)

    logger.info("Database migration complete. Tables: %s", ", ".join(sorted(created)))

    # Quick connectivity check
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    logger.info("Database connectivity check passed.")


if __name__ == "__main__":
    run_migrations()
