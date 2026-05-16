from fastapi import Depends, APIRouter, UploadFile, File, HTTPException, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.analysis import Analysis
from app.models.user import User
from app.routes.auth import get_current_user
import uuid
from datetime import datetime, timezone

from app.utils.validators import (
    read_file_bytes,
    validate_content_type,
    validate_extension,
    open_and_verify_image,
    validate_dimensions,
    looks_like_ultrasound,
)

from app.utils.preprocess import preprocess_for_model
from app.services.ai_service import send_image_to_ai, parse_ai_response

router = APIRouter()


@router.post("/predict")
async def predict(
    file: UploadFile = File(...),
    patient_id: int = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    request_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()

    # 1) التحقق من الامتداد
    validate_extension(file.filename)

    # 2) التحقق من نوع الملف
    validate_content_type(file.content_type)

    # 3) قراءة الملف
    contents = await read_file_bytes(file)

    # 4) فتح الصورة والتأكد منها
    img = open_and_verify_image(contents)

    # 5) التحقق من الأبعاد
    w, h = validate_dimensions(img)

    # 6) التحقق هل الصورة تشبه السونار
    ultrasound_like = looks_like_ultrasound(img)
    if not ultrasound_like:
        raise HTTPException(
            status_code=400,
            detail="The uploaded image does not appear to be an ultrasound image",
        )

    # 7) preprocessing
    processed = preprocess_for_model(img, target_size=(224, 224))

    # 8) إرسال الصورة إلى AI API الحقيقي
    try:
        ai_raw_result = send_image_to_ai(
            file_name=file.filename,
            file_bytes=contents,
            content_type=file.content_type
        )
        ai_result = parse_ai_response(ai_raw_result)

    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"AI service error: {str(e)}"
        )

    has_tumor = ai_result["has_tumor"]
    tumor_type = ai_result["tumor_type"]
    mask_path = ai_result["mask_path"]

    # 9) حفظ النتيجة في قاعدة البيانات
    new_analysis = Analysis(
        user_id=current_user.id,
        patient_id=patient_id,
        filename=file.filename,
        has_tumor=has_tumor,
        tumor_type=tumor_type,
        mask_path=mask_path
    )

    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)

    # 10) إرجاع النتيجة
    return {
        "status": "success",
        "analysis": {
            "has_tumor": has_tumor,
            "tumor_type": tumor_type,
            "mask_path": mask_path
        },
        "metadata": {
            "filename": file.filename,
            "request_id": request_id,
            "timestamp": timestamp,
            "width": w,
            "height": h,
            "ultrasound_like": ultrasound_like,
            "preprocess": processed["meta"],
            "user_id": current_user.id,
            "ai_response": ai_result["ai_meta"]
        }
    }


@router.get("/history/{patient_id}")
def get_history(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    analyses = db.query(Analysis).filter(
        Analysis.user_id == current_user.id,
        Analysis.patient_id == patient_id
    ).all()

    history = []

    for a in analyses:
        history.append({
            "analysis_id": a.id,
            "image": a.filename,
            "has_tumor": a.has_tumor,
            "tumor_type": a.tumor_type,
            "date": a.created_at
        })

    return history


@router.get("/analysis/{analysis_id}")
def get_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id,
        Analysis.user_id == current_user.id
    ).first()

    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return {
        "analysis_id": analysis.id,
        "image": analysis.filename,
        "has_tumor": analysis.has_tumor,
        "tumor_type": analysis.tumor_type,
        "mask_path": analysis.mask_path,
        "date": analysis.created_at
    }