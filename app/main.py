from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.logic import process_message

app = FastAPI(title="AI Automation Demo (Simple)")

class Message(BaseModel):
    name: str = Field(default="User", max_length=200)
    message: str = Field(default="", max_length=2000)
    client_type: str = Field(default="clinic", description="clinic | education | fmcg")


@app.get("/")
def home():
    return {"status": "AI Automation Running"}


@app.post("/whatsapp")
def whatsapp(msg: Message):
    return process_message(msg.name, msg.message, msg.client_type)

