from sqlalchemy.orm import Session
from backend.models import Message, Task
from backend.gemini_client import call_gemini_json
from backend.prompts import GMAIL_TRIAGE_PROMPT
from backend.gemini_schemas import MessageTriageSchema

def analyze_email(db: Session, sender: str, subject: str, raw_text: str):
    # 1. Call Gemini for analysis
    user_prompt = f"Sender: {sender}\nSubject: {subject}\nBody: {raw_text}"
    analysis_json = call_gemini_json(GMAIL_TRIAGE_PROMPT, user_prompt, MessageTriageSchema)
    
    # 2. Parse and Save
    import json
    analysis = json.loads(analysis_json)
    
    db_message = Message(
        platform="gmail",
        sender=sender,
        subject=subject,
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
    
    # 3. Create task if urgent
    if analysis["urgency"] == "urgent":
        db_task = Task(
            module="gmail",
            title=f"Urgent: {subject}",
            description=analysis["recommended_action"],
            priority="high"
        )
        db.add(db_task)
        db.commit()
        
    return db_message
