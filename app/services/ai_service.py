import requests

AI_API_URL = "https://gp-2026-production-5f0f.up.railway.app"


def send_image_to_ai(file_name: str, file_bytes: bytes, content_type: str):
    files = {
        "file": (file_name, file_bytes, content_type)
    }

    try:
        response = requests.post(AI_API_URL, files=files, timeout=180)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        raise Exception(f"AI API request failed: {str(e)}")


def parse_ai_response(ai_result: dict):
    stage1 = ai_result.get("stage1", {})
    stage2 = ai_result.get("stage2")
    pred = stage1.get("pred")
    prob_tumor = stage1.get("prob_tumor")
    timestamp = ai_result.get("timestamp")
    exit_flag = ai_result.get("exit")

    if pred == "normal":
        return {
            "has_tumor": False,
            "tumor_type": None,
            "mask_path": None,
            "ai_meta": {
                "timestamp": timestamp,
                "stage1_pred": pred,
                "prob_tumor": prob_tumor,
                "stage2": stage2,
                "exit": exit_flag,
            }
        }

    tumor_type = None
    mask_path = None

    if isinstance(stage2, dict):
        tumor_type = (
            stage2.get("pred")
            or stage2.get("tumor_type")
            or stage2.get("class")
            or stage2.get("label")
        )

        mask_path = (
            stage2.get("mask_path")
            or stage2.get("mask")
            or stage2.get("segmentation")
        )

    return {
        "has_tumor": True,
        "tumor_type": tumor_type,
        "mask_path": mask_path,
        "ai_meta": {
            "timestamp": timestamp,
            "stage1_pred": pred,
            "prob_tumor": prob_tumor,
            "stage2": stage2,
            "exit": exit_flag,
        }
    }