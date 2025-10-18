"""
Comprehensive Demo Server for All 5 Features
Policy Simulation Assistant - Complete MVP Demo
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import json
import uuid
import time
import csv
import io
import base64
import numpy as np
from data_loader import data_loader

app = FastAPI(
    title="Policy Simulation Assistant - Complete MVP Demo",
    description="Complete demo API for all 5 features: Simulation Engine, Benchmark Dashboard, Narrative Generator, Data Quality Assurance, and Advanced Analytics",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# SHARED MODELS AND DATA
# ============================================================================

# Real data loader - loads actual health indicator data from CSV files
def get_countries_data():
    """Get real countries data from CSV files"""
    return data_loader.get_available_countries()

def get_country_data(country_name: str):
    """Get specific country data from real datasets"""
    return data_loader.get_country_data(country_name)

# ============================================================================
# FEATURE 1: POLICY SIMULATION ENGINE
# ============================================================================

class SimulationParameters(BaseModel):
    doctor_density: float
    nurse_density: float
    health_spending: float

class SimulationRequest(BaseModel):
    country: str
    gender: str = "BOTH"
    parameters: SimulationParameters

class BaselineData(BaseModel):
    life_expectancy: float
    doctor_density: float
    nurse_density: float
    health_spending: float
    year: int

class Prediction(BaseModel):
    life_expectancy: float
    change: float
    change_percentage: float
    confidence_interval: Dict[str, float]
    feature_contributions: Dict[str, float]

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

def simulate_policy_impact(baseline: Dict, parameters: Dict, gender: str = "BOTH") -> Dict:
    """Simulate policy impact using baseline-relative regression model with gender-specific adjustments."""
    
    # Regression coefficients for CHANGE in life expectancy (relative to baseline)
    doctor_coef = 0.12
    nurse_coef = 0.06
    spending_coef = 0.18
    
    # Gender-specific adjustments to coefficients
    gender_adjustments = {
        'MALE': {'doctor_coef': 1.2, 'nurse_coef': 1.0, 'spending_coef': 1.1},
        'FEMALE': {'doctor_coef': 0.8, 'nurse_coef': 1.0, 'spending_coef': 0.9},
        'BOTH': {'doctor_coef': 1.0, 'nurse_coef': 1.0, 'spending_coef': 1.0}
    }
    
    # Apply gender adjustments
    adj = gender_adjustments.get(gender, gender_adjustments['BOTH'])
    adjusted_doctor_coef = doctor_coef * adj['doctor_coef']
    adjusted_nurse_coef = nurse_coef * adj['nurse_coef']
    adjusted_spending_coef = spending_coef * adj['spending_coef']
    
    # Calculate CHANGE from baseline
    baseline_doctor = baseline['doctor_density']
    baseline_nurse = baseline['nurse_density']
    baseline_spending = baseline['health_spending']
    
    # The parameters are already the CHANGE values (e.g., +5 means increase by 5)
    doctor_change = parameters['doctor_density']
    nurse_change = parameters['nurse_density'] 
    spending_change = parameters['health_spending']
    
    # Calculate predicted CHANGE in life expectancy
    predicted_change = (
        doctor_change * adjusted_doctor_coef +
        nurse_change * adjusted_nurse_coef +
        spending_change * adjusted_spending_coef
    )
    
    # Calculate new life expectancy
    predicted_le = baseline['life_expectancy'] + predicted_change
    
    # Calculate change percentage, handling zero baseline
    if baseline['life_expectancy'] > 0:
        change_percentage = (predicted_change / baseline['life_expectancy']) * 100
    else:
        change_percentage = 0  # Default to 0% if baseline is 0
    
    # Calculate confidence interval
    margin_of_error = 0.8 if gender != 'BOTH' else 0.7
    confidence_interval = {
        'lower': predicted_le - margin_of_error,
        'upper': predicted_le + margin_of_error,
        'margin_of_error': margin_of_error
    }
    
    # Calculate feature contributions
    feature_contributions = {
        'doctor_density': doctor_change * adjusted_doctor_coef,
        'nurse_density': nurse_change * adjusted_nurse_coef,
        'health_spending': spending_change * adjusted_spending_coef,
        'intercept': 0.0
    }
    
    return {
        'life_expectancy': predicted_le,
        'change': predicted_change,
        'change_percentage': change_percentage,
        'confidence_interval': confidence_interval,
        'feature_contributions': feature_contributions
    }

# ============================================================================
# FEATURE 2: HEALTH BENCHMARK DASHBOARD
# ============================================================================

class ComparisonRequest(BaseModel):
    countries: List[str]
    metrics: Optional[List[str]] = None
    year: int = 2022
    include_anomalies: bool = True
    include_peers: bool = True

class HealthMetric(BaseModel):
    name: str
    value: float
    unit: str
    rank: int
    percentile: float
    trend: str
    anomaly: bool
    baseline_year: int

class CountryRanking(BaseModel):
    country_code: str
    country_name: str
    overall_rank: int
    metrics: List[HealthMetric]
    total_score: float

class AnomalyAlert(BaseModel):
    country: str
    metric: str
    severity: str
    description: str
    confidence: float
    recommendation: str
    detected_at: str

class PeerGroup(BaseModel):
    name: str
    countries: List[str]
    criteria: List[str]
    average: Dict[str, float]
    size: int

class CountryComparison(BaseModel):
    countries: List[str]
    metrics: List[str]
    year: int
    rankings: List[CountryRanking]
    anomalies: List[AnomalyAlert]
    peer_groups: List[PeerGroup]
    summary: Dict[str, Any]
    generated_at: str

# ============================================================================
# FEATURE 3: NARRATIVE INSIGHT GENERATOR
# ============================================================================

class NarrativeRequest(BaseModel):
    narrative_type: str
    data_source: Dict[str, Any]
    audience: str = "policy_makers"
    tone: str = "formal"
    length: str = "standard"
    focus_areas: List[str] = []
    custom_instructions: Optional[str] = None
    include_citations: bool = True
    include_recommendations: bool = True

class NarrativeSection(BaseModel):
    title: str
    content: str
    order: int
    word_count: int
    key_points: List[str]

class Recommendation(BaseModel):
    title: str
    description: str
    priority: str
    timeline: Optional[str] = None
    resources_needed: Optional[str] = None
    expected_impact: Optional[str] = None

class QualityMetrics(BaseModel):
    coherence_score: float
    accuracy_score: float
    actionability_score: float
    readability_score: float
    overall_score: float
    word_count: int
    reading_time_minutes: int

class NarrativeResponse(BaseModel):
    narrative_id: str
    title: str
    narrative_type: str
    sections: List[NarrativeSection]
    executive_summary: str
    key_insights: List[str]
    recommendations: List[Recommendation]
    quality_metrics: Dict[str, Any]
    metadata: Dict[str, Any]
    generated_at: str
    cost_usd: float
    generation_time_ms: int

# ============================================================================
# FEATURE 4: DATA QUALITY ASSURANCE
# ============================================================================

class QualityAlert(BaseModel):
    id: str
    type: str
    severity: str
    message: str
    affected_indicators: List[str]
    affected_countries: Optional[List[str]] = None
    created_at: str
    resolved: bool = False
    resolved_at: Optional[str] = None
    recommendations: List[str] = []

class QualityMetrics(BaseModel):
    overall_score: float
    completeness_score: float
    validity_score: float
    consistency_score: float
    freshness_score: float
    last_updated: str
    trend: str
    alerts: List[QualityAlert]

class DataSource(BaseModel):
    id: str
    name: str
    url: str
    type: str
    reliability_score: float
    coverage: List[str]
    last_updated: str
    status: str
    version: Optional[str] = None
    description: Optional[str] = None

class ValidationResult(BaseModel):
    dataset_id: str
    validation_timestamp: str
    overall_status: str
    completeness_check: Dict[str, Any]
    validity_check: Dict[str, Any]
    consistency_check: Dict[str, Any]
    outlier_check: Dict[str, Any]
    issues: List[Dict[str, Any]]
    quality_score: float
    validation_duration_ms: int

# ============================================================================
# FEATURE 5: ADVANCED ANALYTICS & REPORTING
# ============================================================================

class TrendAnalysisRequest(BaseModel):
    indicator: str
    country: str
    time_period: Optional[Tuple[int, int]] = None

class CorrelationAnalysisRequest(BaseModel):
    indicators: List[str]
    countries: Optional[List[str]] = None
    time_period: Optional[Tuple[int, int]] = None

class ForecastRequest(BaseModel):
    indicator: str
    country: str
    forecast_years: int = 5
    confidence_level: float = 0.95

class ReportGenerationRequest(BaseModel):
    template: str
    title: str
    simulation_data: Optional[Dict[str, Any]] = None
    analytics_data: Optional[Dict[str, Any]] = None
    data_sources: Optional[List[str]] = None
    config: Dict[str, Any] = {}

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Policy Simulation Assistant - Complete MVP Demo",
        "version": "1.0.0",
        "description": "Complete demo API for all 5 features of the Policy Simulation Assistant",
        "features": {
            "feature_1": "Policy Simulation Engine",
            "feature_2": "Health Benchmark Dashboard", 
            "feature_3": "Narrative Insight Generator",
            "feature_4": "Data Quality Assurance",
            "feature_5": "Advanced Analytics & Reporting"
        },
        "endpoints": {
            "simulation": "/api/simulations/",
            "benchmark": "/api/benchmarks/",
            "narrative": "/api/narratives/",
            "quality": "/api/quality/",
            "analytics": "/api/analytics/"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "policy-simulation-assistant-complete-mvp",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "features": ["simulation", "benchmark", "narrative", "quality", "analytics"]
    }

# ============================================================================
# FEATURE 1 ENDPOINTS
# ============================================================================

@app.get("/api/simulations/countries")
async def get_simulation_countries():
    """Get available countries for simulation"""
    real_countries = get_countries_data()
    countries = []
    for country in real_countries:
        countries.append({
            "code": country["code"],
            "name": country["name"]
        })
    return countries

@app.post("/api/simulations/run")
async def run_simulation(request: SimulationRequest):
    """Run a policy simulation"""
    # Find country in real data
    country_data = get_country_data(request.country)
    if not country_data:
        raise HTTPException(status_code=404, detail=f"Country {request.country} not found")
    
    # Get baseline data
    baseline = country_data['baseline'].copy()
    
    # Update baseline with gender-specific life expectancy if not BOTH
    if request.gender != "BOTH" and 'gender_baseline' in country_data:
        gender_baseline = country_data['gender_baseline'].get(request.gender, {})
        if 'life_expectancy' in gender_baseline:
            baseline['life_expectancy'] = gender_baseline['life_expectancy']
    
    # Run simulation
    prediction_data = simulate_policy_impact(baseline, request.parameters.model_dump(), request.gender)
    
    # Create response
    response = SimulationResponse(
        simulation_id=str(uuid.uuid4()),
        country=request.country,
        timestamp=datetime.now().isoformat(),
        baseline=BaselineData(**baseline),
        parameters=request.parameters,
        prediction=Prediction(**prediction_data),
        model_metrics=ModelMetrics(
            r2_score=0.78,
            mse=0.5,
            rmse=0.7,
            training_samples=100,
            test_samples=25
        ),
        metadata=SimulationMetadata(
            model_version="v1.0-demo-gender",
            execution_time=0.1,
            data_quality=98.4
        )
    )
    
    return response

# ============================================================================
# FEATURE 2 ENDPOINTS
# ============================================================================

@app.get("/api/benchmarks/countries")
async def get_benchmark_countries():
    """Get available countries for benchmarking"""
    real_countries = get_countries_data()
    countries = []
    for country in real_countries:
        countries.append({
            "code": country["code"],
            "name": country["name"]
        })
    return countries

@app.post("/api/benchmarks/compare")
async def compare_countries(request: ComparisonRequest):
    """Compare multiple countries across health metrics"""
    
    try:
        # Get real countries data
        real_countries = get_countries_data()
        country_lookup = {country['code']: country for country in real_countries}
        
        # Validate countries
        for country in request.countries:
            if country not in country_lookup:
                raise HTTPException(status_code=404, detail=f"Country {country} not found")
        
        # Default metrics if none specified
        metrics = request.metrics or ['life_expectancy', 'doctor_density', 'nurse_density', 'health_spending']
        
        # Calculate rankings (simplified)
        rankings = []
        for i, country in enumerate(request.countries):
            country_data = country_lookup[country]['baseline']
        
        # Create mock metrics
        country_metrics = []
        for metric in metrics:
            value = country_data.get(metric, 0)
            country_metrics.append(HealthMetric(
                name=metric,
                value=value,
                unit=get_metric_unit(metric),
                rank=i + 1,
                percentile=100 - (i * 25),
                trend="stable",
                anomaly=False,
                baseline_year=2022
            ))
        
        ranking = CountryRanking(
            country_code=country,
            country_name=country_lookup[country]['name'],
            overall_rank=i + 1,
            metrics=country_metrics,
            total_score=0.8 - (i * 0.2)
        )
        rankings.append(ranking)
        
        # Mock anomalies
        anomalies = []
        if request.include_anomalies:
            anomalies.append(AnomalyAlert(
                country="PRT",
                metric="health_spending",
                severity="medium",
                description="Health spending (5.8% GDP) is below recommended levels",
                confidence=0.8,
                recommendation="Consider increasing health expenditure to improve outcomes",
                detected_at=datetime.now().isoformat()
            ))
        
        # Mock peer groups
        peer_groups = []
        if request.include_peers:
            peer_groups.append(PeerGroup(
                name="Southern Europe",
                countries=["PRT", "ESP", "GRC"],
                criteria=["region"],
                average={"life_expectancy": 82.0, "health_spending": 6.4},
                size=3
            ))
        
        # Generate summary
        summary = {
            "total_countries": len(request.countries),
            "total_anomalies": len(anomalies),
            "high_severity_anomalies": len([a for a in anomalies if a.severity == "high"]),
            "peer_groups": len(peer_groups),
            "best_performer": rankings[0].country_name if rankings else None,
            "worst_performer": rankings[-1].country_name if rankings else None,
            "average_score": sum(r.total_score for r in rankings) / len(rankings) if rankings else 0,
            "score_range": {
                "min": min(r.total_score for r in rankings) if rankings else 0,
                "max": max(r.total_score for r in rankings) if rankings else 0
            }
        }
    
        return CountryComparison(
            countries=request.countries,
            metrics=metrics,
            year=request.year,
            rankings=rankings,
            anomalies=anomalies,
            peer_groups=peer_groups,
            summary=summary,
            generated_at=datetime.now().isoformat()
        )
    except Exception as e:
        print(f"Error in benchmark compare: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

def get_metric_unit(metric: str) -> str:
    """Get unit for metric"""
    units = {
        'life_expectancy': 'years',
        'doctor_density': 'per 1,000 population',
        'nurse_density': 'per 1,000 population',
        'health_spending': '% of GDP'
    }
    return units.get(metric, "")

# ============================================================================
# FEATURE 3 ENDPOINTS
# ============================================================================

@app.get("/api/narratives/options")
async def get_narrative_options():
    """Get available options for narrative generation"""
    return {
        "narrative_types": [
            {"value": "simulation_impact", "label": "Policy Impact Analysis"},
            {"value": "benchmark_comparison", "label": "Country Performance Comparison"},
            {"value": "anomaly_alert", "label": "Anomaly Detection Report"},
            {"value": "trend_analysis", "label": "Trend Analysis Report"},
            {"value": "executive_summary", "label": "Executive Summary"}
        ],
        "audiences": [
            {"value": "ministers", "label": "Ministers"},
            {"value": "ngos", "label": "NGOs"},
            {"value": "researchers", "label": "Researchers"},
            {"value": "public", "label": "Public"},
            {"value": "policy_makers", "label": "Policy Makers"}
        ],
        "tones": [
            {"value": "formal", "label": "Formal"},
            {"value": "conversational", "label": "Conversational"},
            {"value": "technical", "label": "Technical"},
            {"value": "persuasive", "label": "Persuasive"}
        ],
        "lengths": [
            {"value": "brief", "label": "Brief (1-2 pages)"},
            {"value": "standard", "label": "Standard (3-5 pages)"},
            {"value": "detailed", "label": "Detailed (5+ pages)"}
        ],
        "focus_areas": [
            {"value": "economic_impact", "label": "Economic Impact"},
            {"value": "health_outcomes", "label": "Health Outcomes"},
            {"value": "implementation", "label": "Implementation"},
            {"value": "policy_recommendations", "label": "Policy Recommendations"},
            {"value": "risk_assessment", "label": "Risk Assessment"}
        ]
    }

class SimulationNarrativeRequest(BaseModel):
    simulation_results: Dict[str, Any]
    template: str = "policy_insight"
    audience: str = "policy_makers"

@app.post("/api/narratives/generate")
async def generate_narrative(request: SimulationNarrativeRequest):
    """Generate a narrative based on simulation results"""
    
    # Extract simulation data
    sim_results = request.simulation_results
    country = sim_results.get('country', 'Unknown')
    baseline = sim_results.get('baseline', {})
    parameters = sim_results.get('parameters', {})
    prediction = sim_results.get('prediction', {})
    
    # Extract key values
    current_le = baseline.get('life_expectancy', 75.0)
    predicted_change = prediction.get('change', 0.0)
    new_le = current_le + predicted_change
    
    # Determine impact direction
    impact_direction = "positive" if predicted_change > 0 else "negative" if predicted_change < 0 else "neutral"
    
    # Generate narrative based on template
    narrative_id = str(uuid.uuid4())
    
    # Generate narrative based on template
    if request.template in ["policy_insight", "simulation_impact"]:
        # Generate policy-focused narrative
        narrative_text = f"""
