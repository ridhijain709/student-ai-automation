from datetime import datetime, timedelta, timezone
import re
from sqlalchemy.orm import Session
from backend.config import settings
from backend.models import Message, WhatsAppLead


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def normalize_phone(phone: str) -> str:
    digits = re.sub(r"\D", "", phone or "")
    if not digits:
        raise ValueError("Phone number is required.")
    if len(digits) == 10:
        digits = f"{settings.WHATSAPP_DEFAULT_COUNTRY_CODE}{digits}"
    if len(digits) < 11 or len(digits) > 15:
        raise ValueError("Phone number must contain 10-15 digits.")
    return f"+{digits}"


def _format_message(template: str, name: str, requirement: str) -> str:
    clean_requirement = (requirement or "your query").strip()
    return template.format(name=name.strip(), requirement=clean_requirement)


def ingest_lead(
    db: Session,
    *,
    name: str,
    phone: str,
    requirement: str,
    source: str = "google_form",
    source_row_id: str | None = None,
):
    normalized_phone = normalize_phone(phone)
    row_id = (source_row_id or "").strip() or None

    if row_id:
        existing = db.query(WhatsAppLead).filter(WhatsAppLead.source_row_id == row_id).first()
        if existing:
            return {"status": "duplicate", "lead_id": existing.id, "source_row_id": row_id}

    dedupe = (
        db.query(WhatsAppLead)
        .filter(
            WhatsAppLead.phone == normalized_phone,
            WhatsAppLead.requirement == (requirement or "").strip(),
            WhatsAppLead.status.in_(["new", "welcome_sent"]),
        )
        .first()
    )
    if dedupe:
        return {"status": "duplicate", "lead_id": dedupe.id, "source_row_id": row_id}

    lead = WhatsAppLead(
        source_row_id=row_id,
        name=name.strip(),
        phone=normalized_phone,
        requirement=(requirement or "").strip(),
        source=(source or "google_form").strip().lower(),
        status="welcome_sent",
        follow_up_due_at=_utcnow() + timedelta(hours=settings.WHATSAPP_FOLLOWUP_DELAY_HOURS),
    )
    db.add(lead)
    db.flush()

    welcome_text = _format_message(settings.WHATSAPP_INITIAL_TEMPLATE, lead.name, lead.requirement)
    db.add(
        Message(
            platform="whatsapp",
            sender=lead.phone,
            raw_text=f"[system] Lead captured from {lead.source}",
            summary="Welcome message queued",
            category="lead_followup",
            urgency="important",
            draft_reply=welcome_text,
            approval_required=0,
            status="sent",
        )
    )
    db.commit()
    db.refresh(lead)
    return {"status": "processed", "lead_id": lead.id, "phone": lead.phone}


def process_due_followups(db: Session, now: datetime | None = None):
    current = now or _utcnow()
    due_leads = (
        db.query(WhatsAppLead)
        .filter(
            WhatsAppLead.status == "welcome_sent",
            WhatsAppLead.follow_up_due_at.isnot(None),
            WhatsAppLead.follow_up_due_at <= current,
            WhatsAppLead.follow_up_sent_at.is_(None),
        )
        .all()
    )

    sent_count = 0
    failed = []
    for lead in due_leads:
        try:
            followup_text = _format_message(settings.WHATSAPP_FOLLOWUP_TEMPLATE, lead.name, lead.requirement)
            db.add(
                Message(
                    platform="whatsapp",
                    sender=lead.phone,
                    raw_text=f"[system] Follow-up for lead #{lead.id}",
                    summary="Follow-up message queued",
                    category="lead_followup",
                    urgency="important",
                    draft_reply=followup_text,
                    approval_required=0,
                    status="sent",
                )
            )
            lead.follow_up_sent_at = current
            lead.status = "followup_sent"
            lead.error_message = None
            sent_count += 1
        except Exception as exc:
            lead.status = "failed"
            lead.error_message = str(exc)
            failed.append({"lead_id": lead.id, "error": str(exc)})

    db.commit()
    return {"due": len(due_leads), "sent": sent_count, "failed": failed}
