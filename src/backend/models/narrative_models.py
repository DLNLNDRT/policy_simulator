"""
Narrative generation data models
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime
from enum import Enum


class NarrativeType(str, Enum):
    """Types of narratives that can be generated"""
    SIMULATION_IMPACT = "simulation_impact"
    BENCHMARK_COMPARISON = "benchmark_comparison"
    ANOMALY_ALERT = "anomaly_alert"
    TREND_ANALYSIS = "trend_analysis"
    EXECUTIVE_SUMMARY = "executive_summary"


class AudienceType(str, Enum):
    """Target audience for narratives"""
    MINISTERS = "ministers"
    NGOS = "ngos"
    RESEARCHERS = "researchers"
    PUBLIC = "public"
    POLICY_MAKERS = "policy_makers"


class ToneType(str, Enum):
    """Narrative tone options"""
    FORMAL = "formal"
    CONVERSATIONAL = "conversational"
    TECHNICAL = "technical"
    PERSUASIVE = "persuasive"


class LengthType(str, Enum):
    """Narrative length options"""
    BRIEF = "brief"  # 1-2 pages
    STANDARD = "standard"  # 3-5 pages
    DETAILED = "detailed"  # 5+ pages


class FocusArea(str, Enum):
    """Focus areas for narratives"""
    ECONOMIC_IMPACT = "economic_impact"
    HEALTH_OUTCOMES = "health_outcomes"
    IMPLEMENTATION = "implementation"
    POLICY_RECOMMENDATIONS = "policy_recommendations"
    RISK_ASSESSMENT = "risk_assessment"


class NarrativeRequest(BaseModel):
    """Request for narrative generation"""
    narrative_type: NarrativeType = Field(..., description="Type of narrative to generate")
    data_source: Dict[str, Any] = Field(..., description="Source data for narrative generation")
    audience: AudienceType = Field(AudienceType.POLICY_MAKERS, description="Target audience")
    tone: ToneType = Field(ToneType.FORMAL, description="Narrative tone")
    length: LengthType = Field(LengthType.STANDARD, description="Narrative length")
    focus_areas: List[FocusArea] = Field(default_factory=list, description="Focus areas to emphasize")
    custom_instructions: Optional[str] = Field(None, description="Additional custom instructions")
    include_citations: bool = Field(True, description="Include source citations")
    include_recommendations: bool = Field(True, description="Include actionable recommendations")
    
    @validator('focus_areas')
    def validate_focus_areas(cls, v):
        """Validate focus areas"""
        if len(v) > 3:
            raise ValueError('Maximum 3 focus areas allowed')
        return v


class NarrativeSection(BaseModel):
    """Individual section of a narrative"""
    title: str = Field(..., description="Section title")
    content: str = Field(..., description="Section content")
    order: int = Field(..., description="Section order")
    word_count: int = Field(..., description="Word count for section")
    key_points: List[str] = Field(default_factory=list, description="Key points in section")


class Citation(BaseModel):
    """Citation for narrative content"""
    source: str = Field(..., description="Source name or title")
    url: Optional[str] = Field(None, description="Source URL")
    date: Optional[str] = Field(None, description="Publication or access date")
    type: str = Field(..., description="Source type (data, research, policy)")
    relevance: str = Field(..., description="Relevance to narrative content")


class Recommendation(BaseModel):
    """Actionable recommendation"""
    title: str = Field(..., description="Recommendation title")
    description: str = Field(..., description="Detailed recommendation")
    priority: Literal["low", "medium", "high"] = Field(..., description="Priority level")
    timeline: Optional[str] = Field(None, description="Recommended timeline")
    resources_needed: Optional[str] = Field(None, description="Required resources")
    expected_impact: Optional[str] = Field(None, description="Expected impact")


class QualityMetrics(BaseModel):
    """Quality metrics for generated narrative"""
    coherence_score: float = Field(..., description="Narrative coherence score", ge=0, le=5)
    accuracy_score: float = Field(..., description="Factual accuracy score", ge=0, le=5)
    actionability_score: float = Field(..., description="Actionability score", ge=0, le=5)
    readability_score: float = Field(..., description="Readability score", ge=0, le=5)
    overall_score: float = Field(..., description="Overall quality score", ge=0, le=5)
    word_count: int = Field(..., description="Total word count")
    reading_time_minutes: int = Field(..., description="Estimated reading time")


class NarrativeResponse(BaseModel):
    """Complete narrative generation response"""
    narrative_id: str = Field(..., description="Unique narrative identifier")
    title: str = Field(..., description="Narrative title")
    narrative_type: NarrativeType = Field(..., description="Type of narrative")
    sections: List[NarrativeSection] = Field(..., description="Narrative sections")
    executive_summary: str = Field(..., description="Executive summary")
    key_insights: List[str] = Field(..., description="Key insights")
    recommendations: List[Recommendation] = Field(..., description="Actionable recommendations")
    citations: List[Citation] = Field(..., description="Source citations")
    quality_metrics: QualityMetrics = Field(..., description="Quality assessment")
    metadata: Dict[str, Any] = Field(..., description="Generation metadata")
    generated_at: datetime = Field(default_factory=datetime.now, description="Generation timestamp")
    cost_usd: float = Field(..., description="Generation cost in USD")
    generation_time_ms: int = Field(..., description="Generation time in milliseconds")


class TemplateInfo(BaseModel):
    """Information about narrative templates"""
    template_id: str = Field(..., description="Template identifier")
    name: str = Field(..., description="Template name")
    description: str = Field(..., description="Template description")
    narrative_type: NarrativeType = Field(..., description="Supported narrative type")
    audience: AudienceType = Field(..., description="Target audience")
    tone: ToneType = Field(..., description="Default tone")
    length: LengthType = Field(..., description="Default length")
    focus_areas: List[FocusArea] = Field(..., description="Default focus areas")
    sections: List[str] = Field(..., description="Template sections")
    word_count_range: Dict[str, int] = Field(..., description="Expected word count range")


class NarrativeHistory(BaseModel):
    """Historical narrative generation record"""
    narrative_id: str = Field(..., description="Narrative identifier")
    title: str = Field(..., description="Narrative title")
    narrative_type: NarrativeType = Field(..., description="Narrative type")
    audience: AudienceType = Field(..., description="Target audience")
    quality_score: float = Field(..., description="Overall quality score")
    word_count: int = Field(..., description="Word count")
    cost_usd: float = Field(..., description="Generation cost")
    generated_at: datetime = Field(..., description="Generation timestamp")
    user_feedback: Optional[Dict[str, Any]] = Field(None, description="User feedback")


class NarrativeStats(BaseModel):
    """Narrative generation statistics"""
    total_narratives: int = Field(..., description="Total narratives generated")
    narratives_by_type: Dict[str, int] = Field(..., description="Count by narrative type")
    narratives_by_audience: Dict[str, int] = Field(..., description="Count by audience")
    average_quality_score: float = Field(..., description="Average quality score")
    average_cost_usd: float = Field(..., description="Average cost per narrative")
    total_cost_usd: float = Field(..., description="Total cost")
    most_used_template: Optional[str] = Field(None, description="Most used template")
    last_24h_narratives: int = Field(..., description="Narratives in last 24 hours")


class ExportRequest(BaseModel):
    """Request for narrative export"""
    narrative_id: str = Field(..., description="Narrative to export")
    format: Literal["pdf", "docx", "html", "markdown"] = Field(..., description="Export format")
    include_citations: bool = Field(True, description="Include citations")
    include_recommendations: bool = Field(True, description="Include recommendations")
    include_quality_metrics: bool = Field(False, description="Include quality metrics")


class ExportResponse(BaseModel):
    """Narrative export response"""
    download_url: str = Field(..., description="Download URL for exported narrative")
    file_size: int = Field(..., description="File size in bytes")
    format: str = Field(..., description="Export format")
    expires_at: datetime = Field(..., description="Download link expiration")
    generated_at: datetime = Field(default_factory=datetime.now, description="Export timestamp")


class FeedbackRequest(BaseModel):
    """Request for narrative feedback"""
    narrative_id: str = Field(..., description="Narrative identifier")
    overall_rating: int = Field(..., description="Overall rating", ge=1, le=5)
    coherence_rating: int = Field(..., description="Coherence rating", ge=1, le=5)
    accuracy_rating: int = Field(..., description="Accuracy rating", ge=1, le=5)
    actionability_rating: int = Field(..., description="Actionability rating", ge=1, le=5)
    comments: Optional[str] = Field(None, description="Additional comments")
    suggestions: Optional[str] = Field(None, description="Improvement suggestions")


class FeedbackResponse(BaseModel):
    """Feedback submission response"""
    feedback_id: str = Field(..., description="Feedback identifier")
    narrative_id: str = Field(..., description="Narrative identifier")
    overall_rating: int = Field(..., description="Overall rating")
    submitted_at: datetime = Field(default_factory=datetime.now, description="Submission timestamp")
    thank_you_message: str = Field(..., description="Thank you message")
