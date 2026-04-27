from __future__ import annotations

from fastapi import FastAPI

from app.ai_logic import generate_reply
from app.sheets import save_lead

app = FastAPI(title="AI Automation Demo (Simple)")


@app.get("/")
def home():
    return {"status": "AI Automation Running"}


@app.post("/whatsapp")
def whatsapp_webhook(data: dict):
    user_message = data.get("message") or ""
    user_name = data.get("name", "User") or "User"

    reply = generate_reply(user_message)
    save_lead(user_name, user_message)

    return {"reply": reply}