Based on the simulation analysis for {country}, the proposed policy changes are predicted to have a {impact_direction} impact on life expectancy.

**Current Status:**
- Current life expectancy: {current_le:.1f} years
- Predicted change: {predicted_change:+.1f} years
- Projected life expectancy: {new_le:.1f} years

**Policy Implications:**
"""
        
        if parameters.get('doctor_density', 0) != 0:
            narrative_text += f"- Doctor density change: {parameters['doctor_density']:+.1f} per 10,000 population\n"
        if parameters.get('nurse_density', 0) != 0:
            narrative_text += f"- Nurse density change: {parameters['nurse_density']:+.1f} per 10,000 population\n"
        if parameters.get('health_spending', 0) != 0:
            narrative_text += f"- Health spending change: {parameters['health_spending']:+.1f}% of GDP\n"
        
        narrative_text += f"""
**Recommendations:**
- Monitor implementation of proposed changes
- Track health outcomes over time
- Consider additional factors affecting life expectancy
- Validate results with local health data

**Confidence Level:** The simulation uses statistical models based on historical data correlations. Results should be interpreted as directional indicators rather than precise predictions.
"""
    
    elif request.template == "executive_summary":
        # Generate executive summary narrative
        narrative_text = f"""
EXECUTIVE SUMMARY: Health Policy Impact Analysis for {country}

