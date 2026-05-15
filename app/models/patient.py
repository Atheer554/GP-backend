from sqlalchemy import Column, Integer, String
from app.database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer)
    patient_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)