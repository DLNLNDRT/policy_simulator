"""
AI service data models
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime


class NarrativeRequest(BaseModel):
    """AI narrative generation request"""
    country: str = Field(..., description="ISO3 country code", min_length=3, max_length=3)
    simulation_type: str = Field(..., description="Type of simulation", max_length=50)
    baseline_data: Dict[str, Any] = Field(..., description="Baseline health data")
    simulation_params: Dict[str, Any] = Field(..., description="Simulation parameters")
    predicted_outcome: Dict[str, Any] = Field(..., description="Predicted outcome")
    confidence_interval: Dict[str, Any] = Field(..., description="Confidence interval")
    narrative_style: str = Field("professional", description="Narrative style", max_length=20)
    language: str = Field("en", description="Output language", max_length=5)
    
    @validator('narrative_style')
    def validate_narrative_style(cls, v):
        """Validate narrative style"""
        allowed_styles = ["professional", "academic", "policy", "executive"]
        if v not in allowed_styles:
            raise ValueError(f'Narrative style must be one of: {", ".join(allowed_styles)}')
        return v
    
    @validator('language')
    def validate_language(cls, v):
        """Validate language code"""
        allowed_languages = ["en", "es", "fr", "pt"]
        if v not in allowed_languages:
            raise ValueError(f'Language must be one of: {", ".join(allowed_languages)}')
        return v


class NarrativeResponse(BaseModel):
    """AI narrative generation response"""
    narrative: str = Field(..., description="Generated narrative text")
    disclaimers: List[str] = Field(..., description="Safety disclaimers")
    citations: List[str] = Field(..., description="Data source citations")
    methodology: str = Field(..., description="Methodology explanation")
    limitations: List[str] = Field(..., description="Limitations and caveats")
    cost_usd: float = Field(..., description="Generation cost in USD")
    generation_time_ms: int = Field(..., description="Generation time in milliseconds")
    model_used: str = Field(..., description="AI model used")
    tokens_used: Dict[str, int] = Field(..., description="Token usage statistics")


class NarrativeValidationRequest(BaseModel):
    """Narrative validation request"""
    narrative: str = Field(..., description="Narrative text to validate")
    context: Dict[str, Any] = Field(..., description="Validation context")
    validation_type: str = Field("safety", description="Type of validation", max_length=20)
    
    @validator('validation_type')
    def validate_validation_type(cls, v):
        """Validate validation type"""
        allowed_types = ["safety", "accuracy", "completeness", "compliance"]
        if v not in allowed_types:
            raise ValueError(f'Validation type must be one of: {", ".join(allowed_types)}')
        return v


class NarrativeValidationResponse(BaseModel):
    """Narrative validation response"""
    is_valid: bool = Field(..., description="Whether narrative is valid")
    score: float = Field(..., description="Validation score", ge=0, le=1)
    issues: List[Dict[str, Any]] = Field(default_factory=list, description="Validation issues")
    recommendations: List[str] = Field(default_factory=list, description="Improvement recommendations")
    safety_flags: List[str] = Field(default_factory=list, description="Safety concerns")
    compliance_status: Dict[str, bool] = Field(..., description="Compliance status by rule")


class AIHealthStatus(BaseModel):
    """AI service health status"""
    status: str = Field(..., description="Overall health status")
    services: Dict[str, Dict[str, Any]] = Field(..., description="Individual service status")
    last_check: datetime = Field(..., description="Last health check timestamp")
    response_times: Dict[str, float] = Field(..., description="Service response times")
    error_rates: Dict[str, float] = Field(..., description="Service error rates")


class AICostStats(BaseModel):
    """AI cost statistics"""
    total_cost_usd: float = Field(..., description="Total cost in USD")
    total_requests: int = Field(..., description="Total number of requests")
    avg_cost_per_request: float = Field(..., description="Average cost per request")
    cost_by_service: Dict[str, float] = Field(..., description="Cost breakdown by service")
    cost_by_country: Dict[str, float] = Field(..., description="Cost breakdown by country")
    daily_costs: List[Dict[str, Any]] = Field(..., description="Daily cost history")
    budget_usage: float = Field(..., description="Budget usage percentage")


class PromptTemplate(BaseModel):
    """AI prompt template"""
    name: str = Field(..., description="Template name")
    version: str = Field(..., description="Template version")
    system_prompt: str = Field(..., description="System prompt")
    user_prompt_template: str = Field(..., description="User prompt template")
    parameters: List[str] = Field(..., description="Required parameters")
    max_tokens: int = Field(..., description="Maximum tokens")
    temperature: float = Field(..., description="Temperature setting", ge=0, le=2)
    safety_checks: List[str] = Field(..., description="Safety check requirements")


class AIUsageMetrics(BaseModel):
    """AI usage metrics"""
    service_name: str = Field(..., description="AI service name")
    requests_count: int = Field(..., description="Number of requests")
    successful_requests: int = Field(..., description="Successful requests")
    failed_requests: int = Field(..., description="Failed requests")
    total_tokens: int = Field(..., description="Total tokens used")
    total_cost_usd: float = Field(..., description="Total cost in USD")
    avg_response_time_ms: float = Field(..., description="Average response time")
    error_rate: float = Field(..., description="Error rate percentage")
    last_updated: datetime = Field(..., description="Last metrics update")


class AIConfiguration(BaseModel):
    """AI service configuration"""
    openai_enabled: bool = Field(True, description="OpenAI service enabled")
    anthropic_enabled: bool = Field(False, description="Anthropic service enabled")
    default_model: str = Field("gpt-4", description="Default AI model")
    fallback_model: str = Field("gpt-3.5-turbo", description="Fallback AI model")
    max_retries: int = Field(3, description="Maximum retry attempts")
    timeout_seconds: int = Field(30, description="Request timeout")
    rate_limit_per_minute: int = Field(60, description="Rate limit per minute")
    cost_limit_per_hour: float = Field(10.0, description="Cost limit per hour in USD")