OVERVIEW
This analysis evaluates the potential impact of proposed health policy changes on life expectancy in {country}. The simulation model predicts a {impact_direction} impact based on current health indicators and proposed modifications.

KEY FINDINGS
• Current Life Expectancy: {current_le:.1f} years
• Projected Change: {predicted_change:+.1f} years
• New Life Expectancy: {new_le:.1f} years

POLICY CHANGES ANALYZED
"""
        
        if parameters.get('doctor_density', 0) != 0:
            narrative_text += f"• Doctor Density: {parameters['doctor_density']:+.1f} per 10,000 population\n"
        if parameters.get('nurse_density', 0) != 0:
            narrative_text += f"• Nurse Density: {parameters['nurse_density']:+.1f} per 10,000 population\n"
        if parameters.get('health_spending', 0) != 0:
            narrative_text += f"• Health Spending: {parameters['health_spending']:+.1f}% of GDP\n"
        
        narrative_text += f"""
STRATEGIC RECOMMENDATIONS
1. Implement comprehensive monitoring systems
2. Establish baseline metrics for tracking
3. Develop contingency plans for unexpected outcomes
4. Engage stakeholders in implementation process

RISK ASSESSMENT
The analysis is based on statistical correlations and should be considered directional guidance. Actual outcomes may vary due to external factors not captured in this model.

