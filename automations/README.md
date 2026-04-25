# Automations

This section contains detailed documentation for each reusable automation system in the portfolio. Each automation is designed to be adapted for specific client contexts.

---

## Available Automations

| # | Automation | Best For | Status |
|---|-----------|----------|--------|
| 1 | [WhatsApp Lead Follow-Up](whatsapp-lead-followup.md) | Clinics, coaching, food brands, service businesses | Demo Ready |
| 2 | [Gmail Lead Parsing](gmail-lead-parsing.md) | CA firms, consultancies, professional services | Core Built |
| 3 | [AI Content Scheduling](ai-content-scheduling.md) | D2C brands, coaches, personal brands | Template Ready |

---

## How These Are Used

Each automation in this folder represents a **reusable base system** that can be customised for a specific client. The core flow stays the same; only the prompts, data fields, and business context change.

For example:
- The WhatsApp Lead Follow-Up system is used for distributor enquiries (Ajoyal), patient queries (Dr. Rashmi), admission enquiries (Ajay Singh Yadav), and restaurant bookings (Arsh Agarwal).
- The AI Content Scheduling system is adapted for personal brands (Priyanshi, Sitanshu) and for agency clients.

---

## Adapting an Automation for a Client

1. Read the relevant automation doc in this folder
2. Read the client's folder in `clients/` for specific context
3. Adjust the AI prompt to match the client's business type, services, and tone
4. Use the client's `demo-script.md` to guide the live walkthrough

---

## Adding a New Automation

If a new automation is developed for a client, add a new `.md` file in this folder following the structure of the existing files:

- What the automation does
- Business problem it solves
- Solution flow
- Tools used
- What gets automated
- Business impact
- Pricing guidance
- Client types best suited
- Status
