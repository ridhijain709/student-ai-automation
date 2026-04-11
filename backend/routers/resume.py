from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.models import ResumeVersion
from backend.services import resume_service
from pydantic import BaseModel

router = APIRouter(prefix="/resume", tags=["resume"])

class ResumeInput(BaseModel):
    target_role: str
    company_name: str
    jd_text: str
    master_profile_text: str

@router.post("/generate")
def generate(data: ResumeInput, db: Session = Depends(get_db)):
    return resume_service.generate_resume(db, data.target_role, data.company_name, data.jd_text, data.master_profile_text)

@router.get("/versions")
def get_versions(db: Session = Depends(get_db)):
    return db.query(ResumeVersion).all()

@router.get("/version/{id}")
def get_version(id: int, db: Session = Depends(get_db)):
    version = db.query(ResumeVersion).filter(ResumeVersion.id == id).first()
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    return version
