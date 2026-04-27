from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.models import Lead
from backend.schemas_leads import LeadCreate, LeadOut
from backend.services.leads_service import create_lead

router = APIRouter(prefix="/leads", tags=["leads"])


@router.post("", response_model=LeadOut)
def create(payload: LeadCreate, db: Session = Depends(get_db)):
    lead, sheets_result = create_lead(
        db,
        name=payload.name,
        phone=payload.phone,
        email=str(payload.email) if payload.email else None,
        source=payload.source,
        message=payload.message,
        tags=payload.tags,
        sync_to_sheets=payload.sync_to_sheets,
    )

    # Keep response stable; include Sheets result via header-like field later if needed.
    # For demo, expose basic sheets status via exception only if sync requested and failed.
    if payload.sync_to_sheets and sheets_result and not sheets_result.ok:
        raise HTTPException(status_code=502, detail=f"Lead created but Sheets sync failed: {sheets_result.detail}")

    return lead


@router.get("", response_model=list[LeadOut])
def list_leads(db: Session = Depends(get_db), limit: int = 50, offset: int = 0):
    q = db.query(Lead).order_by(Lead.created_at.desc()).offset(offset).limit(min(limit, 200))
    return q.all()


@router.get("/{lead_id}", response_model=LeadOut)
def get_one(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

