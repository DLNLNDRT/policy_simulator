"""
Policy simulation data models
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime


class SimulationRequest(BaseModel):
    """Policy simulation request model"""
    country: str = Field(..., description="ISO3 country code", min_length=3, max_length=3)
    doctor_density_change: float = Field(
        ..., 
        description="Change in doctor density (per 10,000 population)",
        ge=-10.0, 
        le=10.0
    )
    nurse_density_change: float = Field(
        ..., 
        description="Change in nurse density (per 10,000 population)",
        ge=-50.0, 
        le=50.0
    )
    spending_change: float = Field(
        ..., 
        description="Change in government health spending (% of GDP)",
        ge=-10.0, 
        le=10.0
    )
    
    @validator('country')
    def validate_country_code(cls, v):
        """Validate ISO3 country code"""
        if not v.isalpha() or len(v) != 3:
            raise ValueError('Country must be a valid ISO3 code')
        return v.upper()
    
    @validator('doctor_density_change', 'nurse_density_change', 'spending_change')
    def validate_realistic_changes(cls, v, field):
        """Validate realistic policy change ranges"""
        if field.name == 'doctor_density_change' and abs(v) > 5.0:
            raise ValueError('Doctor density change should be within ±5 per 10,000')
        elif field.name == 'nurse_density_change' and abs(v) > 20.0:
            raise ValueError('Nurse density change should be within ±20 per 10,000')
        elif field.name == 'spending_change' and abs(v) > 5.0:
            raise ValueError('Spending change should be within ±5% of GDP')
        return v


class BaselineData(BaseModel):
    """Baseline health data for a country"""
    country: str = Field(..., description="ISO3 country code")
    year: int = Field(..., description="Baseline year")
    life_expectancy: float = Field(..., description="Current life expectancy")
    doctor_density: float = Field(..., description="Current doctor density")
    nurse_density: float = Field(..., description="Current nurse density")
    government_spending: float = Field(..., description="Current health spending")
    population: Optional[float] = Field(None, description="Population size")
    gdp_per_capita: Optional[float] = Field(None, description="GDP per capita")


class PredictedOutcome(BaseModel):
    """Predicted simulation outcome"""
    life_expectancy_change: float = Field(..., description="Predicted change in life expectancy (years)")
    life_expectancy_new: float = Field(..., description="Predicted new life expectancy")
    confidence_score: float = Field(..., description="Model confidence score", ge=0, le=1)
    feature_importance: Dict[str, float] = Field(..., description="Feature importance scores")
    model_metadata: Dict[str, Any] = Field(..., description="Model metadata")


class ConfidenceInterval(BaseModel):
    """Confidence interval for predictions"""
    lower_bound: float = Field(..., description="Lower confidence bound")
    upper_bound: float = Field(..., description="Upper confidence bound")
    confidence_level: float = Field(0.95, description="Confidence level", ge=0, le=1)


class SimulationResult(BaseModel):
    """Simulation calculation result"""
    baseline_data: BaselineData = Field(..., description="Baseline health data")
    predicted_outcome: PredictedOutcome = Field(..., description="Predicted outcome")
    confidence_interval: ConfidenceInterval = Field(..., description="Confidence interval")
    model_version: str = Field(..., description="Model version used")
    calculation_time_ms: int = Field(..., description="Calculation time in milliseconds")


class NarrativeResult(BaseModel):
    """AI-generated narrative result"""
    narrative: str = Field(..., description="Generated narrative text")
    disclaimers: List[str] = Field(..., description="Safety disclaimers")
    citations: List[str] = Field(..., description="Data source citations")
    cost_usd: float = Field(..., description="AI generation cost in USD")
    generation_time_ms: int = Field(..., description="Generation time in milliseconds")


class SimulationResponse(BaseModel):
    """Complete simulation response"""
    country: str = Field(..., description="ISO3 country code")
    baseline_data: BaselineData = Field(..., description="Baseline health data")
    simulation_params: Dict[str, Any] = Field(..., description="Simulation parameters")
    predicted_outcome: PredictedOutcome = Field(..., description="Predicted outcome")
    confidence_interval: ConfidenceInterval = Field(..., description="Confidence interval")
    narrative: str = Field(..., description="AI-generated narrative")
    disclaimers: List[str] = Field(..., description="Safety disclaimers")
    citations: List[str] = Field(..., description="Data source citations")
    model_version: str = Field(..., description="Model version used")
    response_time_ms: int = Field(..., description="Total response time")
    cost_usd: float = Field(..., description="Total cost in USD")
    created_at: datetime = Field(default_factory=datetime.now, description="Response timestamp")


class SimulationHistoryResponse(BaseModel):
    """Simulation history response"""
    id: int = Field(..., description="Simulation ID")
    country: str = Field(..., description="ISO3 country code")
    predicted_change: float = Field(..., description="Predicted life expectancy change")
    confidence_score: float = Field(..., description="Model confidence score")
    response_time_ms: int = Field(..., description="Response time")
    cost_usd: float = Field(..., description="Cost in USD")
    created_at: datetime = Field(..., description="Simulation timestamp")


class SimulationStats(BaseModel):
    """Simulation statistics"""
    total_simulations: int = Field(..., description="Total number of simulations")
    unique_countries: int = Field(..., description="Number of unique countries")
    avg_response_time_ms: float = Field(..., description="Average response time")
    avg_cost_usd: float = Field(..., description="Average cost per simulation")
    total_cost_usd: float = Field(..., description="Total cost")
    success_rate: float = Field(..., description="Success rate percentage")
    most_simulated_country: Optional[str] = Field(None, description="Most simulated country")
    last_24h_simulations: int = Field(..., description="Simulations in last 24 hours")


class SimulationValidation(BaseModel):
    """Simulation validation result"""
    is_valid: bool = Field(..., description="Whether simulation is valid")
    errors: List[str] = Field(default_factory=list, description="Validation errors")
    warnings: List[str] = Field(default_factory=list, description="Validation warnings")
    data_availability: Dict[str, bool] = Field(..., description="Data availability by metric")
    quality_score: float = Field(..., description="Overall data quality score")
