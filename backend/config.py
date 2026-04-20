import os
import logging
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        logger.warning("Invalid integer value for %s. Falling back to default: %s", name, default)
        return default


@dataclass
class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/ridhi.db")
    WHATSAPP_DEFAULT_COUNTRY_CODE: str = os.getenv("WHATSAPP_DEFAULT_COUNTRY_CODE", "91")
    WHATSAPP_INITIAL_TEMPLATE: str = os.getenv(
        "WHATSAPP_INITIAL_TEMPLATE",
        "Hi {name}, thanks for contacting us. We received your requirement: {requirement}.",
    )
    WHATSAPP_FOLLOWUP_TEMPLATE: str = os.getenv(
        "WHATSAPP_FOLLOWUP_TEMPLATE",
        "Hi {name}, quick follow-up on your requirement: {requirement}. Reply here and we can help.",
    )
    WHATSAPP_FOLLOWUP_DELAY_HOURS: int = _env_int("WHATSAPP_FOLLOWUP_DELAY_HOURS", 24)
    CONTENT_REMINDER_MINUTES: int = _env_int("CONTENT_REMINDER_MINUTES", 30)
    CONTENT_SCHEDULING_TOLERANCE_MINUTES: int = _env_int("CONTENT_SCHEDULING_TOLERANCE_MINUTES", 1)
    AUTO_RESPONDER_ESCALATION_KEYWORDS: str = os.getenv(
        "AUTO_RESPONDER_ESCALATION_KEYWORDS",
        "refund,cancel,complaint,lawyer,urgent,human",
    )
    AUTO_RESPONDER_MAX_INCOMING_LENGTH: int = _env_int("AUTO_RESPONDER_MAX_INCOMING_LENGTH", 2000)
    AUTO_RESPONDER_DEFAULT_CONTEXT: str = os.getenv(
        "AUTO_RESPONDER_DEFAULT_CONTEXT",
        "You are a helpful SME support assistant. Keep replies concise and action-oriented.",
    )
    AUTO_RESPONDER_CHANNEL_ALLOWLIST: str = os.getenv(
        "AUTO_RESPONDER_CHANNEL_ALLOWLIST",
        "whatsapp,instagram,email,website",
    )

settings = Settings()
