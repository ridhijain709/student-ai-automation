from sqlalchemy.orm import Session
from backend.models import Contact
from backend.gemini_client import call_gemini_json
from backend.prompts import LINKEDIN_ASSIST_PROMPT
import json

def analyze_message(db: Session, sender: str, raw_text: str):
    user_prompt = f"Sender: {sender}\nMessage: {raw_text}"
    # Using a generic dict for now, can be replaced with a Pydantic schema
    analysis_json = call_gemini_json(LINKEDIN_ASSIST_PROMPT, user_prompt, dict)
    return json.loads(analysis_json)

def save_contact(db: Session, name: str, company: str, role: str, status: str):
    contact = Contact(name=name, platform="linkedin", company=company, role=role, status=status)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact
