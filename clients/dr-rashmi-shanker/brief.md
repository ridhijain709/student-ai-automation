# Dr. Rashmi Shanker — Client Brief

## Overview

- **Name:** Dr. Rashmi Shanker
- **Sector:** Healthcare / Clinic
- **Likely specialisation:** Dermatology or general practice
- **Primary challenge:** Managing high volume of repetitive patient queries alongside clinical work

---

## Strategic Context

Independent practitioners and small clinics face a consistent operational problem: communication with patients is unstructured and manual. A large portion of WhatsApp messages from patients are identical — asking about the same treatments, the same prices, the same appointment availability. Every minute spent answering these manually is a minute away from actual clinical work.

The automation case is unusually strong here because:
1. The queries are highly repetitive and predictable
2. The cost of a missed or delayed response is a lost patient
3. After-hours availability is a genuine competitive advantage

---

## Pain Point Analysis

| Pain Point | Business Impact |
|------------|-----------------|
| Staff answering same questions repeatedly | 1–2 hours of staff time wasted daily |
| After-hours messages unanswered | Patients book with competitors |
| No structured appointment capture | Double bookings or missed slots |
| Doctor personally answering WhatsApp | Reduces clinical focus |
| No query history | No visibility on what patients most commonly ask |

---

## Recommended Automation: Patient Handling AI System

### Module 1 — FAQ Responder
- Common questions handled automatically: treatment options, pricing, side effects, recovery time
- AI uses clinic-specific information — only states what the clinic provides
- Escalation: if question is complex or clinical, directs to staff or doctor

### Module 2 — Appointment Request Capture
- Patient types "book appointment" or similar
- AI asks: Name, preferred date, treatment of interest
- Response logged to Google Sheet
- Confirmation message sent to patient

### Module 3 — After-Hours Handler
- Messages received outside clinic hours get an immediate, professional response
- Appointment requests captured and queued for next morning
- No patient is left waiting until the next business day to even receive an acknowledgement

### Module 4 — Query Log (optional)
- Sheet tracks all inbound queries by type
- Helps identify most common patient concerns (useful for content, FAQs, service additions)

---

## Implementation Notes

- Built on Make.com + WATI or AiSensy
- Clinic provides: treatment list, pricing ranges, working hours, appointment availability
- Demo can be set up within 3–5 days of receiving clinic information
- No technical knowledge required from the clinic side
- Sensitive medical advice is explicitly excluded from AI responses — all clinical questions escalated to doctor

---

## Positioning for This Client

Do not pitch as a tech product. Frame it as:

> "This handles the 80% of patient queries that are routine, so you and your staff focus only on the 20% that actually need clinical attention."

---

## Upsell Path

1. Monthly query analytics report (what are patients asking most?)
2. Post-visit follow-up automation (review request, prescription reminder)
3. Seasonal campaign messages (e.g., summer skin care tips + CTA to book)