NEXT STEPS
• Validate findings with local health experts
• Develop detailed implementation timeline
• Establish success metrics and monitoring protocols
"""
    
    elif request.template == "trend_analysis":
        # Generate trend analysis narrative
        narrative_text = f"""
TREND ANALYSIS: Health Policy Impact Trends for {country}

TREND OVERVIEW
Analysis of proposed health policy changes reveals a {impact_direction} trend in life expectancy projections for {country}.

CURRENT TRENDS
• Baseline Life Expectancy: {current_le:.1f} years
• Projected Change: {predicted_change:+.1f} years
• Trend Direction: {'Upward' if predicted_change > 0 else 'Downward' if predicted_change < 0 else 'Stable'}

FACTOR ANALYSIS
"""
        
        if parameters.get('doctor_density', 0) != 0:
            narrative_text += f"• Doctor Density Impact: {parameters['doctor_density']:+.1f} per 10,000 population\n"
        if parameters.get('nurse_density', 0) != 0:
            narrative_text += f"• Nurse Density Impact: {parameters['nurse_density']:+.1f} per 10,000 population\n"
        if parameters.get('health_spending', 0) != 0:
            narrative_text += f"• Health Spending Impact: {parameters['health_spending']:+.1f}% of GDP\n"
        
        narrative_text += f"""
TREND PROJECTIONS
Based on current data patterns, the proposed changes are expected to result in a {impact_direction} impact on life expectancy. This trend should be monitored closely for any deviations from projections.

ANALYTICAL INSIGHTS
• Statistical confidence in trend direction
• Historical correlation patterns
• External factor considerations
• Long-term sustainability assessment
"""
    
    else:
        # Default to policy insight for unknown templates
        narrative_text = f"""
Based on the simulation analysis for {country}, the proposed policy changes are predicted to have a {impact_direction} impact on life expectancy.

**Current Status:**
- Current life expectancy: {current_le:.1f} years
- Predicted change: {predicted_change:+.1f} years
- Projected life expectancy: {new_le:.1f} years

**Policy Implications:**
"""
        
        if parameters.get('doctor_density', 0) != 0:
            narrative_text += f"- Doctor density change: {parameters['doctor_density']:+.1f} per 10,000 population\n"
        if parameters.get('nurse_density', 0) != 0:
            narrative_text += f"- Nurse density change: {parameters['nurse_density']:+.1f} per 10,000 population\n"
        if parameters.get('health_spending', 0) != 0:
            narrative_text += f"- Health spending change: {parameters['health_spending']:+.1f}% of GDP\n"
        
        narrative_text += f"""
