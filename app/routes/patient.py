from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.patient import Patient
from app.schemas.patient import PatientCreate
from app.routes.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/patients", tags=["Patients"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_patient(patient: PatientCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    new_patient = Patient(
        patient_id=patient.patient_id,
        name=patient.name,
        age=patient.age,
        gender=patient.gender,
        user_id=current_user.id
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient

@router.get("/")
def get_patients(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    patients = db.query(Patient).filter(Patient.user_id==current_user.id).all()
    return patients