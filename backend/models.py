from sqlalchemy import Column, DateTime, Integer, String, Text
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


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    phone = Column(String, nullable=True, index=True)
    email = Column(String, nullable=True, index=True)
    source = Column(String, default="unknown")  # whatsapp | web | referral | unknown
    status = Column(String, default="new")  # new | contacted | qualified | lost | won
    message = Column(Text, nullable=True)
    tags = Column(String, nullable=True)  # comma-separated for demo simplicity

    created_at = Column(DateTime, default=func.now())
