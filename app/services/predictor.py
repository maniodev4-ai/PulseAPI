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

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


def predict(features: WineFeatures) -> PredictionResponse:
    """
    Run inference on a single set of wine features.

    Args:
        features: Validated input features matching the model's
                  expected schema.

    Returns:
        A PredictionResponse containing the predicted class,
        its name, and the model's confidence in that prediction.
    """
    input_array = np.array(
        [
            [
                features.alcohol,
                features.malic_acid,
                features.ash,
                features.alcalinity_of_ash,
                features.magnesium,
                features.total_phenols,
                features.flavanoids,
                features.nonflavanoid_phenols,
                features.proanthocyanins,
                features.color_intensity,
                features.hue,
                features.od280_od315_of_diluted_wines,
                features.proline,
            ]
        ]
    )

    predicted_class = int(model.predict(input_array)[0])
    probabilities = model.predict_proba(input_array)[0]
    confidence = float(probabilities[predicted_class])

    return PredictionResponse(
        predicted_class=predicted_class,
        class_name=CLASS_NAMES[predicted_class],
        confidence=confidence,
    )