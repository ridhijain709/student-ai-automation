from pydantic import BaseModel
from typing import List

class MessageTriageSchema(BaseModel):
    category: str
    urgency: str
    summary: str
    recommended_action: str
    draft_reply: str
    approval_required: bool

class ResumeGenerationSchema(BaseModel):
    professional_summary: str
    skills: List[str]
    project_bullets: List[str]
    cover_letter_draft: str

class TruthGridReportSchema(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    next_30_day_plan: List[str]
    summary_report: str

class DashboardSummarySchema(BaseModel):
    inbox_summary: str
    urgent_tasks: List[str]
    pending_approvals: List[str]
    daily_focus: str
