from sqlalchemy.orm import Session
from backend.models import Message
from backend.gemini_client import call_gemini_json
from backend.prompts import GMAIL_TRIAGE_PROMPT
from backend.gemini_schemas import MessageTriageSchema
import json

def analyze_telegram(db: Session, sender: str, raw_text: str):
    # 1. Call Gemini for analysis
    user_prompt = f"Sender: {sender}\nMessage: {raw_text}"
    analysis_json = call_gemini_json(GMAIL_TRIAGE_PROMPT, user_prompt, MessageTriageSchema)
    
    # 2. Parse and Save
    analysis = json.loads(analysis_json)
    
    db_message = Message(
        platform="telegram",
        sender=sender,
        raw_text=raw_text,
        summary=analysis["summary"],
        category=analysis["category"],
        urgency=analysis["urgency"],
        draft_reply=analysis["draft_reply"],
        approval_required=analysis["approval_required"]
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    return db_message
