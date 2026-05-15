import random
import numpy as np

def gate_has_tumor(model_input: np.ndarray) -> bool:
    """
    Stage 1 (Mock): decide if image is abnormal (has tumor) or not.
    Replace with real inference later.
    """
    return random.choice([True, False])


def segment_tumor(model_input: np.ndarray) -> str:
    """
    Stage 2 (Mock segmentation): return a fake mask path.
    Replace with real segmentation later.
    """
    return "mock_mask.png"


def classify_tumor_type(model_input: np.ndarray) -> str:
    """
    Stage 3 (Mock classification): benign or malignant.
    Replace with real classification later.
    """
    return random.choice(["benign", "malignant"])