**Recommendations:**
- Monitor implementation of proposed changes
- Track health outcomes over time
- Consider additional factors affecting life expectancy
- Validate results with local health data

**Confidence Level:** The simulation uses statistical models based on historical data correlations. Results should be interpreted as directional indicators rather than precise predictions.
"""
    
    
    # Generate disclaimers
    disclaimers = [
        "This analysis is based on statistical models and historical data correlations",
        "Results should be interpreted as directional indicators, not precise predictions",
        "Actual outcomes may vary due to factors not included in this model",
        "Policy decisions should consider multiple factors beyond this analysis"
    ]
    
    # Generate citations
    citations = [
        "WHO Global Health Observatory 2023",
        "World Bank Health Expenditure Data",
        "OECD Health Statistics 2023"
    ]
    
    return {
        "narrative_id": narrative_id,
        "narrative": narrative_text.strip(),
        "disclaimers": disclaimers,
        "citations": citations,
        "metadata": {
            "country": country,
            "template": request.template,
            "audience": request.audience,
            "generated_at": datetime.now().isoformat(),
            "word_count": len(narrative_text.split())
        }
    }

# ============================================================================
# FEATURE 4 ENDPOINTS
# ============================================================================

@app.get("/api/quality/overview")
async def get_quality_overview():
    """Get overall data quality overview"""
    return {
        "overall_score": 98.4,
        "completeness_score": 99.2,
        "validity_score": 97.8,
        "consistency_score": 98.9,
        "freshness_score": 98.1,
        "last_updated": datetime.now().isoformat(),
        "trend": "up",
        "alerts": [
            {
                "id": "alert_001",
                "type": "freshness",
                "severity": "medium",
                "message": "Greece health spending data 3 days old",
                "affected_indicators": ["health_spending"],
                "affected_countries": ["GRC"],
                "created_at": (datetime.now() - timedelta(hours=2)).isoformat(),
                "recommendations": ["Update data from source", "Check data pipeline"]
            }
        ],
        "data_sources": {
            "who_global_health": {
                "name": "WHO Global Health Observatory",
                "last_updated": (datetime.now() - timedelta(days=2)).isoformat(),
                "reliability_score": 0.95,
                "status": "active"
            }
        }
    }

@app.get("/api/quality/alerts")
async def get_quality_alerts(severity: Optional[str] = None, resolved: bool = False):
    """Get quality alerts with optional filtering"""
    alerts = [
        {
            "id": "alert_001",
            "type": "freshness",
            "severity": "medium",
            "message": "Greece health spending data 3 days old",
            "affected_indicators": ["health_spending"],
            "affected_countries": ["GRC"],
            "created_at": (datetime.now() - timedelta(hours=2)).isoformat(),
            "recommendations": ["Update data from source", "Check data pipeline"]
        }
    ]
    
    # Apply filters
    if severity:
        alerts = [alert for alert in alerts if alert["severity"] == severity]
    
    if not resolved:
        alerts = [alert for alert in alerts if not alert.get("resolved", False)]
    
    return alerts

@app.post("/api/quality/validate")
async def validate_data(request: Dict[str, Any]):
    """Validate data quality for a specific dataset"""
    dataset_id = request.get("dataset_id", "health_indicators")
    
    return ValidationResult(
        dataset_id=dataset_id,
        validation_timestamp=datetime.now().isoformat(),
        overall_status="pass",
        completeness_check={
            "status": "pass",
            "score": 99.2,
            "details": "Completeness: 99.2% (119/120 cells)",
            "recommendations": []
        },
        validity_check={
            "status": "pass",
            "score": 97.8,
            "details": "Validity: 97.8% (1 issue found)",
            "recommendations": ["Review outlier in Greece health spending data"]
        },
        consistency_check={
            "status": "pass",
            "score": 98.9,
            "details": "Consistency: 98.9% (no issues found)",
            "recommendations": []
        },
        outlier_check={
            "status": "warning",
            "score": 95.0,
            "details": "Outlier check: 95.0% (1 outlier found)",
            "recommendations": ["Verify outlier data with source"]
        },
        issues=[
            {
                "type": "outlier",
                "severity": "low",
                "description": "Greece health spending appears to be an outlier",
                "affected_records": ["GRC_2022"],
                "recommendation": "Verify with source data"
            }
        ],
        quality_score=97.7,
        validation_duration_ms=150
    )

# ============================================================================
# FEATURE 5 ENDPOINTS
# ============================================================================

@app.post("/api/analytics/trends")
async def analyze_trends(request: TrendAnalysisRequest):
    """Perform trend analysis on health indicators"""
    try:
        # Mock trend analysis data
        result = {
            "indicator": request.indicator,
            "country": request.country,
            "time_period": {
                "start": 2020,
                "end": 2024
            },
            "trend_direction": "increasing",
            "trend_strength": 0.95,
            "annual_change": 0.3,
            "total_change": 1.2,
            "change_percentage": 1.5,
            "statistical_significance": 0.001,
            "confidence_interval": {
                "lower": 0.2,
                "upper": 0.4
            },
            "r_squared": 0.90,
            "sample_size": 5,
            "data_points": [
                {"year": 2020, "value": 81.2},
                {"year": 2021, "value": 81.5},
                {"year": 2022, "value": 81.8},
                {"year": 2023, "value": 82.1},
                {"year": 2024, "value": 82.4}
            ],
            "response_time_ms": 150,
            "generated_at": time.time()
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trend analysis failed: {str(e)}")

@app.post("/api/analytics/correlations")
async def analyze_correlations(request: CorrelationAnalysisRequest):
    """Calculate correlation matrix between health indicators"""
    try:
        # Mock correlation data
        result = {
            "indicators": request.indicators,
            "countries": request.countries,
            "time_period": request.time_period,
            "correlation_matrix": [
                [1.0, 0.78, 0.65, 0.82],
                [0.78, 1.0, 0.45, 0.67],
                [0.65, 0.45, 1.0, 0.58],
                [0.82, 0.67, 0.58, 1.0]
            ],
            "significance_matrix": [
                [0.001, 0.001, 0.01, 0.001],
                [0.001, 0.001, 0.05, 0.001],
                [0.01, 0.05, 0.001, 0.01],
                [0.001, 0.001, 0.01, 0.001]
            ],
            "interpretation": "Strong positive correlations found between life expectancy and healthcare indicators. Government spending shows the strongest correlation with life expectancy outcomes.",
            "sample_size": 25,
            "response_time_ms": 200,
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Correlation analysis failed: {str(e)}")

@app.post("/api/analytics/reports/generate")
async def generate_report(request: ReportGenerationRequest):
    """Generate automated report with customizable templates"""
    try:
        report_id = str(uuid.uuid4())
        
        # Generate report content based on template
        if request.template == "executive_summary":
            content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>{request.title}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                    .header {{ border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }}
                    .section {{ margin-bottom: 30px; }}
                    .section h2 {{ color: #2c3e50; border-bottom: 1px solid #bdc3c7; padding-bottom: 10px; }}
                    .key-finding {{ background: #ecf0f1; padding: 15px; margin: 10px 0; border-left: 4px solid #3498db; }}
                    .recommendation {{ background: #e8f5e8; padding: 15px; margin: 10px 0; border-left: 4px solid #27ae60; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>{request.title}</h1>
                    <p><strong>Generated:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                
                <div class="section">
                    <h2>Executive Summary</h2>
                    <p>This analysis provides comprehensive insights into health policy impacts based on advanced analytics and simulation results.</p>
                </div>
                
                <div class="section">
                    <h2>Key Findings</h2>
                    <div class="key-finding">
                        <strong>Positive Trend in Life Expectancy</strong><br>
                        Analysis shows a consistent upward trend in life expectancy across target countries.
                    </div>
                    <div class="key-finding">
                        <strong>Strong Correlation with Healthcare Spending</strong><br>
                        Government health spending demonstrates strong correlation with health outcomes.
                    </div>
                </div>
                
                <div class="section">
                    <h2>Recommendations</h2>
                    <div class="recommendation">
                        <strong>Increase Healthcare Investment</strong><br>
                        Consider increasing government health spending to improve outcomes.
                    </div>
                    <div class="recommendation">
                        <strong>Monitor Implementation</strong><br>
                        Establish monitoring systems to track policy impact.
                    </div>
                </div>
            </body>
            </html>
            """
        else:
            content = f"<html><body><h1>{request.title}</h1><p>Report content generated for template: {request.template}</p></body></html>"
        
        result = {
            "report_id": report_id,
            "title": request.title,
            "format": "html",
            "content": content,
            "metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "template": request.template,
                "sections_count": 4
            },
            "response_time_ms": 500,
            "generated_at": time.time()
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")

