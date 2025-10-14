"""
Benchmark dashboard data models
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime
from enum import Enum


class MetricType(str, Enum):
    """Health metric types"""
    LIFE_EXPECTANCY = "life_expectancy"
    DOCTOR_DENSITY = "doctor_density"
    NURSE_DENSITY = "nurse_density"
    HEALTH_SPENDING = "health_spending"


class TrendDirection(str, Enum):
    """Trend direction indicators"""
    UP = "up"
    DOWN = "down"
    STABLE = "stable"


class AnomalySeverity(str, Enum):
    """Anomaly severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class HealthMetric(BaseModel):
    """Individual health metric with ranking and trend"""
    name: str = Field(..., description="Metric name")
    value: float = Field(..., description="Metric value")
    unit: str = Field(..., description="Unit of measurement")
    rank: int = Field(..., description="Rank among compared countries")
    percentile: float = Field(..., description="Percentile (0-100)")
    trend: TrendDirection = Field(..., description="Trend direction")
    anomaly: bool = Field(False, description="Whether this is an anomaly")
    baseline_year: int = Field(..., description="Baseline year for comparison")


class CountryRanking(BaseModel):
    """Country ranking information"""
    country_code: str = Field(..., description="ISO3 country code")
    country_name: str = Field(..., description="Country name")
    overall_rank: int = Field(..., description="Overall ranking")
    metrics: List[HealthMetric] = Field(..., description="Individual metric rankings")
    total_score: float = Field(..., description="Composite score")


class AnomalyAlert(BaseModel):
    """Anomaly detection alert"""
    country: str = Field(..., description="Country code")
    metric: str = Field(..., description="Metric name")
    severity: AnomalySeverity = Field(..., description="Severity level")
    description: str = Field(..., description="Anomaly description")
    confidence: float = Field(..., description="Confidence score (0-1)")
    recommendation: str = Field(..., description="Recommended action")
    detected_at: datetime = Field(default_factory=datetime.now, description="Detection timestamp")


class PeerGroup(BaseModel):
    """Peer group definition and analysis"""
    name: str = Field(..., description="Peer group name")
    countries: List[str] = Field(..., description="Country codes in group")
    criteria: List[str] = Field(..., description="Grouping criteria")
    average: Dict[str, float] = Field(..., description="Average values by metric")
    size: int = Field(..., description="Number of countries in group")


class ComparisonRequest(BaseModel):
    """Request for country comparison"""
    countries: List[str] = Field(..., description="List of country codes to compare", min_items=2, max_items=4)
    metrics: Optional[List[MetricType]] = Field(None, description="Specific metrics to compare")
    year: Optional[int] = Field(2022, description="Year for comparison")
    include_anomalies: bool = Field(True, description="Include anomaly detection")
    include_peers: bool = Field(True, description="Include peer group analysis")
    
    @validator('countries')
    def validate_countries(cls, v):
        """Validate country codes"""
        if len(v) != len(set(v)):
            raise ValueError('Duplicate countries not allowed')
        return v


class CountryComparison(BaseModel):
    """Complete country comparison result"""
    countries: List[str] = Field(..., description="Compared countries")
    metrics: List[MetricType] = Field(..., description="Compared metrics")
    year: int = Field(..., description="Comparison year")
    rankings: List[CountryRanking] = Field(..., description="Country rankings")
    anomalies: List[AnomalyAlert] = Field(..., description="Detected anomalies")
    peer_groups: List[PeerGroup] = Field(..., description="Peer group analysis")
    summary: Dict[str, Any] = Field(..., description="Comparison summary")
    generated_at: datetime = Field(default_factory=datetime.now, description="Generation timestamp")


class AnomalyDetectionRequest(BaseModel):
    """Request for anomaly detection"""
    country: Optional[str] = Field(None, description="Specific country to analyze")
    metric: Optional[MetricType] = Field(None, description="Specific metric to analyze")
    timeframe: int = Field(5, description="Years to look back for trend analysis", ge=1, le=10)
    sensitivity: float = Field(2.0, description="Sensitivity threshold (standard deviations)", ge=1.0, le=3.0)


class AnomalyDetectionResponse(BaseModel):
    """Anomaly detection results"""
    anomalies: List[AnomalyAlert] = Field(..., description="Detected anomalies")
    total_analyzed: int = Field(..., description="Total data points analyzed")
    detection_confidence: float = Field(..., description="Overall detection confidence")
    parameters: AnomalyDetectionRequest = Field(..., description="Detection parameters")
    generated_at: datetime = Field(default_factory=datetime.now, description="Detection timestamp")


class PeerGroupRequest(BaseModel):
    """Request for peer group analysis"""
    country: str = Field(..., description="Country to find peers for")
    criteria: List[str] = Field(["gdp_per_capita", "population"], description="Grouping criteria")
    max_peers: int = Field(5, description="Maximum number of peers", ge=2, le=10)
    similarity_threshold: float = Field(0.7, description="Minimum similarity score", ge=0.0, le=1.0)


class PeerGroupResponse(BaseModel):
    """Peer group analysis results"""
    target_country: str = Field(..., description="Target country")
    peer_groups: List[PeerGroup] = Field(..., description="Identified peer groups")
    best_match: Optional[PeerGroup] = Field(None, description="Best matching peer group")
    similarity_scores: Dict[str, float] = Field(..., description="Similarity scores by country")
    generated_at: datetime = Field(default_factory=datetime.now, description="Analysis timestamp")


class BenchmarkStats(BaseModel):
    """Benchmark dashboard statistics"""
    total_countries: int = Field(..., description="Total countries available")
    total_metrics: int = Field(..., description="Total metrics tracked")
    last_updated: datetime = Field(..., description="Last data update")
    anomaly_alerts: int = Field(..., description="Active anomaly alerts")
    peer_groups: int = Field(..., description="Available peer groups")
    data_quality_score: float = Field(..., description="Overall data quality score")


class ExportRequest(BaseModel):
    """Request for data export"""
    format: Literal["json", "csv", "pdf"] = Field("json", description="Export format")
    countries: List[str] = Field(..., description="Countries to export")
    metrics: List[MetricType] = Field(..., description="Metrics to export")
    include_charts: bool = Field(True, description="Include visualizations")
    include_anomalies: bool = Field(True, description="Include anomaly data")


class ExportResponse(BaseModel):
    """Export response"""
    download_url: str = Field(..., description="Download URL for exported data")
    file_size: int = Field(..., description="File size in bytes")
    expires_at: datetime = Field(..., description="Download link expiration")
    format: str = Field(..., description="Export format")
    generated_at: datetime = Field(default_factory=datetime.now, description="Export timestamp")
