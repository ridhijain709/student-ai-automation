from datetime import datetime, timedelta, timezone
import json
from sqlalchemy.orm import Session
from backend.config import settings
from backend.gemini_client import call_gemini_json
from backend.models import ContentScheduleItem
from backend.prompts import CONTENT_SCHEDULER_SUGGESTION_PROMPT

SUPPORTED_PLATFORMS = {"instagram", "linkedin", "facebook", "x", "youtube"}


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def parse_datetime(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("scheduled_for must be ISO format, e.g. 2026-05-01T10:00:00Z") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _generate_ai_suggestion(platform: str, title: str, content: str, brief: str | None):
    prompt = (
        f"Platform: {platform}\n"
        f"Title: {title}\n"
        f"Content: {content}\n"
        f"Brief: {(brief or 'N/A').strip()}"
    )
    schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "content": {"type": "string"},
            "channel_tips": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["title", "content", "channel_tips"],
    }
    try:
        raw = call_gemini_json(CONTENT_SCHEDULER_SUGGESTION_PROMPT, prompt, schema)
        parsed = json.loads(raw)
        tips = ", ".join(parsed.get("channel_tips", []))
        return f"Title: {parsed.get('title', title)}\nContent: {parsed.get('content', content)}\nTips: {tips}".strip()
    except Exception:
        return f"Suggested CTA: add one clear action line for {platform} and keep it under 2 short paragraphs."


def create_schedule_item(
    db: Session,
    *,
    platform: str,
    title: str,
    content: str,
    scheduled_for: str,
    generate_ai_suggestion: bool = False,
    brief: str | None = None,
):
    normalized_platform = platform.strip().lower()
    if normalized_platform not in SUPPORTED_PLATFORMS:
        raise ValueError(f"Unsupported platform '{platform}'. Supported: {', '.join(sorted(SUPPORTED_PLATFORMS))}")

    scheduled_dt = parse_datetime(scheduled_for)
    if scheduled_dt < _utcnow() - timedelta(minutes=settings.CONTENT_SCHEDULING_TOLERANCE_MINUTES):
        raise ValueError(
            f"scheduled_for cannot be more than {settings.CONTENT_SCHEDULING_TOLERANCE_MINUTES} minutes in the past."
        )

    reminder_at = scheduled_dt - timedelta(minutes=settings.CONTENT_REMINDER_MINUTES)
    ai_suggestion = None
    if generate_ai_suggestion:
        ai_suggestion = _generate_ai_suggestion(normalized_platform, title, content, brief)

    item = ContentScheduleItem(
        platform=normalized_platform,
        title=title.strip(),
        content=content.strip(),
        scheduled_for=scheduled_dt,
        reminder_at=reminder_at,
        ai_suggestion=ai_suggestion,
        status="scheduled",
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def mark_published(db: Session, *, item: ContentScheduleItem, publish_reference: str | None = None):
    item.status = "published"
    item.publish_reference = (publish_reference or "").strip() or None
    item.error_message = None
    db.commit()
    db.refresh(item)
    return item


def run_due_reminders(db: Session, now: datetime | None = None):
    current = now or _utcnow()
    due = (
        db.query(ContentScheduleItem)
        .filter(
            ContentScheduleItem.status == "scheduled",
            ContentScheduleItem.reminder_at.isnot(None),
            ContentScheduleItem.reminder_at <= current,
            ContentScheduleItem.reminder_sent_at.is_(None),
            ContentScheduleItem.scheduled_for >= current,
        )
        .all()
    )
    for item in due:
        item.reminder_sent_at = current
        item.status = "reminded"
    db.commit()
    return {"due": len(due), "items": [item.id for item in due]}
