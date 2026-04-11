from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.models import TruthGridReport
from backend.services import truthgrid_service
from pydantic import BaseModel

router = APIRouter(prefix="/truthgrid", tags=["truthgrid"])

class TruthGridInput(BaseModel):
    student_name: str
    target_role: str
    projects_count: int
    internships_count: int
    tools_score: int
    communication_score: int
    certifications_count: int

@router.post("/generate")
def generate(data: TruthGridInput, db: Session = Depends(get_db)):
    return truthgrid_service.generate_report(
        db, data.student_name, data.target_role, 
        data.projects_count, data.internships_count, 
        data.tools_score, data.communication_score, data.certifications_count
    )

@router.get("/reports")
def get_reports(db: Session = Depends(get_db)):
    return db.query(TruthGridReport).all()

@router.get("/report/{id}")
def get_report(id: int, db: Session = Depends(get_db)):
    report = db.query(TruthGridReport).filter(TruthGridReport.id == id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report
