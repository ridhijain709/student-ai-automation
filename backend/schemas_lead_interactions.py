from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class LeadInteractionOut(BaseModel):
    id: int
    client_key: str
    client_name: Optional[str] = None
    platform: str
    name: Optional[str] = None
    message: Optional[str] = None
    intent: Optional[str] = None
    followup_step: int
    followup_1: Optional[str] = None
    followup_2: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class LeadInteractionListOut(BaseModel):
    total: int = Field(..., ge=0)
    items: list[LeadInteractionOut]

