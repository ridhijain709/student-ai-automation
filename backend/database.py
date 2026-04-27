from __future__ import annotations

import os
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./automation.db")


def _connect_args(database_url: str) -> dict:
    if database_url.startswith("sqlite"):
        return {"check_same_thread": False}
    return {}


engine = create_engine(DATABASE_URL, connect_args=_connect_args(DATABASE_URL))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    vertical = Column(String(50), nullable=False)
    sender_name = Column(String(100), default="Anonymous")
    incoming_message = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    source = Column(String(20))  # faq | gemini
    escalated = Column(Boolean, default=False)
    response_time_ms = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)


class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True)
    vertical = Column(String(50), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    hit_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class ClientConfig(Base):
    __tablename__ = "client_configs"

    id = Column(Integer, primary_key=True)
    vertical = Column(String(50), unique=True)
    client_name = Column(String(100))
    business_name = Column(String(100))
    sector = Column(String(50))
    status = Column(String(20), default="demo")  # demo | live | building
    booking_link = Column(String(200))
    contact_phone = Column(String(20))
    monthly_price = Column(Integer)
    setup_price = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

