from PIL import Image
import numpy as np

def preprocess_for_model(img: Image.Image, target_size=(224, 224)) -> dict:
    """
    Preprocess steps:
    - Convert to RGB
    - Resize to target_size
    - Convert to numpy float32
    - Normalize to [0,1]
    - Change shape to (1, 3, H, W) suitable for many models
    Returns:
      {
        "input_array": np.ndarray,
        "meta": {...}
      }
    """
    original_mode = img.mode
    original_size = img.size

    rgb = img.convert("RGB")
    resized = rgb.resize(target_size)

    arr = np.array(resized).astype(np.float32)  # (H, W, 3)
    arr_norm = arr / 255.0

    # (H, W, 3) -> (3, H, W)
    chw = np.transpose(arr_norm, (2, 0, 1))

    # Add batch dimension: (1, 3, H, W)
    batched = np.expand_dims(chw, axis=0)

    meta = {
        "original_mode": original_mode,
        "processed_mode": "RGB",
        "original_size": [original_size[0], original_size[1]],
        "processed_size": [target_size[0], target_size[1]],
        "normalized": True,
        "shape": list(batched.shape),
    }

    return {
        "input_array": batched,
        "meta": meta
    }