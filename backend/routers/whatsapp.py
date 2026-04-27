from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.models import Message
from backend.services import whatsapp_service
from pydantic import BaseModel
from typing import Any, Optional

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])

class WhatsAppInput(BaseModel):
    sender: str
    raw_text: str


class WhatsAppWebhookMock(BaseModel):
    """
    Simple payload for demo automation.
    This intentionally does NOT match any vendor-specific schema.
    """

    from_number: str
    text: str
    name: Optional[str] = None
    automation: Optional[str] = None  # clinic | education | fmcg
    metadata: dict[str, Any] = {}

@router.post("/incoming")
def incoming(
    msg: WhatsAppInput,
    db: Session = Depends(get_db),
    client: str | None = Query(default=None, description="Demo mode: clinic | education | fmcg"),
):
    return whatsapp_service.process_incoming(db, msg.sender, msg.raw_text, client=client)

@router.post("/webhook")
def webhook(
    payload: WhatsAppWebhookMock,
    db: Session = Depends(get_db),
    client: str | None = Query(default=None, description="Demo mode: clinic | education | fmcg"),
    business_name: str | None = Query(default=None, description="Optional override for personalization"),
    tone: str | None = Query(default=None, description="Optional override: premium | friendly | professional"),
    pricing_line: str | None = Query(default=None, description="Optional override for pricing line"),
    cta_link: str | None = Query(default=None, description="Optional override for booking link"),
):
    """
    Mock WhatsApp webhook endpoint.
    Use this in demos to simulate an inbound WhatsApp message.
    """
    sender = payload.name or payload.from_number
    vertical = payload.automation or payload.metadata.get("automation")
    return whatsapp_service.process_incoming(
        db,
        sender,
        payload.text,
        vertical=vertical,
        client=client,
        business_name=business_name,
        tone=tone,
        pricing_line=pricing_line,
        cta_link=cta_link,
    )


@router.post("/send")
def send_message(to: str, text: str):
    """
    Mock outbound send.
    In a real WhatsApp integration this would call a provider (Twilio/Meta/etc.).
    """
    return {"ok": True, "provider": "mock", "to": to, "text": text}

@router.get("/messages")
def get_messages(db: Session = Depends(get_db)):
    return db.query(Message).filter(Message.platform == "whatsapp").all()

@router.post("/draft-reply")
def draft_reply(msg_id: int, db: Session = Depends(get_db)):
    msg = db.query(Message).filter(Message.id == msg_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"draft": msg.draft_reply}
