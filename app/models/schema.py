"""
Pydantic models defining the shape of requests and responses
for the /predict endpoint.
"""

from pydantic import BaseModel, Field


class WineFeatures(BaseModel):
    """
    Input features for a wine prediction request.

    These correspond exactly to the 13 features the model
    was trained on, in the same order.
    """

    alcohol: float = Field(..., json_schema_extra={"example": 13.0})
    malic_acid: float = Field(..., json_schema_extra={"example": 2.0})
    ash: float = Field(..., json_schema_extra={"example": 2.3})
    alcalinity_of_ash: float = Field(..., json_schema_extra={"example": 18.0})
    magnesium: float = Field(..., json_schema_extra={"example": 100.0})
    total_phenols: float = Field(..., json_schema_extra={"example": 2.5})
    flavanoids: float = Field(..., json_schema_extra={"example": 2.0})
    nonflavanoid_phenols: float = Field(..., json_schema_extra={"example": 0.3})
    proanthocyanins: float = Field(..., json_schema_extra={"example": 1.5})
    color_intensity: float = Field(..., json_schema_extra={"example": 5.0})
    hue: float = Field(..., json_schema_extra={"example": 1.0})
    od280_od315_of_diluted_wines: float = Field(..., json_schema_extra={"example": 2.5})
    proline: float = Field(..., json_schema_extra={"example": 750.0})


class PredictionResponse(BaseModel):
    """
    Response returned by the /predict endpoint.
    """

    predicted_class: int
    class_name: str
    confidence: float