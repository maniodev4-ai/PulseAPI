"""
Tests for PulseAPI endpoints and prediction logic.
"""

from fastapi.testclient import TestClient

from app.main import app
from app.models.schema import WineFeatures
from app.services.predictor import predict

client = TestClient(app)


# --- Integration tests: hit the actual API endpoints ---

def test_health_check_returns_ok():
    """The /health endpoint should return status ok with a 200."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_endpoint_returns_valid_response():
    """The /predict endpoint should return a valid prediction shape."""
    payload = {
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
    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "predicted_class" in data
    assert "class_name" in data
    assert "confidence" in data
    assert 0 <= data["confidence"] <= 1


def test_predict_endpoint_rejects_missing_fields():
    """Sending an incomplete payload should fail validation with 422."""
    incomplete_payload = {"alcohol": 13.0}
    response = client.post("/predict", json=incomplete_payload)
    assert response.status_code == 422


# --- Unit test: test the predictor function directly, no HTTP involved ---

def test_predict_function_returns_expected_shape():
    """Calling predict() directly should return a valid PredictionResponse."""
    features = WineFeatures(
        alcohol=13.0,
        malic_acid=2.0,
        ash=2.3,
        alcalinity_of_ash=18.0,
        magnesium=100.0,
        total_phenols=2.5,
        flavanoids=2.0,
        nonflavanoid_phenols=0.3,
        proanthocyanins=1.5,
        color_intensity=5.0,
        hue=1.0,
        od280_od315_of_diluted_wines=2.5,
        proline=750.0,
    )
    result = predict(features)

    assert result.predicted_class in [0, 1, 2]
    assert result.class_name in ["class_0", "class_1", "class_2"]
    assert 0 <= result.confidence <= 1


def test_predict_endpoint_rejects_negative_values():
    """Sending negative feature values should fail with a 400 error."""
    payload = {
        "alcohol": -5.0,
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
    response = client.post("/predict", json=payload)
    assert response.status_code == 400
    assert "negative" in response.json()["detail"]