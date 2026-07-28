"""
API route definitions for PulseAPI.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import Prediction
from app.models.schema import WineFeatures, PredictionResponse
from app.services.predictor import predict

router = APIRouter()


def get_db():
    """
    Dependency that provides a database session for each request.
    Opens a session, yields it, then closes it when the request is done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
def predict_wine_class(
    features: WineFeatures,
    db: Session = Depends(get_db)
) -> PredictionResponse:
    """
    Predict the wine class from input features.

    Accepts the 13 chemical measurements the model was trained on,
    returns the predicted class with confidence, and saves the
    prediction to the database for history and analysis.

    Raises:
        HTTPException: 400 if any feature value is invalid.
    """
    try:
        result = predict(features)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Save prediction to database
    record = Prediction(
        alcohol=features.alcohol,
        malic_acid=features.malic_acid,
        ash=features.ash,
        alcalinity_of_ash=features.alcalinity_of_ash,
        magnesium=features.magnesium,
        total_phenols=features.total_phenols,
        flavanoids=features.flavanoids,
        nonflavanoid_phenols=features.nonflavanoid_phenols,
        proanthocyanins=features.proanthocyanins,
        color_intensity=features.color_intensity,
        hue=features.hue,
        od280_od315_of_diluted_wines=features.od280_od315_of_diluted_wines,
        proline=features.proline,
        predicted_class=result.predicted_class,
        class_name=result.class_name,
        confidence=result.confidence,
    )
    db.add(record)
    db.commit()

    return result

@router.get("/predictions")
def get_predictions(db: Session = Depends(get_db)) -> list:
    """
    Retrieve all past predictions from the database.

    Returns a list of every prediction ever made, ordered
    by most recent first.
    """
    records = db.query(Prediction).order_by(Prediction.created_at.desc()).all()
    return [
        {
            "id": r.id,
            "predicted_class": r.predicted_class,
            "class_name": r.class_name,
            "confidence": r.confidence,
            "created_at": r.created_at.isoformat(),
        }
        for r in records
    ]