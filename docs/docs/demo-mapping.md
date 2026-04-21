# Demo Mapping

This repository is being repositioned into 3 client-ready automation demos.

---

## 1. WhatsApp Lead Follow-up System

### Business problem
Leads come in, but follow-up is delayed or forgotten.

### Solution
Automate lead capture and follow-up using a form, sheet, workflow trigger, and WhatsApp messaging.

### Current repo mapping
- `backend/routers/whatsapp.py`
- `backend/services/whatsapp_service.py`
- `frontend/src/pages/WhatsAppPage.tsx`

### Suggested demo assets
- form submission screenshot
- WhatsApp message screenshot
- workflow diagram
- Loom walkthrough

---

## 2. Content Auto-Scheduler

### Business problem
Small businesses struggle to post content consistently.

### Solution
Generate captions from a content sheet and schedule them automatically.

### Current repo mapping
- Create new content scheduler route/service
- Create new frontend page for the demo

### Suggested demo assets
- content calendar screenshot
- generated caption example
- workflow diagram
- Loom walkthrough

---

## 3. FAQ Auto-Reply Bot

### Business problem
Teams waste time answering the same questions repeatedly.

### Solution
Use AI to classify customer questions and draft instant replies.

### Current repo mapping
- `backend/prompts.py`
- `backend/routers/telegram.py`
- `backend/routers/gmail.py`
- `frontend/src/pages/TelegramPage.tsx`
- `frontend/src/pages/GmailPage.tsx`

### Suggested demo assets
- incoming question screenshot
- AI reply screenshot
- approval flow screenshot
- workflow diagram
- Loom walkthrough

---

## Positioning Rule
Every demo should be framed as an outcome:
- faster response time
- fewer missed leads
- consistent posting
- less manual support work
