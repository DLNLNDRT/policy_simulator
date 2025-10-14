"""
Updated simulation models for Feature 1 implementation.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class SimulationParameters(BaseModel):
    doctor_density: float = Field(ge=0, le=10, description="Doctor density per 1,000 population")
    nurse_density: float = Field(ge=0, le=20, description="Nurse density per 1,000 population")
    health_spending: float = Field(ge=0, le=15, description="Government health spending as % of GDP")

class SimulationRequest(BaseModel):
    country: str = Field(..., description="Country code (ISO3)")
    parameters: SimulationParameters

class ConfidenceInterval(BaseModel):
    lower: float
    upper: float
    margin_of_error: float

class FeatureContributions(BaseModel):
    doctor_density: float
    nurse_density: float
    health_spending: float
    intercept: float

class Prediction(BaseModel):
    life_expectancy: float
    change: float
    change_percentage: float
    confidence_interval: ConfidenceInterval
    feature_contributions: FeatureContributions

class BaselineData(BaseModel):
    life_expectancy: float
    doctor_density: float
    nurse_density: float
    health_spending: float
    year: int

class ModelMetrics(BaseModel):
    r2_score: float
    mse: float
    rmse: float
    training_samples: int
    test_samples: int

class SimulationMetadata(BaseModel):
    model_version: str
    execution_time: float
    data_quality: float

class SimulationResponse(BaseModel):
    simulation_id: str
    country: str
    timestamp: str
    baseline: BaselineData
    parameters: SimulationParameters
    prediction: Prediction
    model_metrics: ModelMetrics
    metadata: SimulationMetadata

class CountryInfo(BaseModel):
    code: str
    name: str
    baseline: BaselineData
    data_quality: float

class CountriesResponse(BaseModel):
    countries: List[CountryInfo]

class ModelInfo(BaseModel):
    status: str
    feature_importance: Optional[Dict[str, float]] = None
    metrics: Optional[Dict[str, float]] = None
    model_type: Optional[str] = None
    features: Optional[List[str]] = None
    target: Optional[str] = None
