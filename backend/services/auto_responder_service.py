from datetime import datetime, timezone
import json
from sqlalchemy.orm import Session
from backend.config import settings
from backend.gemini_client import call_gemini_json
from backend.models import AutoResponderEvent
from backend.prompts import AUTO_RESPONDER_PROMPT


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _keywords() -> list[str]:
    return [k.strip().lower() for k in settings.AUTO_RESPONDER_ESCALATION_KEYWORDS.split(",") if k.strip()]


def _allowlist() -> set[str]:
    return {c.strip().lower() for c in settings.AUTO_RESPONDER_CHANNEL_ALLOWLIST.split(",") if c.strip()}


def _should_escalate(message: str) -> str | None:
    lowered = message.lower()
    for keyword in _keywords():
        if keyword in lowered:
            return f"matched escalation keyword: {keyword}"
    return None


def _generate_reply(channel: str, sender: str, text: str, business_context: str | None):
    schema = {
        "type": "object",
        "properties": {
            "reply": {"type": "string"},
            "confidence": {"type": "string"},
            "requires_human": {"type": "boolean"},
            "reason": {"type": "string"},
        },
        "required": ["reply", "confidence", "requires_human", "reason"],
    }
    context = (business_context or settings.AUTO_RESPONDER_DEFAULT_CONTEXT).strip()
    prompt = (
        f"Business Context: {context}\n"
        f"Channel: {channel}\n"
        f"Sender: {sender}\n"
        f"Customer Message: {text}"
    )
    try:
        raw = call_gemini_json(AUTO_RESPONDER_PROMPT, prompt, schema)
        parsed = json.loads(raw)
        return parsed
    except Exception:
        return {
            "reply": "Thanks for reaching out. A team member will review this shortly and get back to you.",
            "confidence": "low",
            "requires_human": True,
            "reason": "fallback_response_due_to_model_error",
        }


def handle_webhook(
    db: Session,
    *,
    channel: str,
    sender: str,
    text: str,
    source: str = "webhook",
    business_context: str | None = None,
    metadata: dict | None = None,
):
    normalized_channel = channel.strip().lower()
    if normalized_channel not in _allowlist():
        event = AutoResponderEvent(
            channel=normalized_channel,
            sender=sender.strip(),
            incoming_text=text.strip(),
            status="ignored",
            escalation_reason="channel_not_allowlisted",
            source=source,
            metadata_json=json.dumps(metadata or {}),
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return {"event_id": event.id, "status": event.status, "reply": None}

    escalation_reason = _should_escalate(text)
    if escalation_reason:
        event = AutoResponderEvent(
            channel=normalized_channel,
            sender=sender.strip(),
            incoming_text=text.strip(),
            status="escalated",
            escalation_reason=escalation_reason,
            source=source,
            metadata_json=json.dumps(metadata or {}),
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return {"event_id": event.id, "status": event.status, "reply": None}

    ai_result = _generate_reply(normalized_channel, sender.strip(), text.strip()[:2000], business_context)
    status = "replied"
    reason = ai_result.get("reason", "")
    if ai_result.get("requires_human"):
        status = "escalated"

    event = AutoResponderEvent(
        channel=normalized_channel,
        sender=sender.strip(),
        incoming_text=text.strip(),
        reply_text=ai_result.get("reply"),
        status=status,
        escalation_reason=reason if status == "escalated" else None,
        source=source,
        metadata_json=json.dumps(metadata or {}),
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return {"event_id": event.id, "status": status, "reply": event.reply_text}
