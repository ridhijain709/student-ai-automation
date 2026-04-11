from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.models import Message
from backend.services import gmail_service
from pydantic import BaseModel

router = APIRouter(prefix="/gmail", tags=["gmail"])

class EmailInput(BaseModel):
    sender: str
    subject: str
    raw_text: str

@router.post("/analyze")
def analyze_email(email: EmailInput, db: Session = Depends(get_db)):
    return gmail_service.analyze_email(db, email.sender, email.subject, email.raw_text)

@router.get("/messages")
def get_messages(db: Session = Depends(get_db)):
    return db.query(Message).filter(Message.platform == "gmail").all()

@router.post("/draft-reply")
def draft_reply(email_id: int, db: Session = Depends(get_db)):
    # Logic to return draft reply
    message = db.query(Message).filter(Message.id == email_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"draft": message.draft_reply}
