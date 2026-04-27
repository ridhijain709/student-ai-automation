from fastapi import FastAPI
from fastapi import Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.db import engine, Base
from backend.database import (
    Conversation,
    FAQ,
    get_db as get_portfolio_db,
    init_db as init_portfolio_db,
)
from backend.response_engine import ResponseEngine
from backend.routers import (
    content,
    dashboard,
    gmail,
    lead_interactions,
    leads,
    linkedin,
    resume,
    sheets,
    telegram,
    truthgrid,
    whatsapp,
)

# Initialize database tables on startup
def init_db():
    Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ridhi Command Center API")

# CORS setup for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def _startup():
    init_db()
    init_portfolio_db()

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Register routers
app.include_router(gmail.router)
app.include_router(telegram.router)
app.include_router(linkedin.router)
app.include_router(whatsapp.router)
app.include_router(resume.router)
app.include_router(truthgrid.router)
app.include_router(dashboard.router)
app.include_router(leads.router)
app.include_router(sheets.router)
app.include_router(content.router)
app.include_router(lead_interactions.router)


# ------------------------------
# Portfolio / multi-vertical API
# ------------------------------

VERTICALS = [
    {"key": "fmcg", "name": "Ajoyal Food Products (FMCG)", "status": "demo"},
    {"key": "clinic", "name": "TANUS Skin Clinic", "status": "demo"},
    {"key": "edtech", "name": "IIAIPE (AI Education)", "status": "demo"},
    {"key": "agency", "name": "The Brand Salt (White-label)", "status": "core"},
    {"key": "bschool", "name": "Jaipuria School of Business", "status": "demo"},
]


class ProcessMessageIn(BaseModel):
    client_vertical: str = Field(..., min_length=2, max_length=80)
    incoming_message: str = Field(..., min_length=1, max_length=4000)
    sender_name: str = Field(default="Anonymous", max_length=100)


class ProcessMessageOut(BaseModel):
    reply: str
    escalate: bool
    matched_faq: bool
    source: str
    response_time_ms: float


@app.get("/api/verticals")
def api_verticals():
    return {"verticals": VERTICALS}


@app.post("/api/message/process", response_model=ProcessMessageOut)
def api_process_message(payload: ProcessMessageIn, db: Session = Depends(get_portfolio_db)):
    engine = ResponseEngine(payload.client_vertical)
    result = engine.generate_response(payload.incoming_message, payload.sender_name)

    conv = Conversation(
        vertical=payload.client_vertical,
        sender_name=payload.sender_name,
        incoming_message=payload.incoming_message,
        ai_response=result.reply,
        source=result.source,
        escalated=bool(result.escalate),
        response_time_ms=float(result.response_time_ms),
    )
    db.add(conv)
    db.commit()

    return {
        "reply": result.reply,
        "escalate": bool(result.escalate),
        "matched_faq": bool(result.matched_faq),
        "source": result.source,
        "response_time_ms": float(result.response_time_ms),
    }


@app.get("/api/conversations/{client_vertical}")
def api_conversations(client_vertical: str, db: Session = Depends(get_portfolio_db)):
    items = (
        db.query(Conversation)
        .filter(Conversation.vertical == client_vertical)
        .order_by(Conversation.timestamp.desc())
        .limit(50)
        .all()
    )
    return {
        "vertical": client_vertical,
        "items": [
            {
                "id": c.id,
                "timestamp": c.timestamp,
                "sender_name": c.sender_name,
                "incoming_message": c.incoming_message,
                "ai_response": c.ai_response,
                "source": c.source,
                "escalated": bool(c.escalated),
                "response_time_ms": c.response_time_ms,
            }
            for c in items
        ],
    }


class FAQIn(BaseModel):
    vertical: str = Field(..., min_length=2, max_length=80)
    question: str = Field(..., min_length=3, max_length=4000)
    answer: str = Field(..., min_length=3, max_length=4000)


@app.post("/api/config/faq")
def api_add_faq(payload: FAQIn, db: Session = Depends(get_portfolio_db)):
    row = FAQ(vertical=payload.vertical, question=payload.question, answer=payload.answer)
    db.add(row)
    db.commit()
    return {"ok": True, "id": row.id}


class EscalateIn(BaseModel):
    conversation_id: int = Field(..., ge=1)
    note: str | None = None


@app.post("/api/escalate")
def api_escalate(payload: EscalateIn, db: Session = Depends(get_portfolio_db)):
    c = db.query(Conversation).filter(Conversation.id == payload.conversation_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Conversation not found")
    c.escalated = True
    db.commit()
    return {"ok": True, "simulated_notification": True}


@app.get("/api/stats/{client_vertical}")
def api_stats(client_vertical: str, db: Session = Depends(get_portfolio_db)):
    total = db.query(Conversation).filter(Conversation.vertical == client_vertical).count()
    escalated = (
        db.query(Conversation)
        .filter(Conversation.vertical == client_vertical, Conversation.escalated == True)  # noqa: E712
        .count()
    )
    auto_resolved = max(total - escalated, 0)

    avg_ms = 0.0
    if total:
        rows = db.query(Conversation.response_time_ms).filter(Conversation.vertical == client_vertical).all()
        vals = [float(r[0] or 0) for r in rows]
        avg_ms = sum(vals) / max(len(vals), 1)

    conversion_rate = 0.0
    if total:
        conversion_rate = min(0.65, 0.15 + (auto_resolved / total) * 0.4)

    return {
        "total_inquiries": total,
        "escalated": escalated,
        "auto_resolved": auto_resolved,
        "avg_response_time_seconds": avg_ms / 1000.0,
        "conversion_rate": conversion_rate,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
