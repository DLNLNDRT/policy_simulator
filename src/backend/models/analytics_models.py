"""
Analytics data models for Policy Simulation Assistant
Defines Pydantic models for advanced analytics, report generation, and visualization.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Tuple, Union
from datetime import datetime
from enum import Enum

class TrendDirection(str, Enum):
    """Trend direction enumeration"""
    INCREASING = "increasing"
    DECREASING = "decreasing"
    STABLE = "stable"

class ChartType(str, Enum):
    """Chart type enumeration"""
    LINE = "line"
    BAR = "bar"
    SCATTER = "scatter"
    HEATMAP = "heatmap"
    BOX = "box"
    HISTOGRAM = "histogram"
    PIE = "pie"
    AREA = "area"
    RADAR = "radar"
    BUBBLE = "bubble"

class ReportTemplate(str, Enum):
    """Report template enumeration"""
    EXECUTIVE_SUMMARY = "executive_summary"
    DETAILED_ANALYSIS = "detailed_analysis"
    POLICY_BRIEF = "policy_brief"
    RESEARCH_REPORT = "research_report"

class ExportFormat(str, Enum):
    """Export format enumeration"""
    PDF = "pdf"
    DOCX = "docx"
    PPTX = "pptx"
    PNG = "png"
    SVG = "svg"
    HTML = "html"

# Trend Analysis Models
class TrendAnalysisRequest(BaseModel):
    """Request model for trend analysis"""
    indicator: str = Field(..., description="Health indicator to analyze")
    country: str = Field(..., description="Country code to analyze")
    time_period: Optional[Tuple[int, int]] = Field(None, description="Optional time period (start_year, end_year)")
    
    @validator('indicator')
    def validate_indicator(cls, v):
        """Validate indicator name"""
        valid_indicators = ['life_expectancy', 'doctor_density', 'nurse_density', 'government_spending']
        if v not in valid_indicators:
            raise ValueError(f'Indicator must be one of: {", ".join(valid_indicators)}')
        return v
    
    @validator('country')
    def validate_country(cls, v):
        """Validate country code"""
        if not v.isalpha() or len(v) != 3:
            raise ValueError('Country must be a valid ISO3 code')
        return v.upper()

class ConfidenceInterval(BaseModel):
    """Confidence interval model"""
    lower: float = Field(..., description="Lower confidence bound")
    upper: float = Field(..., description="Upper confidence bound")

class DataPoint(BaseModel):
    """Data point model"""
    year: int = Field(..., description="Year")
    value: float = Field(..., description="Value")

class TimePeriod(BaseModel):
    """Time period model"""
    start: int = Field(..., description="Start year")
    end: int = Field(..., description="End year")

class TrendAnalysisResponse(BaseModel):
    """Response model for trend analysis"""
    indicator: str = Field(..., description="Health indicator analyzed")
    country: str = Field(..., description="Country code analyzed")
    time_period: TimePeriod = Field(..., description="Time period analyzed")
    trend_direction: TrendDirection = Field(..., description="Direction of trend")
    trend_strength: float = Field(..., description="Strength of trend (0-1)")
    annual_change: float = Field(..., description="Annual change in indicator")
    total_change: float = Field(..., description="Total change over time period")
    change_percentage: float = Field(..., description="Percentage change")
    statistical_significance: float = Field(..., description="Statistical significance (p-value)")
    confidence_interval: ConfidenceInterval = Field(..., description="Confidence interval for trend")
    r_squared: float = Field(..., description="R-squared value")
    sample_size: int = Field(..., description="Sample size")
    data_points: List[DataPoint] = Field(..., description="Data points used in analysis")
    response_time_ms: int = Field(..., description="Response time in milliseconds")
    generated_at: float = Field(..., description="Generation timestamp")

# Correlation Analysis Models
class CorrelationAnalysisRequest(BaseModel):
    """Request model for correlation analysis"""
    indicators: List[str] = Field(..., description="List of indicators to correlate", min_items=2)
    countries: Optional[List[str]] = Field(None, description="Optional list of countries to include")
    time_period: Optional[Tuple[int, int]] = Field(None, description="Optional time period")
    
    @validator('indicators')
    def validate_indicators(cls, v):
        """Validate indicators list"""
        valid_indicators = ['life_expectancy', 'doctor_density', 'nurse_density', 'government_spending']
        for indicator in v:
            if indicator not in valid_indicators:
                raise ValueError(f'Indicator {indicator} must be one of: {", ".join(valid_indicators)}')
        return v

class CorrelationAnalysisResponse(BaseModel):
    """Response model for correlation analysis"""
    indicators: List[str] = Field(..., description="Indicators analyzed")
    countries: Optional[List[str]] = Field(None, description="Countries included")
    time_period: Optional[Tuple[int, int]] = Field(None, description="Time period analyzed")
    correlation_matrix: List[List[float]] = Field(..., description="Correlation matrix")
    significance_matrix: List[List[float]] = Field(..., description="Significance matrix (p-values)")
    interpretation: str = Field(..., description="Interpretation of results")
    sample_size: int = Field(..., description="Sample size")
    response_time_ms: int = Field(..., description="Response time in milliseconds")
    generated_at: str = Field(..., description="Generation timestamp")

# Forecast Models
class ForecastRequest(BaseModel):
    """Request model for forecasting"""
    indicator: str = Field(..., description="Health indicator to forecast")
    country: str = Field(..., description="Country code")
    forecast_years: int = Field(5, description="Number of years to forecast", ge=1, le=20)
    confidence_level: float = Field(0.95, description="Confidence level for prediction intervals", ge=0.5, le=0.99)

class ModelPerformance(BaseModel):
    """Model performance metrics"""
    r_squared: float = Field(..., description="R-squared value")
    rmse: float = Field(..., description="Root mean square error")
    trend_slope: float = Field(..., description="Trend slope")
    intercept: float = Field(..., description="Model intercept")

class ForecastDataPoint(BaseModel):
    """Forecast data point"""
    year: int = Field(..., description="Forecast year")
    predicted_value: float = Field(..., description="Predicted value")
    confidence_interval: ConfidenceInterval = Field(..., description="Confidence interval")

class HistoricalDataPoint(BaseModel):
    """Historical data point"""
    year: int = Field(..., description="Year")
    value: float = Field(..., description="Value")

class ForecastResponse(BaseModel):
    """Response model for forecasting"""
    indicator: str = Field(..., description="Health indicator forecasted")
    country: str = Field(..., description="Country code")
    forecast_years: int = Field(..., description="Number of years forecasted")
    confidence_level: float = Field(..., description="Confidence level used")
    model_performance: ModelPerformance = Field(..., description="Model performance metrics")
    historical_data: List[HistoricalDataPoint] = Field(..., description="Historical data used")
    forecast_data: List[ForecastDataPoint] = Field(..., description="Forecast data points")
    response_time_ms: int = Field(..., description="Response time in milliseconds")
    generated_at: str = Field(..., description="Generation timestamp")

# Statistical Test Models
class StatisticalTestRequest(BaseModel):
    """Request model for statistical significance test"""
    indicator: str = Field(..., description="Health indicator to compare")
    country1: str = Field(..., description="First country code")
    country2: str = Field(..., description="Second country code")
    time_period: Optional[Tuple[int, int]] = Field(None, description="Optional time period")

class TestResults(BaseModel):
    """Statistical test results"""
    t_statistic: float = Field(..., description="T-statistic")
    p_value: float = Field(..., description="P-value")
    significance_level: str = Field(..., description="Significance level interpretation")
    cohens_d: float = Field(..., description="Cohen's d effect size")
    effect_size_interpretation: str = Field(..., description="Effect size interpretation")

class DescriptiveStatistics(BaseModel):
    """Descriptive statistics for a country"""
    mean: float = Field(..., description="Mean value")
    std: float = Field(..., description="Standard deviation")
    n: int = Field(..., description="Sample size")

class CountryStatistics(BaseModel):
    """Statistics for both countries"""
    country1: DescriptiveStatistics = Field(..., description="Statistics for first country")
    country2: DescriptiveStatistics = Field(..., description="Statistics for second country")

class StatisticalTestResponse(BaseModel):
    """Response model for statistical significance test"""
    indicator: str = Field(..., description="Health indicator compared")
    country1: str = Field(..., description="First country code")
    country2: str = Field(..., description="Second country code")
    time_period: Optional[Tuple[int, int]] = Field(None, description="Time period analyzed")
    test_results: TestResults = Field(..., description="Statistical test results")
    descriptive_statistics: CountryStatistics = Field(..., description="Descriptive statistics")
    interpretation: str = Field(..., description="Interpretation of results")
    response_time_ms: int = Field(..., description="Response time in milliseconds")
    generated_at: str = Field(..., description="Generation timestamp")

# Regression Analysis Models
class RegressionAnalysisRequest(BaseModel):
    """Request model for regression analysis"""
    target_indicator: str = Field(..., description="Target variable for regression")
    predictor_indicators: List[str] = Field(..., description="List of predictor variables", min_items=1)
    countries: Optional[List[str]] = Field(None, description="Optional list of countries to include")
    time_period: Optional[Tuple[int, int]] = Field(None, description="Optional time period")

class RegressionModelPerformance(BaseModel):
    """Regression model performance metrics"""
    r_squared: float = Field(..., description="R-squared value")
    adjusted_r_squared: float = Field(..., description="Adjusted R-squared value")
    mse: float = Field(..., description="Mean square error")
    rmse: float = Field(..., description="Root mean square error")
    intercept: float = Field(..., description="Model intercept")

class CoefficientSignificance(BaseModel):
    """Coefficient significance information"""
    coefficient: float = Field(..., description="Coefficient value")
    std_error: Optional[float] = Field(None, description="Standard error")
    t_statistic: Optional[float] = Field(None, description="T-statistic")
    p_value: Optional[float] = Field(None, description="P-value")
    significant: bool = Field(..., description="Whether coefficient is significant")

class RegressionAnalysisResponse(BaseModel):
    """Response model for regression analysis"""
    target_indicator: str = Field(..., description="Target variable")
    predictor_indicators: List[str] = Field(..., description="Predictor variables")
    countries: Optional[List[str]] = Field(None, description="Countries included")
    time_period: Optional[Tuple[int, int]] = Field(None, description="Time period analyzed")
    model_performance: RegressionModelPerformance = Field(..., description="Model performance metrics")
    feature_importance: Dict[str, float] = Field(..., description="Feature importance scores")
    coefficient_significance: Dict[str, CoefficientSignificance] = Field(..., description="Coefficient significance")
    sample_size: int = Field(..., description="Sample size")
    degrees_of_freedom: int = Field(..., description="Degrees of freedom")
    interpretation: str = Field(..., description="Interpretation of results")
    response_time_ms: int = Field(..., description="Response time in milliseconds")
    generated_at: str = Field(..., description="Generation timestamp")

# Report Generation Models
class ReportGenerationRequest(BaseModel):
    """Request model for report generation"""
    template: ReportTemplate = Field(..., description="Report template to use")
    title: str = Field(..., description="Report title")
    simulation_data: Optional[Dict[str, Any]] = Field(None, description="Simulation data to include")
    analytics_data: Optional[Dict[str, Any]] = Field(None, description="Analytics data to include")
    data_sources: Optional[List[str]] = Field(None, description="Data sources to cite")
    config: Dict[str, Any] = Field(default_factory=dict, description="Report configuration")

class ReportMetadata(BaseModel):
    """Report metadata"""
    generated_at: str = Field(..., description="Generation timestamp")
    template: str = Field(..., description="Template used")
    sections_count: int = Field(..., description="Number of sections")

class ReportGenerationResponse(BaseModel):
    """Response model for report generation"""
    report_id: str = Field(..., description="Unique report identifier")
    title: str = Field(..., description="Report title")
    format: str = Field(..., description="Report format")
    content: str = Field(..., description="Report content (HTML)")
    metadata: ReportMetadata = Field(..., description="Report metadata")
    response_time_ms: int = Field(..., description="Response time in milliseconds")
    generated_at: float = Field(..., description="Generation timestamp")

# Visualization Models
class VisualizationRequest(BaseModel):
    """Request model for visualization creation"""
    chart_type: ChartType = Field(..., description="Type of chart to create")
    title: str = Field(..., description="Chart title")
    data: Dict[str, Any] = Field(..., description="Data for visualization")
    config: Dict[str, Any] = Field(default_factory=dict, description="Chart configuration")
    chart_spec: Optional[Dict[str, Any]] = Field(None, description="Custom chart specification")

class VisualizationResponse(BaseModel):
    """Response model for visualization creation"""
    chart_id: str = Field(..., description="Unique chart identifier")
    chart_type: ChartType = Field(..., description="Type of chart created")
    data: Dict[str, Any] = Field(..., description="Chart data")
    config: Dict[str, Any] = Field(..., description="Chart configuration")
    analysis: Dict[str, Any] = Field(default_factory=dict, description="Chart analysis")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Chart metadata")
    response_time_ms: int = Field(..., description="Response time in milliseconds")
    generated_at: float = Field(..., description="Generation timestamp")

# Dashboard Models
class DashboardComponent(BaseModel):
    """Dashboard component configuration"""
    type: str = Field(..., description="Component type")
    title: str = Field(..., description="Component title")
    data_source: str = Field(..., description="Data source for component")
    position: Dict[str, int] = Field(default_factory=dict, description="Component position")
    size: Dict[str, int] = Field(default_factory=dict, description="Component size")
    styling: Dict[str, Any] = Field(default_factory=dict, description="Component styling")
    filters: List[str] = Field(default_factory=list, description="Component filters")

class DashboardRequest(BaseModel):
    """Request model for dashboard creation"""
    title: str = Field(..., description="Dashboard title")
    components: List[DashboardComponent] = Field(..., description="Dashboard components")
    dashboard_config: Dict[str, Any] = Field(..., description="Dashboard configuration")
    data_sources: Dict[str, Any] = Field(..., description="Data sources for components")

class DashboardResponse(BaseModel):
    """Response model for dashboard creation"""
    dashboard_id: str = Field(..., description="Unique dashboard identifier")
    dashboard: Dict[str, Any] = Field(..., description="Dashboard configuration")
    export_options: Dict[str, Any] = Field(..., description="Export options")
    metadata: Dict[str, Any] = Field(..., description="Dashboard metadata")
    response_time_ms: int = Field(..., description="Response time in milliseconds")
    generated_at: float = Field(..., description="Generation timestamp")

# Analytics Summary Models
class AnalyticsSummary(BaseModel):
    """Analytics summary model"""
    total_analyses: int = Field(..., description="Total number of analyses performed")
    trend_analyses: int = Field(..., description="Number of trend analyses")
    correlation_analyses: int = Field(..., description="Number of correlation analyses")
    forecasts: int = Field(..., description="Number of forecasts generated")
    statistical_tests: int = Field(..., description="Number of statistical tests")
    regression_analyses: int = Field(..., description="Number of regression analyses")
    reports_generated: int = Field(..., description="Number of reports generated")
    visualizations_created: int = Field(..., description="Number of visualizations created")
    dashboards_built: int = Field(..., description="Number of dashboards built")
    avg_response_time_ms: float = Field(..., description="Average response time")
    last_updated: datetime = Field(..., description="Last update timestamp")

class AnalyticsHealth(BaseModel):
    """Analytics system health model"""
    status: str = Field(..., description="System status")
    uptime_percentage: float = Field(..., description="System uptime percentage")
    error_rate: float = Field(..., description="Error rate")
    active_connections: int = Field(..., description="Active connections")
    memory_usage: float = Field(..., description="Memory usage percentage")
    cpu_usage: float = Field(..., description="CPU usage percentage")
    last_health_check: datetime = Field(..., description="Last health check timestamp")
