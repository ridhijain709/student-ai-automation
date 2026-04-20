from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.models import Message, WhatsAppLead
from backend.services import whatsapp_service, whatsapp_lead_service
from pydantic import BaseModel, Field

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])

class WhatsAppInput(BaseModel):
    sender: str = Field(..., min_length=2, max_length=120)
    raw_text: str = Field(..., min_length=1, max_length=3000)


class LeadCaptureInput(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    phone: str = Field(..., min_length=7, max_length=30)
    requirement: str = Field(default="", max_length=1000)
    source: str = Field(default="google_form", max_length=60)
    source_row_id: str | None = Field(default=None, max_length=120)

@router.post("/incoming")
def incoming(msg: WhatsAppInput, db: Session = Depends(get_db)):
    return whatsapp_service.process_incoming(db, msg.sender, msg.raw_text)

@router.post("/leads")
def create_lead(payload: LeadCaptureInput, db: Session = Depends(get_db)):
    try:
        return whatsapp_lead_service.ingest_lead(
            db,
            name=payload.name,
            phone=payload.phone,
            requirement=payload.requirement,
            source=payload.source,
            source_row_id=payload.source_row_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@router.post("/followups/run")
def run_followups(db: Session = Depends(get_db)):
    return whatsapp_lead_service.process_due_followups(db)

@router.get("/leads")
def get_leads(db: Session = Depends(get_db)):
    return db.query(WhatsAppLead).order_by(WhatsAppLead.created_at.desc()).all()

@router.get("/messages")
def get_messages(db: Session = Depends(get_db)):
    return db.query(Message).filter(Message.platform == "whatsapp").all()

@router.post("/draft-reply")
def draft_reply(msg_id: int, db: Session = Depends(get_db)):
    msg = db.query(Message).filter(Message.id == msg_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"draft": msg.draft_reply}
