from app.models import analysis
from app.models import user
from app.models.patient import Patient
from app.database import engine
from app.database import Base
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.predict import router as predict_router
from app.routes.auth import router as auth_router
from app.routes.patient import router as patient_router

app = FastAPI(title="Breast Cancer Detection Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://localhost:3000",
    "https://gp-frontend-gamma.vercel.app",
    "https://gp-frontend-git-feature-ef5217-atheeraladwan371-7653s-projects.vercel.app",
    "https://gp-frontend-git-feature-44801a-atheeraladwan371-7653s-projects.vercel.app",
    " http://localhost:5173/",

    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Backend is working"}

app.include_router(predict_router)
app.include_router(auth_router)
app.include_router(patient_router)