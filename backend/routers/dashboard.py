from fastapi import APIRouter, Depends, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.services import dashboard_service
from backend.models import LeadInteraction, Lead

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("", response_class=HTMLResponse)
def leads_dashboard(
    db: Session = Depends(get_db),
    limit: int = 100,
    client: str | None = Query(default=None, description="Filter: clinic | education | fmcg"),
):
    # Prefer new structured interactions; fall back to legacy leads if none exist.
    q = db.query(LeadInteraction)
    if client:
        q = q.filter(LeadInteraction.client_key == client)
    interactions = (
        q.order_by(LeadInteraction.created_at.desc())
        .limit(min(max(limit, 1), 300))
        .all()
    )
    leads = []
    if not interactions:
        leads = (
            db.query(Lead)
            .order_by(Lead.created_at.desc())
            .limit(min(max(limit, 1), 300))
            .all()
        )

    if interactions:
        rows = "\n".join(
            f"<tr>"
            f"<td style='padding:8px;border-bottom:1px solid #eee'>{(x.client_name or x.client_key or '')}</td>"
            f"<td style='padding:8px;border-bottom:1px solid #eee'>{(x.name or '')}</td>"
            f"<td style='padding:8px;border-bottom:1px solid #eee;white-space:pre-wrap'>{(x.message or '')}</td>"
            f"<td style='padding:8px;border-bottom:1px solid #eee'>{(x.intent or '')}</td>"
            f"<td style='padding:8px;border-bottom:1px solid #eee'>{x.created_at}</td>"
            f"</tr>"
            for x in interactions
        )
    else:
        rows = "\n".join(
            f"<tr>"
            f"<td style='padding:8px;border-bottom:1px solid #eee'>{(l.name or '')}</td>"
            f"<td style='padding:8px;border-bottom:1px solid #eee;white-space:pre-wrap'>{(l.message or '')}</td>"
            f"<td style='padding:8px;border-bottom:1px solid #eee'>{l.created_at}</td>"
            f"</tr>"
            for l in leads
        )

    return f"""
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Lead Dashboard</title>
  </head>
  <body style="font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial; margin: 24px;">
    <div style="display:flex; justify-content:space-between; align-items:flex-end; gap: 16px; flex-wrap: wrap;">
      <div>
        <h2 style="margin:0 0 6px 0;">Lead Dashboard</h2>
        <div style="color:#555;">Latest leads captured from automations (WhatsApp/web/etc.).</div>
      </div>
      <div style="color:#666; font-size: 14px;">Showing {len(leads)} lead(s)</div>
    </div>

    <div style="margin-top: 16px; border:1px solid #eee; border-radius: 10px; overflow:hidden;">
      <table style="width:100%; border-collapse:collapse;">
        <thead>
          <tr style="background:#fafafa; text-align:left;">
            {"<th style='padding:10px;border-bottom:1px solid #eee; width: 18%;'>Client</th><th style='padding:10px;border-bottom:1px solid #eee; width: 14%;'>Name</th><th style='padding:10px;border-bottom:1px solid #eee;'>Message</th><th style='padding:10px;border-bottom:1px solid #eee; width: 14%;'>Intent</th><th style='padding:10px;border-bottom:1px solid #eee; width: 18%;'>Timestamp</th>" if interactions else "<th style='padding:10px;border-bottom:1px solid #eee; width: 16%;'>Name</th><th style='padding:10px;border-bottom:1px solid #eee;'>Message</th><th style='padding:10px;border-bottom:1px solid #eee; width: 18%;'>Timestamp</th>"}
          </tr>
        </thead>
        <tbody>
          {rows or ("<tr><td colspan='5' style='padding:14px;color:#777;'>No leads yet. Send a WhatsApp webhook to generate one.</td></tr>" if interactions else "<tr><td colspan='3' style='padding:14px;color:#777;'>No leads yet. Send a WhatsApp webhook to generate one.</td></tr>")}
        </tbody>
      </table>
    </div>

    <div style="margin-top:14px; color:#666; font-size: 14px;">
      Tip: For a quick demo, call <code>POST /whatsapp/webhook?client=clinic</code> (or education/fmcg).
    </div>
  </body>
</html>
"""

@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    return dashboard_service.get_summary(db)