@app.get("/api/quality/sources")
async def get_data_sources():
    """Get information about data sources"""
    return [
        {
            "source_id": "who_gho",
            "name": "WHO Global Health Observatory",
            "description": "Comprehensive health statistics from WHO",
            "url": "https://www.who.int/data/gho",
            "last_updated": "2024-01-15",
            "coverage": "Global",
            "quality_score": 98.5
        },
        {
            "source_id": "world_bank",
            "name": "World Bank Health Data",
            "description": "Health and development indicators",
            "url": "https://data.worldbank.org/topic/health",
            "last_updated": "2024-01-10",
            "coverage": "Global",
            "quality_score": 97.8
        },
        {
            "source_id": "oecd_health",
            "name": "OECD Health Statistics",
            "description": "Health indicators for OECD countries",
            "url": "https://stats.oecd.org/",
            "last_updated": "2024-01-12",
            "coverage": "OECD Countries",
            "quality_score": 99.1
        }
    ]

# ============================================================================
# DEMO PAGE
# ============================================================================

@app.get("/test", response_class=HTMLResponse)
async def test_page():
    """Simple test page to verify interactive functionality"""
    with open("test_interactive.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/full", response_class=HTMLResponse)
async def full_interactive_demo():
    """Full interactive demo with complete user interfaces for all features"""
    with open("full_interactive_demo.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/test_narrative", response_class=HTMLResponse)
async def test_narrative():
    """Test narrative page"""
    with open("test_narrative.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/demo", response_class=HTMLResponse)
