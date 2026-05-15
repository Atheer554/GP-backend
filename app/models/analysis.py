from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from app.database import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))
    filename = Column(String, nullable=False)
    has_tumor = Column(Boolean, nullable=False)
    tumor_type = Column(String, nullable=True)
    mask_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)