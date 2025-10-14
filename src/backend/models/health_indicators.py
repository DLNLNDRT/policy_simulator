"""
Health indicators data models
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime


class HealthIndicatorBase(BaseModel):
    """Base health indicator model"""
    country: str = Field(..., description="ISO3 country code", min_length=3, max_length=3)
    year: int = Field(..., description="Year", ge=1990, le=2024)
    metric_name: str = Field(..., description="Health metric name", max_length=100)
    value: float = Field(..., description="Metric value")
    unit: Optional[str] = Field(None, description="Unit of measurement", max_length=50)
    source: Optional[str] = Field(None, description="Data source", max_length=200)
    quality_score: float = Field(100.0, description="Data quality score", ge=0, le=100)


class HealthIndicatorCreate(HealthIndicatorBase):
    """Health indicator creation model"""
    pass


class HealthIndicatorUpdate(BaseModel):
    """Health indicator update model"""
    value: Optional[float] = None
    unit: Optional[str] = None
    source: Optional[str] = None
    quality_score: Optional[float] = Field(None, ge=0, le=100)


class HealthIndicatorResponse(HealthIndicatorBase):
    """Health indicator response model"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class CountryMetrics(BaseModel):
    """Country-specific health metrics"""
    life_expectancy: Optional[float] = Field(None, description="Life expectancy in years")
    doctor_density: Optional[float] = Field(None, description="Doctors per 10,000 population")
    nurse_density: Optional[float] = Field(None, description="Nurses per 10,000 population")
    pharmacist_density: Optional[float] = Field(None, description="Pharmacists per 10,000 population")
    government_spending: Optional[float] = Field(None, description="Health spending as % of GDP")
    access_to_medicine: Optional[float] = Field(None, description="Access to affordable medicine %")
    population_density: Optional[float] = Field(None, description="Population density per km²")


class HealthIndicatorRequest(BaseModel):
    """Health indicator query request"""
    country: Optional[str] = Field(None, description="ISO3 country code")
    year: Optional[int] = Field(None, description="Year", ge=1990, le=2024)
    metric_name: Optional[str] = Field(None, description="Metric name filter")
    limit: int = Field(100, description="Maximum results", ge=1, le=1000)
    offset: int = Field(0, description="Results offset", ge=0)


class CountryIndicatorsResponse(BaseModel):
    """Country indicators response model"""
    country: str = Field(..., description="ISO3 country code")
    year: int = Field(..., description="Year")
    metrics: CountryMetrics = Field(..., description="Country health metrics")
    data_quality: Dict[str, float] = Field(..., description="Data quality scores by metric")
    last_updated: datetime = Field(..., description="Last data update timestamp")
    sources: Dict[str, str] = Field(..., description="Data sources by metric")


class DataQualityMetrics(BaseModel):
    """Data quality metrics model"""
    overall_score: float = Field(..., description="Overall data quality score", ge=0, le=100)
    completeness: float = Field(..., description="Data completeness percentage", ge=0, le=100)
    validity: float = Field(..., description="Data validity percentage", ge=0, le=100)
    consistency: float = Field(..., description="Data consistency percentage", ge=0, le=100)
    freshness: float = Field(..., description="Data freshness score", ge=0, le=100)
    country_coverage: int = Field(..., description="Number of countries with data")
    year_coverage: Dict[str, int] = Field(..., description="Year coverage by metric")
    issues: List[Dict[str, Any]] = Field(default_factory=list, description="Data quality issues")


class HealthIndicatorStats(BaseModel):
    """Health indicator statistics"""
    total_records: int = Field(..., description="Total number of records")
    countries_count: int = Field(..., description="Number of countries")
    metrics_count: int = Field(..., description="Number of unique metrics")
    years_covered: List[int] = Field(..., description="Years with data")
    avg_quality_score: float = Field(..., description="Average quality score")
    last_updated: datetime = Field(..., description="Last update timestamp")


class MetricValidation(BaseModel):
    """Metric validation rules"""
    metric_name: str = Field(..., description="Metric name")
    min_value: Optional[float] = Field(None, description="Minimum valid value")
    max_value: Optional[float] = Field(None, description="Maximum valid value")
    required_unit: Optional[str] = Field(None, description="Required unit")
    validation_rules: List[str] = Field(default_factory=list, description="Validation rules")


class HealthIndicatorValidation(BaseModel):
    """Health indicator validation result"""
    is_valid: bool = Field(..., description="Whether the indicator is valid")
    errors: List[str] = Field(default_factory=list, description="Validation errors")
    warnings: List[str] = Field(default_factory=list, description="Validation warnings")
    quality_score: float = Field(..., description="Calculated quality score", ge=0, le=100)
