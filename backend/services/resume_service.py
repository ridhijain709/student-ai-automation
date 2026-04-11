from sqlalchemy.orm import Session
from backend.models import ResumeVersion
from backend.gemini_client import call_gemini_json
from backend.prompts import RESUME_GENERATION_PROMPT
from backend.gemini_schemas import ResumeGenerationSchema
import json

def generate_resume(db: Session, target_role: str, company_name: str, jd_text: str, master_profile: str):
    user_prompt = f"Target Role: {target_role}\nCompany: {company_name}\nJD: {jd_text}\nProfile: {master_profile}"
    analysis_json = call_gemini_json(RESUME_GENERATION_PROMPT, user_prompt, ResumeGenerationSchema)
    analysis = json.loads(analysis_json)
    
    version = ResumeVersion(
        target_role=target_role,
        company_name=company_name,
        jd_text=jd_text,
        generated_summary=analysis["professional_summary"],
        generated_skills=",".join(analysis["skills"]),
        generated_bullets=",".join(analysis["project_bullets"]),
        generated_cover_letter=analysis["cover_letter_draft"]
    )
    db.add(version)
    db.commit()
    db.refresh(version)
    return version
