"""
Data Quality Assurance data models
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum

class QualityAlertType(str, Enum):
    COMPLETENESS = "completeness"
    VALIDITY = "validity"
    CONSISTENCY = "consistency"
    FRESHNESS = "freshness"

class QualityAlertSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ValidationStatus(str, Enum):
    PASS = "pass"
    WARNING = "warning"
    FAIL = "fail"

class ProcessingStepType(str, Enum):
    DATA_INGESTION = "data_ingestion"
    DATA_CLEANING = "data_cleaning"
    DATA_TRANSFORMATION = "data_transformation"
    DATA_VALIDATION = "data_validation"
    DATA_AGGREGATION = "data_aggregation"
    MODEL_TRAINING = "model_training"
    SIMULATION_EXECUTION = "simulation_execution"

class DataSourceType(str, Enum):
    WHO_GLOBAL_HEALTH = "who_global_health"
    WORLD_BANK = "world_bank"
    OECD_HEALTH = "oecd_health"
    NATIONAL_STATISTICS = "national_statistics"
    INTERNAL_PROCESSING = "internal_processing"

class QualityAlert(BaseModel):
    """Quality alert model"""
    id: str = Field(..., description="Unique alert identifier")
    type: QualityAlertType = Field(..., description="Type of quality issue")
    severity: QualityAlertSeverity = Field(..., description="Severity level")
    message: str = Field(..., description="Alert message")
    affected_indicators: List[str] = Field(default_factory=list, description="Affected health indicators")
    affected_countries: Optional[List[str]] = Field(None, description="Affected countries")
    created_at: datetime = Field(..., description="Alert creation timestamp")
    resolved: bool = Field(default=False, description="Whether alert is resolved")
    resolved_at: Optional[datetime] = Field(None, description="Alert resolution timestamp")
    recommendations: List[str] = Field(default_factory=list, description="Recommended actions")

class QualityMetrics(BaseModel):
    """Overall quality metrics model"""
    overall_score: float = Field(..., description="Overall quality score (0-100)", ge=0, le=100)
    completeness_score: float = Field(..., description="Data completeness score (0-100)", ge=0, le=100)
    validity_score: float = Field(..., description="Data validity score (0-100)", ge=0, le=100)
    consistency_score: float = Field(..., description="Data consistency score (0-100)", ge=0, le=100)
    freshness_score: float = Field(..., description="Data freshness score (0-100)", ge=0, le=100)
    last_updated: datetime = Field(..., description="Last update timestamp")
    trend: str = Field(..., description="Quality trend", regex="^(up|down|stable)$")
    alerts: List[QualityAlert] = Field(default_factory=list, description="Active quality alerts")

class QualityBreakdown(BaseModel):
    """Quality breakdown by various dimensions"""
    by_indicator: Dict[str, float] = Field(..., description="Quality scores by health indicator")
    by_country: Dict[str, float] = Field(..., description="Quality scores by country")
    by_source: Dict[str, float] = Field(..., description="Quality scores by data source")
    by_time_period: Dict[str, float] = Field(..., description="Quality scores by time period")

class ValidationCheck(BaseModel):
    """Individual validation check result"""
    status: ValidationStatus = Field(..., description="Validation status")
    score: float = Field(..., description="Validation score (0-100)", ge=0, le=100)
    details: str = Field(..., description="Validation details")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")

class ValidationIssue(BaseModel):
    """Validation issue details"""
    type: str = Field(..., description="Issue type")
    severity: QualityAlertSeverity = Field(..., description="Issue severity")
    description: str = Field(..., description="Issue description")
    affected_records: List[str] = Field(default_factory=list, description="Affected data records")
    recommendation: str = Field(..., description="Recommended action")

class ValidationResult(BaseModel):
    """Comprehensive validation result"""
    dataset_id: str = Field(..., description="Dataset identifier")
    validation_timestamp: datetime = Field(..., description="Validation timestamp")
    overall_status: ValidationStatus = Field(..., description="Overall validation status")
    completeness_check: ValidationCheck = Field(..., description="Completeness validation")
    validity_check: ValidationCheck = Field(..., description="Validity validation")
    consistency_check: ValidationCheck = Field(..., description="Consistency validation")
    outlier_check: ValidationCheck = Field(..., description="Outlier detection")
    issues: List[ValidationIssue] = Field(default_factory=list, description="Validation issues")
    quality_score: float = Field(..., description="Overall quality score", ge=0, le=100)
    validation_duration_ms: int = Field(..., description="Validation duration in milliseconds")

class DataSource(BaseModel):
    """Data source information"""
    id: str = Field(..., description="Source identifier")
    name: str = Field(..., description="Source name")
    url: str = Field(..., description="Source URL")
    type: DataSourceType = Field(..., description="Source type")
    reliability_score: float = Field(..., description="Reliability score (0-1)", ge=0, le=1)
    coverage: List[str] = Field(..., description="Covered health indicators")
    last_updated: datetime = Field(..., description="Last update timestamp")
    status: str = Field(default="active", description="Source status")
    version: Optional[str] = Field(None, description="Source version")
    description: Optional[str] = Field(None, description="Source description")

class ProcessingStep(BaseModel):
    """Data processing step"""
    step_id: str = Field(..., description="Step identifier")
    type: ProcessingStepType = Field(..., description="Step type")
    description: str = Field(..., description="Step description")
    timestamp: datetime = Field(..., description="Step timestamp")
    input_data: str = Field(..., description="Input data description")
    output_data: str = Field(..., description="Output data description")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Step parameters")
    duration_ms: int = Field(default=0, description="Step duration in milliseconds")
    success: bool = Field(default=True, description="Step success status")
    error_message: Optional[str] = Field(None, description="Error message if failed")

class DataTransformation(BaseModel):
    """Data transformation information"""
    transformation_id: str = Field(..., description="Transformation identifier")
    name: str = Field(..., description="Transformation name")
    description: str = Field(..., description="Transformation description")
    input_schema: Dict[str, Any] = Field(..., description="Input data schema")
    output_schema: Dict[str, Any] = Field(..., description="Output data schema")
    transformation_logic: str = Field(..., description="Transformation logic description")
    timestamp: datetime = Field(..., description="Transformation timestamp")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Transformation parameters")

class DatasetVersion(BaseModel):
    """Dataset version information"""
    version_id: str = Field(..., description="Version identifier")
    dataset_id: str = Field(..., description="Dataset identifier")
    version_number: str = Field(..., description="Version number")
    created_at: datetime = Field(..., description="Creation timestamp")
    created_by: str = Field(..., description="Created by user")
    changes: List[str] = Field(..., description="List of changes")
    data_hash: str = Field(..., description="Data integrity hash")
    size_bytes: int = Field(..., description="Dataset size in bytes")
    record_count: int = Field(..., description="Number of records")

class AuditEntry(BaseModel):
    """Audit trail entry"""
    entry_id: str = Field(..., description="Audit entry identifier")
    timestamp: datetime = Field(..., description="Entry timestamp")
    action: str = Field(..., description="Action performed")
    user_id: Optional[str] = Field(None, description="User identifier")
    resource_type: str = Field(..., description="Resource type")
    resource_id: str = Field(..., description="Resource identifier")
    details: Dict[str, Any] = Field(default_factory=dict, description="Action details")
    ip_address: Optional[str] = Field(None, description="IP address")

class ProvenanceData(BaseModel):
    """Data provenance information"""
    dataset_id: str = Field(..., description="Dataset identifier")
    original_sources: List[DataSource] = Field(..., description="Original data sources")
    processing_steps: List[ProcessingStep] = Field(default_factory=list, description="Processing steps")
    transformations: List[DataTransformation] = Field(default_factory=list, description="Data transformations")
    version_history: List[DatasetVersion] = Field(default_factory=list, description="Version history")
    audit_trail: List[AuditEntry] = Field(default_factory=list, description="Audit trail")
    created_at: datetime = Field(..., description="Creation timestamp")
    last_updated: datetime = Field(..., description="Last update timestamp")

class QualityOverview(BaseModel):
    """Quality overview response"""
    overall_score: float = Field(..., description="Overall quality score", ge=0, le=100)
    completeness_score: float = Field(..., description="Completeness score", ge=0, le=100)
    validity_score: float = Field(..., description="Validity score", ge=0, le=100)
    consistency_score: float = Field(..., description="Consistency score", ge=0, le=100)
    freshness_score: float = Field(..., description="Freshness score", ge=0, le=100)
    last_updated: datetime = Field(..., description="Last update timestamp")
    trend: str = Field(..., description="Quality trend")
    alerts: List[QualityAlert] = Field(default_factory=list, description="Active alerts")
    data_sources: Dict[str, Dict[str, Any]] = Field(..., description="Data sources status")

class QualityTrend(BaseModel):
    """Quality trend data point"""
    timestamp: datetime = Field(..., description="Trend timestamp")
    overall_score: float = Field(..., description="Overall quality score", ge=0, le=100)
    completeness_score: float = Field(..., description="Completeness score", ge=0, le=100)
    validity_score: float = Field(..., description="Validity score", ge=0, le=100)
    consistency_score: float = Field(..., description="Consistency score", ge=0, le=100)
    freshness_score: float = Field(..., description="Freshness score", ge=0, le=100)
    alert_count: int = Field(..., description="Number of active alerts", ge=0)

class IndicatorQuality(BaseModel):
    """Health indicator quality information"""
    indicator_id: str = Field(..., description="Indicator identifier")
    overall_score: float = Field(..., description="Overall quality score", ge=0, le=100)
    completeness_score: float = Field(..., description="Completeness score", ge=0, le=100)
    validity_score: float = Field(..., description="Validity score", ge=0, le=100)
    consistency_score: float = Field(..., description="Consistency score", ge=0, le=100)
    freshness_score: float = Field(..., description="Freshness score", ge=0, le=100)
    last_updated: datetime = Field(..., description="Last update timestamp")
    trend: str = Field(..., description="Quality trend")
    coverage: Dict[str, Any] = Field(..., description="Data coverage information")
    issues: List[ValidationIssue] = Field(default_factory=list, description="Quality issues")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")

class CountryQuality(BaseModel):
    """Country quality information"""
    country_code: str = Field(..., description="Country code")
    country_name: str = Field(..., description="Country name")
    overall_score: float = Field(..., description="Overall quality score", ge=0, le=100)
    completeness_score: float = Field(..., description="Completeness score", ge=0, le=100)
    validity_score: float = Field(..., description="Validity score", ge=0, le=100)
    consistency_score: float = Field(..., description="Consistency score", ge=0, le=100)
    freshness_score: float = Field(..., description="Freshness score", ge=0, le=100)
    last_updated: datetime = Field(..., description="Last update timestamp")
    trend: str = Field(..., description="Quality trend")
    indicators: Dict[str, Dict[str, Any]] = Field(..., description="Indicator quality details")
    alerts: List[QualityAlert] = Field(default_factory=list, description="Active alerts")
    data_sources: List[DataSource] = Field(default_factory=list, description="Data sources")

class ValidationRequest(BaseModel):
    """Data validation request"""
    dataset_id: str = Field(..., description="Dataset identifier")
    validation_type: str = Field(default="comprehensive", description="Validation type")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Validation parameters")

class AlertResolutionRequest(BaseModel):
    """Quality alert resolution request"""
    resolution_notes: str = Field(default="", description="Resolution notes")

class AlertResolutionResponse(BaseModel):
    """Quality alert resolution response"""
    alert_id: str = Field(..., description="Alert identifier")
    resolved: bool = Field(..., description="Resolution status")
    resolved_at: datetime = Field(..., description="Resolution timestamp")
    resolution_notes: str = Field(..., description="Resolution notes")
    resolved_by: str = Field(..., description="Resolved by user")
    status: str = Field(..., description="Resolution status")

class ProvenanceExportRequest(BaseModel):
    """Provenance data export request"""
    format: str = Field(default="json", description="Export format", regex="^(json|csv)$")

class ProvenanceExportResponse(BaseModel):
    """Provenance data export response"""
    dataset_id: str = Field(..., description="Dataset identifier")
    format: str = Field(..., description="Export format")
    exported_data: str = Field(..., description="Exported data")
    export_timestamp: datetime = Field(..., description="Export timestamp")
    size_bytes: int = Field(..., description="Export size in bytes")

class DataSourcesResponse(BaseModel):
    """Data sources response"""
    summary: Dict[str, Any] = Field(..., description="Sources summary")
    sources: List[DataSource] = Field(..., description="List of data sources")

class QualityTrendsResponse(BaseModel):
    """Quality trends response"""
    trends: List[QualityTrend] = Field(..., description="Quality trends data")
    period_days: int = Field(..., description="Trend period in days")
    generated_at: datetime = Field(..., description="Generation timestamp")
