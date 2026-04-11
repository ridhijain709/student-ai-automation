from pydantic import BaseModel
from typing import Optional

class MessageBase(BaseModel):
    platform: str
    sender: str
    subject: Optional[str] = None
    raw_text: str
    summary: Optional[str] = None
    category: Optional[str] = None
    urgency: Optional[str] = None
    draft_reply: Optional[str] = None
    approval_required: int = 1
    status: str = 'pending'

class TaskBase(BaseModel):
    module: str
    title: str
    description: str
    priority: str
    due_date: Optional[str] = None
    status: str = 'open'

class ResumeVersionBase(BaseModel):
    target_role: str
    company_name: Optional[str] = None
    jd_text: str
    generated_summary: Optional[str] = None
    generated_skills: Optional[str] = None
    generated_bullets: Optional[str] = None
    generated_cover_letter: Optional[str] = None

class TruthGridReportBase(BaseModel):
    student_name: str
    target_role: str
    score: int
    strengths: str
    weaknesses: str
    next_steps: str
    full_report: str
