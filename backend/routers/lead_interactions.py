from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.models import LeadInteraction
from backend.schemas_lead_interactions import LeadInteractionListOut, LeadInteractionOut


router = APIRouter(prefix="/lead-interactions", tags=["lead-interactions"])


@router.get("", response_model=LeadInteractionListOut)
def list_lead_interactions(
    db: Session = Depends(get_db),
    client: str | None = Query(default=None, description="Filter: clinic | education | fmcg"),
    limit: int = 50,
    offset: int = 0,
):
    q = db.query(LeadInteraction)
    if client:
        q = q.filter(LeadInteraction.client_key == client)

    total = q.count()
    items = (
        q.order_by(LeadInteraction.created_at.desc())
        .offset(offset)
        .limit(min(max(limit, 1), 200))
        .all()
    )
    return {"total": total, "items": items}


@router.get("/{interaction_id}", response_model=LeadInteractionOut)
def get_one(interaction_id: int, db: Session = Depends(get_db)):
    return db.query(LeadInteraction).filter(LeadInteraction.id == interaction_id).first()

