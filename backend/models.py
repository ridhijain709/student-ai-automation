from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from backend.db import Base

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    platform = Column(String)
    company = Column(String)
    role = Column(String)
    status = Column(String)
    notes = Column(Text)
    last_contacted_at = Column(String)
    created_at = Column(DateTime, default=func.now())

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String)
    sender = Column(String)
    subject = Column(String)
    raw_text = Column(Text)
    summary = Column(Text)
    category = Column(String)
    urgency = Column(String)
    draft_reply = Column(Text)
    approval_required = Column(Integer, default=1)
    status = Column(String, default='pending')
    created_at = Column(DateTime, default=func.now())

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    module = Column(String)
    title = Column(String)
    description = Column(Text)
    priority = Column(String)
    due_date = Column(String)
    status = Column(String, default='open')
    created_at = Column(DateTime, default=func.now())

class ResumeVersion(Base):
    __tablename__ = "resume_versions"
    id = Column(Integer, primary_key=True, index=True)
    target_role = Column(String)
    company_name = Column(String)
    jd_text = Column(Text)
    generated_summary = Column(Text)
    generated_skills = Column(Text)
    generated_bullets = Column(Text)
    generated_cover_letter = Column(Text)
    created_at = Column(DateTime, default=func.now())

class TruthGridReport(Base):
    __tablename__ = "truthgrid_reports"
    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String)
    target_role = Column(String)
    score = Column(Integer)
    strengths = Column(Text)
    weaknesses = Column(Text)
    next_steps = Column(Text)
    full_report = Column(Text)
    created_at = Column(DateTime, default=func.now())

class WhatsAppLead(Base):
    __tablename__ = "whatsapp_leads"
    id = Column(Integer, primary_key=True, index=True)
    source_row_id = Column(String, index=True, unique=True, nullable=True)
    name = Column(String, nullable=False)
    phone = Column(String, index=True, nullable=False)
    requirement = Column(Text, nullable=True)
    source = Column(String, default="google_form")
    status = Column(String, default="new")
    follow_up_due_at = Column(DateTime, nullable=True)
    follow_up_sent_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class ContentScheduleItem(Base):
    __tablename__ = "content_schedule_items"
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    scheduled_for = Column(DateTime, nullable=False)
    status = Column(String, default="scheduled")
    ai_suggestion = Column(Text, nullable=True)
    reminder_at = Column(DateTime, nullable=True)
    reminder_sent_at = Column(DateTime, nullable=True)
    publish_reference = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class AutoResponderEvent(Base):
    __tablename__ = "auto_responder_events"
    id = Column(Integer, primary_key=True, index=True)
    channel = Column(String, index=True, nullable=False)
    sender = Column(String, nullable=False)
    incoming_text = Column(Text, nullable=False)
    reply_text = Column(Text, nullable=True)
    status = Column(String, default="processed")
    escalation_reason = Column(String, nullable=True)
    source = Column(String, default="webhook")
    metadata_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
