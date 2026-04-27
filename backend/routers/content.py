from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.content_generator import generate_content


router = APIRouter(tags=["content"])


class GenerateContentIn(BaseModel):
    topic: str = Field(..., min_length=1, max_length=300)
    platform: str = Field(..., min_length=2, max_length=50, description="instagram | linkedin | whatsapp")


class GenerateContentOut(BaseModel):
    platform: str
    topic: str
    content: str


@router.post("/generate-content", response_model=GenerateContentOut)
def generate_content_endpoint(payload: GenerateContentIn):
    try:
        content = generate_content(topic=payload.topic, platform=payload.platform)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "platform": payload.platform,
        "topic": payload.topic,
        "content": content,
    }

