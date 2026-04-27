from __future__ import annotations

import json

from sqlalchemy.orm import Session

from backend.gemini_client import call_gemini_json
from backend.gemini_schemas import MessageTriageSchema
from backend.models import Message
from backend.services.leads_service import create_lead
from backend.models import LeadInteraction
from backend.services.followup_service import build_followups, should_trigger_followups
from backend.services.intent_service import detect_intent, qualification_questions
from config.client_profiles import get_client_profile
from config.rules_registry import get_vertical


def _ensure_cta(text: str, vertical_key: str) -> str:
    """
    Hard guardrail: every reply ends with a CTA question.
    (Prompts should already do this, but demos need deterministic conversion behavior.)
    """
    t = (text or "").strip()
    if not t:
        return "Thanks for reaching out—can I book a quick call/slot for you?"
    if t.endswith("?"):
        return t
    if vertical_key == "clinic":
        return f"{t}\n\nWould you like to book an appointment today or tomorrow?"
    if vertical_key == "education":
        return f"{t}\n\nWould you like to book a 15‑minute counselling call today or tomorrow?"
    if vertical_key == "fmcg":
        return f"{t}\n\nCan you share your city/area and required quantity so I can send the best quote?"
    return f"{t}\n\nWhat’s the best next step for you—should I book a quick call?"


def process_incoming(
    db: Session,
    sender: str,
    raw_text: str,
    *,
    vertical: str | None = None,
    client: str | None = None,
    business_name: str | None = None,
    tone: str | None = None,
    pricing_line: str | None = None,
    cta_link: str | None = None,
):
    profile = get_client_profile(
        client or vertical,
        business_name=business_name,
        tone=tone,
        pricing_line=pricing_line,
        cta_link=cta_link,
    )
    rules = get_vertical(vertical or profile.industry)
    intent = detect_intent(vertical=rules.key, message=raw_text)
    qualify_qs = qualification_questions(vertical=rules.key, intent=intent)

    user_prompt = (
        f"Client business: {profile.business_name}\n"
        f"Client tone: {profile.tone}\n"
        f"Pricing line: {profile.pricing_line}\n"
        f"Primary CTA link: {profile.cta_link}\n"
        f"Vertical: {rules.name} ({rules.key})\n"
        f"Detected intent (rule-based): {intent}\n"
        f"Sender: {sender}\n"
        f"Message: {raw_text}\n\n"
        f"Lead qualification questions (ask only what’s missing, pick 1–2): {', '.join(qualify_qs) if qualify_qs else 'N/A'}\n"
        f"CTA ideas (pick one if helpful): {', '.join(rules.cta_hints)}"
    )
    analysis_json = call_gemini_json(rules.whatsapp_triage_prompt, user_prompt, MessageTriageSchema)
    analysis = json.loads(analysis_json)
    
    db_message = Message(
        platform="whatsapp",
        sender=sender,
        raw_text=raw_text,
        summary=analysis["summary"],
        category=analysis["category"],
        urgency=analysis["urgency"],
        draft_reply=_ensure_cta(analysis.get("draft_reply", ""), rules.key),
        approval_required=bool(analysis.get("approval_required", True)),
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    # New structured capture for demo + multi-client.
    followup_1 = None
    followup_2 = None
    if should_trigger_followups(intent=intent, message=raw_text):
        followup_1, followup_2 = build_followups(profile=profile, intent=intent)

    interaction = LeadInteraction(
        client_key=profile.industry,
        client_name=profile.business_name,
        platform="whatsapp",
        name=sender,
        message=raw_text,
        intent=intent,
        followup_step=0,
        followup_1=followup_1,
        followup_2=followup_2,
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)

    # Keep legacy lead capture for compatibility (tags store vertical).
    create_lead(
        db,
        name=sender,
        phone=None,
        email=None,
        source="whatsapp",
        message=raw_text,
        tags=f"{rules.key},{intent}",
        sync_to_sheets=False,
    )

    # Return clean demo-friendly payload (still includes db_message fields for UI).
    return {
        "message": db_message,
        "client": {
            "key": profile.industry,
            "business_name": profile.business_name,
            "tone": profile.tone,
            "pricing_line": profile.pricing_line,
            "cta_link": profile.cta_link,
        },
        "intent": intent,
        "qualification_questions": qualify_qs,
        "draft_reply": db_message.draft_reply,
        "followups": [f for f in [followup_1, followup_2] if f],
        "lead_interaction_id": interaction.id,
    }
