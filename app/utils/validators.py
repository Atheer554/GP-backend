from fastapi import HTTPException, UploadFile
from PIL import Image
import io

ALLOWED_TYPES = {"image/jpeg", "image/png"}
ALLOWED_EXTS = {".jpg", ".jpeg", ".png"}

MAX_MB = 10
MIN_W, MIN_H = 128, 128
MAX_W, MAX_H = 6000, 6000


async def read_file_bytes(file: UploadFile) -> bytes:
    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > MAX_MB:
        raise HTTPException(status_code=400, detail="File too large")
    return contents


def validate_content_type(content_type: str) -> None:
    if content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Only JPG/PNG images are allowed")


def validate_extension(filename: str) -> None:
    if not filename or "." not in filename:
        raise HTTPException(status_code=400, detail="File must have an extension")

    ext = "." + filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTS:
        raise HTTPException(status_code=400, detail="Only .jpg/.jpeg/.png are allowed")


def open_and_verify_image(contents: bytes) -> Image.Image:
    try:
        img = Image.open(io.BytesIO(contents))
        img.verify()
        img = Image.open(io.BytesIO(contents))
        return img
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")


def validate_dimensions(img: Image.Image) -> tuple[int, int]:
    w, h = img.size
    if w < MIN_W or h < MIN_H or w > MAX_W or h > MAX_H:
        raise HTTPException(status_code=400, detail="Invalid image dimensions")
    return w, h


def looks_like_ultrasound(img: Image.Image) -> bool:
    # Heuristic: ultrasound images are often grayscale
    if img.mode not in ("L", "RGB", "RGBA"):
        img = img.convert("RGB")

    if img.mode == "L":
        return True

    rgb = img.convert("RGB").resize((128, 128))
    pixels = list(rgb.getdata())

    diffs = []
    for r, g, b in pixels[::50]:
        diffs.append(abs(r - g) + abs(r - b) + abs(g - b))

    avg_diff = sum(diffs) / max(len(diffs), 1)
    return avg_diff < 20