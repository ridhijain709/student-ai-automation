from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.models import Message
from backend.services import telegram_service
from pydantic import BaseModel

router = APIRouter(prefix="/telegram", tags=["telegram"])

class TelegramInput(BaseModel):
    sender: str
    raw_text: str

@router.post("/analyze")
def analyze_telegram(msg: TelegramInput, db: Session = Depends(get_db)):
    return telegram_service.analyze_telegram(db, msg.sender, msg.raw_text)

@router.get("/messages")
def get_messages(db: Session = Depends(get_db)):
    return db.query(Message).filter(Message.platform == "telegram").all()
