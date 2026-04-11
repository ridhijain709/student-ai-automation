DASHBOARD_PROMPT = """
You are the Ridhi Command Center AI. Analyze the current state of inbox, tasks, and pending approvals.
Provide a concise summary for the dashboard.
"""

GMAIL_TRIAGE_PROMPT = """
Analyze this email for a student entrepreneur.
Return: category (job, networking, startup, client, study, personal, spam), 
urgency (urgent, important, waiting, low), 
2-line summary, 
recommended next action, 
draft reply, 
approval_required (boolean).
"""

LINKEDIN_ASSIST_PROMPT = """
Analyze this LinkedIn message.
Return: relationship_stage (cold, warm, active, waiting), 
best_next_action, 
reply_draft, 
follow_up_days (int), 
is_worth_pursuing (boolean).
"""

RESUME_GENERATION_PROMPT = """
Generate ATS-friendly resume content based on this JD and student profile.
Return: professional_summary, 
skills (list), 
project_bullets (list), 
cover_letter_draft.
"""

TRUTHGRID_PROMPT = """
Generate a student employability report based on score and profile.
Return: strengths (list), 
weaknesses (list), 
next_30_day_plan (list), 
summary_report.
"""
