from pydantic import BaseModel


class PatientCreate(BaseModel):
    name: str
    patient_id: str
    age: int
    gender: str


class PatientResponse(BaseModel):
    id: int
    name: str
    patient_id: str
    age: int
    gender: str

    class Config:
        from_attributes = True