from sqlalchemy.orm import Session
from backend.models import Message, Task, Contact, TruthGridReport

def get_summary(db: Session):
    return {
        "urgent_messages": db.query(Message).filter(Message.urgency == "urgent").count(),
        "pending_followups": db.query(Contact).filter(Contact.status == "waiting").count(),
        "emails_action": db.query(Message).filter(Message.platform == "gmail", Message.status == "pending").count(),
        "linkedin_waiting": db.query(Contact).filter(Contact.platform == "linkedin", Contact.status == "waiting").count(),
        "resume_tasks": db.query(Task).filter(Task.module == "resume").count(),
        "truthgrid_recent": db.query(TruthGridReport).order_by(TruthGridReport.created_at.desc()).limit(5).all(),
        "tasks_by_priority": {
            "Urgent": db.query(Task).filter(Task.priority == "urgent").all(),
            "High": db.query(Task).filter(Task.priority == "high").all(),
            "Low": db.query(Task).filter(Task.priority == "low").all()
        }
    }
