import os
from dataclasses import dataclass

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
    WHATSAPP_FOLLOWUP_DELAY_HOURS: int = int(os.getenv("WHATSAPP_FOLLOWUP_DELAY_HOURS", "24"))
    CONTENT_REMINDER_MINUTES: int = int(os.getenv("CONTENT_REMINDER_MINUTES", "30"))
    AUTO_RESPONDER_ESCALATION_KEYWORDS: str = os.getenv(
        "AUTO_RESPONDER_ESCALATION_KEYWORDS",
        "refund,cancel,complaint,lawyer,urgent,human",
    )
    AUTO_RESPONDER_DEFAULT_CONTEXT: str = os.getenv(
        "AUTO_RESPONDER_DEFAULT_CONTEXT",
        "You are a helpful SME support assistant. Keep replies concise and action-oriented.",
    )
    AUTO_RESPONDER_CHANNEL_ALLOWLIST: str = os.getenv(
        "AUTO_RESPONDER_CHANNEL_ALLOWLIST",
        "whatsapp,instagram,email,website",
    )

settings = Settings()
