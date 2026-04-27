from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class LeadCreate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=200)
    phone: Optional[str] = Field(default=None, max_length=50)
    email: Optional[EmailStr] = None
    source: str = Field(default="unknown", max_length=50)
    message: Optional[str] = None
    tags: Optional[str] = Field(default=None, description="Comma-separated tags")
    sync_to_sheets: bool = Field(default=True, description="If true, attempt Sheets sync after create")


class LeadOut(BaseModel):
    id: int
    name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    source: str
    status: str
    message: Optional[str]
    tags: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

