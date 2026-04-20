from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.models import ContentScheduleItem
from backend.services import content_scheduler_service

router = APIRouter(prefix="/content-scheduler", tags=["content-scheduler"])


class ScheduleItemInput(BaseModel):
    platform: str = Field(..., min_length=2, max_length=30)
    title: str = Field(..., min_length=3, max_length=150)
    content: str = Field(..., min_length=5, max_length=3000)
    scheduled_for: str
    generate_ai_suggestion: bool = False
    brief: str | None = Field(default=None, max_length=500)


class PublishInput(BaseModel):
    publish_reference: str | None = Field(default=None, max_length=500)


@router.post("/items")
def create_item(payload: ScheduleItemInput, db: Session = Depends(get_db)):
    try:
        return content_scheduler_service.create_schedule_item(
            db,
            platform=payload.platform,
            title=payload.title,
            content=payload.content,
            scheduled_for=payload.scheduled_for,
            generate_ai_suggestion=payload.generate_ai_suggestion,
            brief=payload.brief,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/items")
def list_items(
    status: str | None = Query(default=None),
    platform: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(ContentScheduleItem)
    if status:
        query = query.filter(ContentScheduleItem.status == status.strip().lower())
    if platform:
        query = query.filter(ContentScheduleItem.platform == platform.strip().lower())
    return query.order_by(ContentScheduleItem.scheduled_for.asc()).all()


@router.post("/items/{item_id}/publish")
def publish_item(item_id: int, payload: PublishInput, db: Session = Depends(get_db)):
    item = db.query(ContentScheduleItem).filter(ContentScheduleItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Scheduled item not found")
    return content_scheduler_service.mark_published(
        db, item=item, publish_reference=payload.publish_reference
    )


@router.post("/reminders/run")
def run_reminders(now: str | None = None, db: Session = Depends(get_db)):
    parsed_now = None
    if now:
        try:
            parsed_now = content_scheduler_service.parse_datetime(now)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
    return content_scheduler_service.run_due_reminders(db, now=parsed_now)
