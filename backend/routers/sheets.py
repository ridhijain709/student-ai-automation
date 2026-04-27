from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.config import settings
from backend.db import get_db
from backend.models import Lead
from backend.services.sheets_service import append_lead_row

router = APIRouter(prefix="/sheets", tags=["sheets"])


@router.get("/status")
def status():
    return {
        "mode": settings.SHEETS_MODE,
        "spreadsheet_id_set": bool(settings.GOOGLE_SHEETS_SPREADSHEET_ID),
        "sheet_name": settings.GOOGLE_SHEETS_SHEET_NAME,
    }


@router.post("/sync/lead/{lead_id}")
def sync_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    result = append_lead_row(
        lead_id=lead.id,
        name=lead.name,
        phone=lead.phone,
        email=lead.email,
        source=lead.source,
        message=lead.message,
        tags=lead.tags,
        created_at=lead.created_at,
    )
    if not result.ok:
        raise HTTPException(status_code=502, detail=result.detail)
    return {"ok": True, "mode": result.mode, "detail": result.detail}

