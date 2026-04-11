from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.models import Message
from backend.services import whatsapp_service
from pydantic import BaseModel

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])

class WhatsAppInput(BaseModel):
    sender: str
    raw_text: str

@router.post("/incoming")
def incoming(msg: WhatsAppInput, db: Session = Depends(get_db)):
    return whatsapp_service.process_incoming(db, msg.sender, msg.raw_text)

@router.get("/messages")
def get_messages(db: Session = Depends(get_db)):
    return db.query(Message).filter(Message.platform == "whatsapp").all()

@router.post("/draft-reply")
def draft_reply(msg_id: int, db: Session = Depends(get_db)):
    msg = db.query(Message).filter(Message.id == msg_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"draft": msg.draft_reply}
