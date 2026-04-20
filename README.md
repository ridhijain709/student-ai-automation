# SME AI Automation Portfolio

Client-ready portfolio for productized automation services for small and mid-sized businesses (SMEs).

## Positioning

This repository is structured as a consultancy showcase, not a generic student app.  
It demonstrates practical AI automation systems that can be scoped, demoed, and implemented quickly for SMEs.

## Productized Offers

### 1) WhatsApp Lead Follow-up System
- Captures inbound leads from form/sheet workflows.
- Sends immediate acknowledgement message.
- Queues timed follow-up sequence (example: +24h, +48h).
- Logs status for sales handoff.

### 2) Content Calendar + Auto-Scheduler
- Builds weekly/monthly content themes.
- Drafts post copy with AI assistance.
- Supports batch scheduling workflow with client-approved tools.

### 3) AI Query Auto-Responder
- Accepts inbound query text.
- Categorizes urgency/intent.
- Generates response drafts for faster first replies.

## Who This Is For

- Coaching institutes
- Clinics and healthcare practices
- CA/accounting firms
- Retail/FMCG distributors
- Local service businesses

## What Is Live vs Demo

| Area | Status | Notes |
| --- | --- | --- |
| Portfolio landing page (`src/App.tsx`) | Live in repo | Main presentation layer |
| AI draft generation flows | Demo-ready | Works with configured model/backend routes |
| WhatsApp/social platform posting | Simulated by default | Live credentials are connected only in client environments |
| Secrets/API keys | Not stored in repo | Use env vars only |

## Quick Setup

### Prerequisites
- Node.js 18+
- npm

### Run locally
```bash
npm install
npm run dev
```

Open `http://localhost:3000`.

### Build check
```bash
npm run lint
npm run build
```

## Demo Flow (for client calls)

1. Start with one business pain-point (missed leads, content inconsistency, slow query handling).
2. Show the matching productized module.
3. Walk through sample input → automated output.
4. Clarify demo scope vs production integration.
5. Propose 1-week pilot.

## Offer Structure (example)

- **Starter Pilot (1 workflow):** ₹6,000–₹10,000
- **Growth Pack (3 workflows + 30-day support):** ₹18,000+
- **Custom SME Stack:** scoped after discovery

> Pricing is indicative for portfolio presentation and should be adjusted per scope, tool costs, and support window.

## Limitations and Honesty Notes

- This repo intentionally avoids hardcoded production credentials.
- Third-party integrations (WhatsApp API providers, scheduler accounts, CRM tools) require client-owned accounts.
- Some flows are simulation-first to keep demos safe and reproducible.

## Supporting Docs

- `PORTFOLIO_ROADMAP.md` – practical delivery roadmap from demo to implementation.
- `DEPLOYMENT_GUIDE.md` – deployment notes (use placeholders/secrets, never raw keys).

