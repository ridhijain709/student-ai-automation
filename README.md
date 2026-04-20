# SME AI Automation Suite

Production-oriented, low-cost automation stack for SMEs with 3 core workflows:

1. **WhatsApp Lead Follow-up**
2. **Content Scheduler**
3. **AI Auto-Responder**

This repo keeps the implementation simple enough for non-technical operators, while adding safer validation, status tracking, and configuration for real deployments.

---

## What’s Included

### 1) WhatsApp Lead Follow-up (`/whatsapp`)
- Capture new leads with row-aware dedupe (`source_row_id`)
- Normalize and validate phone numbers
- Prevent duplicate sends with status-based gating
- Track lifecycle: `new` → `welcome_sent` → `followup_sent` / `failed`
- Run due follow-ups with one endpoint call

Key endpoints:
- `POST /whatsapp/leads`
- `POST /whatsapp/followups/run`
- `GET /whatsapp/leads`
- `GET /whatsapp/messages`

### 2) Content Scheduler (`/content-scheduler`)
- Create scheduled content with strict platform validation
- Reliable datetime parsing (ISO, timezone-safe UTC normalization)
- Optional AI suggestion generation (with fallback if model fails)
- Reminder execution flow with one-time reminder state tracking
- Publish status updates with reference IDs

Key endpoints:
- `POST /content-scheduler/items`
- `GET /content-scheduler/items`
- `POST /content-scheduler/reminders/run`
- `POST /content-scheduler/items/{id}/publish`

### 3) AI Auto-Responder (`/auto-responder`)
- Safe webhook handling with request validation
- Channel allowlist to block unexpected sources
- Keyword-based escalation for sensitive conversations
- Configurable business context (no hardcoded vertical assumptions)
- Persistent response/event logging for auditability

Key endpoints:
- `POST /auto-responder/webhook`
- `GET /auto-responder/events`

---

## Architecture

- **Backend:** FastAPI + SQLAlchemy + SQLite
- **Frontend:** React + Vite (dashboard/prototype UI)
- **AI:** Gemini (`gemini-1.5-flash`) with structured JSON responses where needed

The backend is the source of truth for automation status tracking.

---

## Setup

### Prerequisites
- Python 3.10+
- Node.js 20+

### Backend
```bash
cd /home/runner/work/student-ai-automation/student-ai-automation
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn backend.main:app --reload --port 8000
```

### Frontend
```bash
cd /home/runner/work/student-ai-automation/student-ai-automation
npm ci
npm run dev
```

---

## Example Requests

### Create a lead
```bash
curl -X POST http://localhost:8000/whatsapp/leads \
  -H "Content-Type: application/json" \
  -d '{
    "source_row_id":"row-101",
    "name":"Anita",
    "phone":"9876543210",
    "requirement":"Need pricing for coaching package",
    "source":"google_sheet"
  }'
```

### Create a scheduled post
```bash
curl -X POST http://localhost:8000/content-scheduler/items \
  -H "Content-Type: application/json" \
  -d '{
    "platform":"linkedin",
    "title":"Free SME Growth Checklist",
    "content":"Download our checklist to reduce lead response time.",
    "scheduled_for":"2026-05-01T10:00:00Z",
    "generate_ai_suggestion":true
  }'
```

### Handle incoming customer webhook
```bash
curl -X POST http://localhost:8000/auto-responder/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "channel":"whatsapp",
    "sender":"+919999999999",
    "text":"Can someone help me with my order status?",
    "source":"whatsapp_cloud_api"
  }'
```

---

## Production Notes

- Replace permissive CORS (`*`) before deployment.
- Keep all API keys in environment variables.
- For high-volume usage, migrate from SQLite to Postgres and add background workers for scheduler/follow-up jobs.
- Current sending is queue/simulation-ready through stored drafts; integrate your provider (AiSensy/Twilio/WATI) in the service layer.

---

## Positioning for Client Demos

This suite is designed to show SME owners outcomes, not tooling:
- Faster lead response
- Fewer missed follow-ups
- Consistent content execution
- Reliable first-response support with human escalation
