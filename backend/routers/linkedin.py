from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.models import Contact
from backend.services import linkedin_service
from pydantic import BaseModel

router = APIRouter(prefix="/linkedin", tags=["linkedin"])

class MessageInput(BaseModel):
    sender: str
    raw_text: str

class ContactInput(BaseModel):
    name: str
    company: str
    role: str
    status: str

@router.post("/analyze-message")
def analyze(msg: MessageInput, db: Session = Depends(get_db)):
    return linkedin_service.analyze_message(db, msg.sender, msg.raw_text)

@router.post("/save-contact")
def save(contact: ContactInput, db: Session = Depends(get_db)):
    return linkedin_service.save_contact(db, contact.name, contact.company, contact.role, contact.status)

@router.get("/contacts")
def get_contacts(db: Session = Depends(get_db)):
    return db.query(Contact).filter(Contact.platform == "linkedin").all()
