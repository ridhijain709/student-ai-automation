from __future__ import annotations

from sqlalchemy.orm import Session

from backend.models import Lead
from backend.services.sheets_service import append_lead_row


def create_lead(
    db: Session,
    *,
    name: str | None,
    phone: str | None,
    email: str | None,
    source: str,
    message: str | None,
    tags: str | None,
    sync_to_sheets: bool,
):
    lead = Lead(
        name=name,
        phone=phone,
        email=email,
        source=source,
        message=message,
        tags=tags,
        status="new",
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)

    sheets_result = None
    if sync_to_sheets:
        sheets_result = append_lead_row(
            lead_id=lead.id,
            name=lead.name,
            phone=lead.phone,
            email=lead.email,
            source=lead.source,
            message=lead.message,
            tags=lead.tags,
            created_at=lead.created_at,
        )

    return lead, sheets_result

