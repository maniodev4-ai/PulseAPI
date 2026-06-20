"""
API route definitions for PulseAPI.
"""

from fastapi import APIRouter, HTTPException

from app.models.schema import WineFeatures, PredictionResponse
from app.services.predictor import predict

router = APIRouter()


@router.get("/health")
def health_check() -> dict:
    """
    Health check endpoint.

    Returns a simple status to confirm the API is running.
    Used by monitoring tools, load balancers, or just you,
    to verify the service is alive.
    """
    return {"status": "ok"}


@router.post("/predict", response_model=PredictionResponse)
def predict_wine_class(features: WineFeatures) -> PredictionResponse:
    """
    Predict the wine class from input features.

    Accepts the 13 chemical measurements the model was trained on
    and returns the predicted class along with the model's
    confidence in that prediction.

    Raises:
        HTTPException: 400 if any feature value is invalid
                        (e.g. negative measurements).
    """
    try:
        return predict(features)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))