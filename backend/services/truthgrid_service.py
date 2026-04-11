from sqlalchemy.orm import Session
from backend.models import TruthGridReport
from backend.gemini_client import call_gemini_json
from backend.prompts import TRUTHGRID_PROMPT
from backend.gemini_schemas import TruthGridReportSchema
import json

def calculate_score(projects, internships, tools, comms, certs):
    # Simple rule-based scoring
    return (projects * 10) + (internships * 15) + (tools * 5) + (comms * 5) + (certs * 5)

def generate_report(db: Session, student_name: str, target_role: str, projects: int, internships: int, tools: int, comms: int, certs: int):
    score = calculate_score(projects, internships, tools, comms, certs)
    
    user_prompt = f"Student: {student_name}, Role: {target_role}, Score: {score}"
    analysis_json = call_gemini_json(TRUTHGRID_PROMPT, user_prompt, TruthGridReportSchema)
    analysis = json.loads(analysis_json)
    
    report = TruthGridReport(
        student_name=student_name,
        target_role=target_role,
        score=score,
        strengths=",".join(analysis["strengths"]),
        weaknesses=",".join(analysis["weaknesses"]),
        next_steps=",".join(analysis["next_30_day_plan"]),
        full_report=analysis["summary_report"]
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report
