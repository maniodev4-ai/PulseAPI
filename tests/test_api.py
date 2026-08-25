"""
Tests for PulseAPI endpoints and prediction logic.
"""

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.models.schema import WineFeatures
from app.services.predictor import predict
from app.database.connection import Base
from app.database.models import Prediction
from app.auth.models import APIKey
from app.api.routes import get_db
from app.auth.dependencies import get_api_key

# ── Test database setup ──────────────────────────────────────────
TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(bind=test_engine)

Base.metadata.create_all(bind=test_engine)

TEST_API_KEY = "test-key-abc123"

with TestingSessionLocal() as setup_db:
    existing = setup_db.query(APIKey).filter(
        APIKey.key_hash == TEST_API_KEY
    ).first()
    if not existing:
        from datetime import datetime
        setup_db.add(APIKey(
            key_hash=TEST_API_KEY,
            name="test-key",
            is_active=True,
            created_at=datetime.utcnow()
        ))
        setup_db.commit()

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_api_key():
    with TestingSessionLocal() as db:
        return db.query(APIKey).filter(APIKey.key_hash == TEST_API_KEY).first()


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_api_key] = override_get_api_key

client = TestClient(app)

VALID_PAYLOAD = {
    "alcohol": 13.0,
    "malic_acid": 2.0,
    "ash": 2.3,
    "alcalinity_of_ash": 18.0,
    "magnesium": 100.0,
    "total_phenols": 2.5,
    "flavanoids": 2.0,
    "nonflavanoid_phenols": 0.3,
    "proanthocyanins": 1.5,
    "color_intensity": 5.0,
    "hue": 1.0,
    "od280_od315_of_diluted_wines": 2.5,
    "proline": 750.0,
}


# ── Integration tests ────────────────────────────────────────────

def test_health_check_returns_ok():
    """The /health endpoint should return status ok with a 200."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_endpoint_returns_valid_response():
    """The /predict endpoint should return a valid prediction shape."""
    response = client.post("/predict", json=VALID_PAYLOAD)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_class" in data
    assert "class_name" in data
    assert "confidence" in data
    assert 0 <= data["confidence"] <= 1


def test_predict_endpoint_rejects_missing_fields():
    """Sending an incomplete payload should fail validation with 422."""
    response = client.post("/predict", json={"alcohol": 13.0})
    assert response.status_code == 422


def test_predict_endpoint_rejects_negative_values():
    """Sending negative feature values should fail with a 400 error."""
    payload = {**VALID_PAYLOAD, "alcohol": -5.0}
    response = client.post("/predict", json=payload)
    assert response.status_code == 400
    assert "negative" in response.json()["detail"]


def test_get_predictions_returns_list():
    """The /predictions endpoint should return a list."""
    response = client.get("/predictions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ── Unit test ────────────────────────────────────────────────────

def test_predict_function_returns_expected_shape():
    """Calling predict() directly should return a valid PredictionResponse."""
    features = WineFeatures(**VALID_PAYLOAD)
    result = predict(features)
    assert result.predicted_class in [0, 1, 2]
    assert result.class_name in ["class_0", "class_1", "class_2"]
    assert 0 <= result.confidence <= 1