"""
Model loading and inference logic.

Loads the trained model once at import time and exposes
a function to run predictions on new input data.
"""

import pickle
from pathlib import Path

import numpy as np

from app.models.schema import WineFeatures, PredictionResponse

MODEL_PATH = Path("ml/saved_model.pkl")

CLASS_NAMES = ["class_0", "class_1", "class_2"]


def _load_model():
    """Load the trained model from disk, raising a clear error if missing."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found at {MODEL_PATH}. "
            "Run 'python ml/train.py' to generate it before starting the API."
        )
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


model = _load_model()


def predict(features: WineFeatures) -> PredictionResponse:
    """
    Run inference on a single set of wine features.

    Args:
        features: Validated input features matching the model's
                  expected schema.

    Returns:
        A PredictionResponse containing the predicted class,
        its name, and the model's confidence in that prediction.

    Raises:
        ValueError: If any feature value is negative, since none
                    of the wine measurements can physically be negative.
    """
    feature_dict = features.model_dump()
    for name, value in feature_dict.items():
        if value < 0:
            raise ValueError(
                f"Invalid value for '{name}': {value}. "
                "Wine feature measurements cannot be negative."
            )

    input_array = np.array([list(feature_dict.values())])

    predicted_class = int(model.predict(input_array)[0])
    probabilities = model.predict_proba(input_array)[0]
    confidence = float(probabilities[predicted_class])

    return PredictionResponse(
        predicted_class=predicted_class,
        class_name=CLASS_NAMES[predicted_class],
        confidence=confidence,
    )