from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.models import AutoResponderEvent
from backend.services import auto_responder_service

router = APIRouter(prefix="/auto-responder", tags=["auto-responder"])


class AutoResponderWebhookInput(BaseModel):
    channel: str = Field(..., min_length=2, max_length=30)
    sender: str = Field(..., min_length=2, max_length=120)
    text: str = Field(..., min_length=1, max_length=3000)
    source: str = Field(default="webhook", max_length=60)
    business_context: str | None = Field(default=None, max_length=500)
    metadata: dict | None = None


@router.post("/webhook")
def webhook(payload: AutoResponderWebhookInput, db: Session = Depends(get_db)):
    return auto_responder_service.handle_webhook(
        db,
        channel=payload.channel,
        sender=payload.sender,
        text=payload.text,
        source=payload.source,
        business_context=payload.business_context,
        metadata=payload.metadata,
    )


@router.get("/events")
def list_events(db: Session = Depends(get_db)):
    return db.query(AutoResponderEvent).order_by(AutoResponderEvent.created_at.desc()).all()
