from sqlalchemy.orm import Session
from backend.models import Message
from backend.gemini_client import call_gemini_json
from backend.prompts import GMAIL_TRIAGE_PROMPT
from backend.gemini_schemas import MessageTriageSchema
import json

def process_incoming(db: Session, sender: str, raw_text: str):
    user_prompt = f"Sender: {sender}\nMessage: {raw_text}"
    analysis_json = call_gemini_json(GMAIL_TRIAGE_PROMPT, user_prompt, MessageTriageSchema)
    analysis = json.loads(analysis_json)
    
    db_message = Message(
        platform="whatsapp",
        sender=sender,
        raw_text=raw_text,
        summary=analysis["summary"],
        category=analysis["category"],
        urgency=analysis["urgency"],
        draft_reply=analysis["draft_reply"],
        approval_required=True
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message
