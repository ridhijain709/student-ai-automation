from __future__ import annotations

from typing import Any

from app.clients import clinic_flow, education_flow, fmcg_flow
from app.utils import save_lead

def process_message(name: str, message: str, client_type: str, *, client_name: str | None = None) -> dict[str, Any]:
    message_lower = (message or "").lower()
    ct = (client_type or "").strip().lower()

    if ct == "clinic":
        reply, intent = clinic_flow(message_lower, client_name=client_name or "TANUS Clinic")
    elif ct == "education":
        reply, intent = education_flow(message_lower, client_name=client_name or "NextStep Education")
    elif ct == "fmcg":
        reply, intent = fmcg_flow(message_lower, client_name=client_name or "Ajoyal Foods")
    else:
        reply = "Sorry, I didn’t understand your request."
        intent = "unknown"

    save_lead(name, message, intent, ct or "unknown")

    return {"reply": reply, "intent": intent, "client_type": ct}