async def demo_page():
    """Demo page for testing all 5 features"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Policy Simulation Assistant - Complete MVP Demo</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50">
        <div class="min-h-screen py-8">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="text-center mb-8">
                    <h1 class="text-4xl font-bold text-gray-900 mb-4">
                        Policy Simulation Assistant
                    </h1>
                    <p class="text-xl text-gray-600">
                        Complete MVP Demo - All 5 Features
                    </p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-8">
                    <!-- Feature 1: Simulation Engine -->
                    <div class="bg-white rounded-lg shadow-lg p-6">
                        <div class="flex items-center mb-4">
                            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mr-4">
                                <span class="text-2xl">🎯</span>
                            </div>
                            <div>
                                <h3 class="text-lg font-semibold text-gray-900">Feature 1</h3>
                                <p class="text-sm text-gray-600">Policy Simulation Engine</p>
                            </div>
                        </div>
                        <p class="text-gray-700 mb-4">
                            Run what-if simulations to predict the impact of healthcare workforce and spending changes on life expectancy.
                        </p>
                        <div class="space-y-2">
                            <button onclick="testSimulation()" class="w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                                Test Simulation
                            </button>
                            <button onclick="testCountries()" class="w-full px-4 py-2 bg-blue-100 text-blue-700 rounded hover:bg-blue-200">
                                Get Countries
                            </button>
                        </div>
                    </div>

                    <!-- Feature 2: Benchmark Dashboard -->
                    <div class="bg-white rounded-lg shadow-lg p-6">
                        <div class="flex items-center mb-4">
                            <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mr-4">
                                <span class="text-2xl">📊</span>
                            </div>
                            <div>
                                <h3 class="text-lg font-semibold text-gray-900">Feature 2</h3>
                                <p class="text-sm text-gray-600">Health Benchmark Dashboard</p>
                            </div>
                        </div>
                        <p class="text-gray-700 mb-4">
                            Compare countries across health indicators, detect anomalies, and analyze peer groups.
                        </p>
                        <div class="space-y-2">
                            <button onclick="testBenchmark()" class="w-full px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
                                Test Benchmark
                            </button>
                            <button onclick="testCompare()" class="w-full px-4 py-2 bg-green-100 text-green-700 rounded hover:bg-green-200">
                                Compare Countries
                            </button>
                        </div>
                    </div>

                    <!-- Feature 3: Narrative Generator -->
                    <div class="bg-white rounded-lg shadow-lg p-6">
                        <div class="flex items-center mb-4">
                            <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mr-4">
                                <span class="text-2xl">📝</span>
                            </div>
                            <div>
                                <h3 class="text-lg font-semibold text-gray-900">Feature 3</h3>
                                <p class="text-sm text-gray-600">Narrative Insight Generator</p>
                            </div>
                        </div>
                        <p class="text-gray-700 mb-4">
                            Generate AI-powered policy narratives from simulation results and benchmark data.
                        </p>
                        <div class="space-y-2">
                            <button onclick="testNarrative()" class="w-full px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700">
                                Test Narrative
                            </button>
                            <button onclick="testOptions()" class="w-full px-4 py-2 bg-purple-100 text-purple-700 rounded hover:bg-purple-200">
                                Get Options
                            </button>
                        </div>
                    </div>

                    <!-- Feature 4: Data Quality Assurance -->
                    <div class="bg-white rounded-lg shadow-lg p-6">
                        <div class="flex items-center mb-4">
                            <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center mr-4">
                                <span class="text-2xl">🛡️</span>
                            </div>
                            <div>
                                <h3 class="text-lg font-semibold text-gray-900">Feature 4</h3>
                                <p class="text-sm text-gray-600">Data Quality Assurance</p>
                            </div>
                        </div>
                        <p class="text-gray-700 mb-4">
                            Monitor data quality, validate datasets, and track data provenance.
                        </p>
                        <div class="space-y-2">
                            <button onclick="testQualityOverview()" class="w-full px-4 py-2 bg-yellow-600 text-white rounded hover:bg-yellow-700">
                                Quality Overview
                            </button>
                            <button onclick="testQualityAlerts()" class="w-full px-4 py-2 bg-yellow-100 text-yellow-700 rounded hover:bg-yellow-200">
                                Quality Alerts
                            </button>
                        </div>
                    </div>

                    <!-- Feature 5: Advanced Analytics -->
                    <div class="bg-white rounded-lg shadow-lg p-6">
                        <div class="flex items-center mb-4">
                            <div class="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center mr-4">
                                <span class="text-2xl">📈</span>
                            </div>
                            <div>
                                <h3 class="text-lg font-semibold text-gray-900">Feature 5</h3>
                                <p class="text-sm text-gray-600">Advanced Analytics & Reporting</p>
                            </div>
                        </div>
                        <p class="text-gray-700 mb-4">
                            Perform trend analysis, generate reports, and create advanced visualizations.
                        </p>
                        <div class="space-y-2">
                            <button onclick="testTrendAnalysis()" class="w-full px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700">
                                Trend Analysis
                            </button>
                            <button onclick="testReportGeneration()" class="w-full px-4 py-2 bg-indigo-100 text-indigo-700 rounded hover:bg-indigo-200">
                                Generate Report
                            </button>
                        </div>
                    </div>

                    <!-- API Documentation -->
                    <div class="bg-white rounded-lg shadow-lg p-6">
                        <div class="flex items-center mb-4">
                            <div class="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center mr-4">
                                <span class="text-2xl">📚</span>
                            </div>
                            <div>
                                <h3 class="text-lg font-semibold text-gray-900">API Documentation</h3>
                                <p class="text-sm text-gray-600">Interactive API Docs</p>
                            </div>
                        </div>
                        <p class="text-gray-700 mb-4">
                            Explore all available endpoints and test the API directly.
                        </p>
                        <div class="space-y-2">
                            <a href="/docs" target="_blank" class="w-full px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700 text-center block">
                                Open API Docs
                            </a>
                            <button onclick="testHealthCheck()" class="w-full px-4 py-2 bg-gray-100 text-gray-700 rounded hover:bg-gray-200">
                                Health Check
                            </button>
                        </div>
                    </div>
                </div>

                <div id="results" class="bg-white rounded-lg shadow-lg p-6">
                    <h2 class="text-xl font-semibold mb-4">API Response</h2>
                    <pre id="output" class="bg-gray-100 p-4 rounded text-sm overflow-auto max-h-96"></pre>
                </div>
            </div>
        </div>

        <script>
            const API_BASE = window.location.origin;
            
            function displayResult(data) {
                document.getElementById('output').textContent = JSON.stringify(data, null, 2);
            }
            
            // Feature 1 Tests
            async function testSimulation() {
                try {
                    const response = await fetch(`${API_BASE}/api/simulations/run`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            country: 'PRT',
                            gender: 'BOTH',
                            parameters: {
                                doctor_density: 3.0,
                                nurse_density: 6.0,
                                health_spending: 7.0
                            }
                        })
                    });
                    const data = await response.json();
                    displayResult(data);
                } catch (error) {
                    displayResult({ error: error.message });
                }
            }
            
            async function testCountries() {
                try {
                    const response = await fetch(`${API_BASE}/api/simulations/countries`);
                    const data = await response.json();
                    displayResult(data);
                } catch (error) {
                    displayResult({ error: error.message });
                }
            }
            
            // Feature 2 Tests
            async function testBenchmark() {
                try {
                    const response = await fetch(`${API_BASE}/api/benchmarks/countries`);
                    const data = await response.json();
                    displayResult(data);
                } catch (error) {
                    displayResult({ error: error.message });
                }
            }
            
            async function testCompare() {
                try {
                    const response = await fetch(`${API_BASE}/api/benchmarks/compare`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            countries: ['PRT', 'ESP', 'SWE'],
                            metrics: ['life_expectancy', 'doctor_density', 'health_spending'],
                            include_anomalies: true,
                            include_peers: true
                        })
                    });
                    const data = await response.json();
                    displayResult(data);
                } catch (error) {
                    displayResult({ error: error.message });
                }
            }
            
            // Feature 3 Tests
            async function testNarrative() {
                try {
                    const response = await fetch(`${API_BASE}/api/narratives/generate`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            narrative_type: 'simulation_impact',
                            data_source: {
                                country: 'Portugal',
                                predicted_change: 0.75,
                                confidence_interval: { lower: 0.60, upper: 0.90 }
                            },
                            audience: 'policy_makers',
                            tone: 'formal',
                            length: 'standard',
                            focus_areas: ['policy_recommendations'],
                            include_citations: true,
                            include_recommendations: true
                        })
                    });
                    const data = await response.json();
                    displayResult(data);
                } catch (error) {
                    displayResult({ error: error.message });
                }
            }
            
            async function testOptions() {
                try {
                    const response = await fetch(`${API_BASE}/api/narratives/options`);
                    const data = await response.json();
                    displayResult(data);
                } catch (error) {
                    displayResult({ error: error.message });
                }
            }
            
            // Feature 4 Tests
            async function testQualityOverview() {
                try {
                    const response = await fetch(`${API_BASE}/api/quality/overview`);
                    const data = await response.json();
                    displayResult(data);
                } catch (error) {
                    displayResult({ error: error.message });
                }
            }
            
            async function testQualityAlerts() {
                try {
                    const response = await fetch(`${API_BASE}/api/quality/alerts`);
                    const data = await response.json();
                    displayResult(data);
                } catch (error) {
                    displayResult({ error: error.message });
                }
            }
            
            // Feature 5 Tests
            async function testTrendAnalysis() {
                try {
                    const response = await fetch(`${API_BASE}/api/analytics/trends`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            indicator: 'life_expectancy',
                            country: 'PRT',
                            time_period: [2020, 2024]
                        })
                    });
                    const data = await response.json();
                    displayResult(data);
                } catch (error) {
                    displayResult({ error: error.message });
                }
            }
            
            async function testReportGeneration() {
                try {
                    const response = await fetch(`${API_BASE}/api/analytics/reports/generate`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            template: 'executive_summary',
                            title: 'Health Policy Impact Analysis Report',
                            simulation_data: {
                                country: 'Portugal',
                                predicted_change: 0.75
                            },
                            config: {
                                include_charts: true,
                                include_tables: true
                            }
                        })
                    });
                    const data = await response.json();
                    displayResult(data);
                } catch (error) {
                    displayResult({ error: error.message });
                }
            }
            
            // System Tests
            async function testHealthCheck() {
                try {
                    const response = await fetch(`${API_BASE}/health`);
                    const data = await response.json();
                    displayResult(data);
                } catch (error) {
                    displayResult({ error: error.message });
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Get port from environment variable (Railway sets this)
    port = int(os.environ.get("PORT", 8005))
    
    print("🚀 Starting Policy Simulation Assistant - Complete MVP Demo Server...")
    print(f"📊 Available at: http://localhost:{port}")
    print(f"📚 API Docs at: http://localhost:{port}/docs")
    print(f"🌍 Demo page: http://localhost:{port}/demo")
    print("")
    print("🎯 Feature 1 - Simulation Engine:")
    print(f"   - Countries: http://localhost:{port}/api/simulations/countries")
    print(f"   - Run Simulation: http://localhost:{port}/api/simulations/run")
    print("")
    print("📊 Feature 2 - Benchmark Dashboard:")
    print(f"   - Countries: http://localhost:{port}/api/benchmarks/countries")
    print(f"   - Compare: http://localhost:{port}/api/benchmarks/compare")
    print("")
    print("📝 Feature 3 - Narrative Generator:")
    print(f"   - Options: http://localhost:{port}/api/narratives/options")
    print(f"   - Generate: http://localhost:{port}/api/narratives/generate")
    print("")
    print("🛡️ Feature 4 - Data Quality Assurance:")
    print(f"   - Overview: http://localhost:{port}/api/quality/overview")
    print(f"   - Alerts: http://localhost:{port}/api/quality/alerts")
    print(f"   - Validate: http://localhost:{port}/api/quality/validate")
    print("")
    print("📈 Feature 5 - Advanced Analytics & Reporting:")
    print(f"   - Trends: http://localhost:{port}/api/analytics/trends")
    print(f"   - Correlations: http://localhost:{port}/api/analytics/correlations")
    print(f"   - Reports: http://localhost:{port}/api/analytics/reports/generate")
    print("")
    print(f"🔍 Health Check: http://localhost:{port}/health")
    
    uvicorn.run(app, host="0.0.0.0", port=port)
