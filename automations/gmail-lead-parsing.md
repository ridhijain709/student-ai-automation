# Gmail Lead Parsing Automation

## What This Automation Does

Reads incoming emails from a Gmail inbox, uses AI to extract key information (client name, query type, urgency level), logs everything to a Google Sheet, and flags urgent items for immediate attention.

---

## Business Problem

Businesses that receive client queries, leads, or support requests by email face:

- Staff manually reading and classifying each email
- Urgent queries buried in general inbox
- No searchable database of client requests
- Time lost on repetitive email triage every morning

---

## Solution Flow

```
New email arrives in Gmail
        ↓
Script reads subject + body
        ↓
Gemini AI extracts: name, query type, urgency
        ↓
Data written to Google Sheet
        ↓
Urgent items flagged in red / separate tab
        ↓
Email marked as read
```

---

## Tools Used

| Tool | Role |
|------|------|
| Gmail API | Read incoming emails |
| Google Gemini API | Extract structured data from email body |
| Google Sheets API | Store parsed leads |
| Python 3.10 | Script execution |
| Make.com (optional) | Trigger and scheduling |

---

## What Gets Automated

1. **Email reading** — script checks inbox at set intervals or on trigger
2. **AI extraction** — pulls sender name, query type, urgency score from free-form email text
3. **Sheet logging** — writes structured rows to Google Sheet automatically
4. **Urgency flagging** — urgent queries highlighted or routed separately
5. **Status marking** — email marked as read after processing

---

## Example Output (Google Sheet Row)

| Sender Name | Email | Query Type | Urgency | Summary | Received |
|-------------|-------|------------|---------|---------|----------|
| Ramesh Gupta | rg@example.com | Tax filing | High | Needs ITR filed before deadline | 25 Apr 2026 |
| Anita Sharma | as@example.com | New client inquiry | Medium | Wants GST registration help | 25 Apr 2026 |

---

## Business Impact

- Eliminates 30–60 minutes of daily manual email triage
- Urgent queries handled within minutes instead of hours
- Builds a searchable client query history automatically
- Consistent classification removes human error

---

## Pricing Guidance

| Tier | Scope | Price Range |
|------|-------|-------------|
| Basic | Gmail parsing + sheet logging | ₹6,000–₹10,000 |
| Standard | Parsing + urgency flagging + notifications | ₹12,000–₹18,000 |
| Advanced | Full client CRM pipeline integration | ₹20,000–₹30,000 |

---

## Client Types Best Suited For This

- CA firms and accounting practices
- Law firms
- Consultancies receiving inquiry emails daily
- E-commerce businesses with customer support emails
- Any business where email triage takes 30+ minutes per day

---

## Status

Core script functional. Integration demo available on request.
