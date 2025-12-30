"""
Data Quality Assurance API routes
Provides endpoints for quality monitoring, validation, and provenance tracking
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
import structlog
import time
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from src.backend.core.database import get_db
from src.backend.core.exceptions import DataQualityException, ValidationError
from src.backend.services.quality_monitor import (
    DataQualityMonitor, 
    QualityMetrics, 
    QualityBreakdown, 
    ValidationResult,
    QualityAlert
)
from src.backend.services.provenance_tracker import (
    DataProvenanceTracker,
    ProvenanceData,
    ProcessingStepType,
    DataSourceType
)

logger = structlog.get_logger()
router = APIRouter(prefix="/api/quality")

# Initialize services
quality_monitor = DataQualityMonitor()
provenance_tracker = DataProvenanceTracker()

@router.get("/overview", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def get_quality_overview():
    """
    Get overall data quality overview with key metrics and alerts.
    """
    logger.info("Fetching quality overview")
    
    try:
        # Mock data for demonstration - in real implementation, this would come from actual data
        mock_data = {
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
                    "created_at": datetime.now().isoformat(),
                    "resolved": False
                },
                {
                    "id": "alert_002", 
                    "type": "validity",
                    "severity": "low",
                    "message": "Portugal nurse density outlier detected",
                    "affected_indicators": ["nurse_density"],
                    "created_at": datetime.now().isoformat(),
                    "resolved": False
                }
            ],
            "data_sources": {
                "who_global_health": {
                    "name": "WHO Global Health Observatory",
                    "last_updated": (datetime.now() - timedelta(days=2)).isoformat(),
                    "reliability_score": 0.95,
                    "status": "active"
                },
                "world_bank": {
                    "name": "World Bank Data",
                    "last_updated": (datetime.now() - timedelta(days=1)).isoformat(),
                    "reliability_score": 0.92,
                    "status": "active"
                },
            }
        }
        
        return mock_data
        
    except Exception as e:
        logger.error("Error fetching quality overview", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve quality overview")

@router.get("/indicators/{indicator_id}", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def get_indicator_quality(indicator_id: str):
    """
    Get quality metrics for a specific health indicator.
    """
    logger.info("Fetching quality for indicator", indicator_id=indicator_id)
    
    try:
        # Mock data for demonstration
        mock_quality_data = {
            "indicator_id": indicator_id,
            "overall_score": 97.5,
            "completeness_score": 98.0,
            "validity_score": 97.0,
            "consistency_score": 97.5,
            "freshness_score": 97.5,
            "last_updated": datetime.now().isoformat(),
            "trend": "stable",
            "coverage": {
                "countries": ["PRT", "ESP", "SWE", "GRC"],
                "years": ["2020", "2021", "2022"],
                "total_records": 12
            },
            "issues": [
                {
                    "type": "outlier",
                    "severity": "low",
                    "description": f"Outlier detected in {indicator_id} for Greece",
                    "affected_country": "GRC",
                    "affected_year": "2022"
                }
            ],
            "recommendations": [
                "Verify outlier data with source",
                "Consider data validation rules update"
            ]
        }
        
        return mock_quality_data
        
    except Exception as e:
        logger.error("Error fetching indicator quality", indicator_id=indicator_id, exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve indicator quality")

@router.get("/countries/{country_code}", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def get_country_quality(country_code: str):
    """
    Get quality metrics for a specific country.
    """
    logger.info("Fetching quality for country", country_code=country_code)
    
    try:
        # Mock data for demonstration
        mock_quality_data = {
            "country_code": country_code,
            "country_name": {"PRT": "Portugal", "ESP": "Spain", "SWE": "Sweden", "GRC": "Greece"}.get(country_code, country_code),
            "overall_score": 98.7,
            "completeness_score": 99.0,
            "validity_score": 98.5,
            "consistency_score": 98.5,
            "freshness_score": 98.8,
            "last_updated": datetime.now().isoformat(),
            "trend": "up",
            "indicators": {
                "life_expectancy": {
                    "score": 99.0,
                    "last_updated": (datetime.now() - timedelta(days=1)).isoformat(),
                    "status": "excellent"
                },
                "doctor_density": {
                    "score": 98.5,
                    "last_updated": (datetime.now() - timedelta(days=2)).isoformat(),
                    "status": "good"
                },
                "nurse_density": {
                    "score": 98.0,
                    "last_updated": (datetime.now() - timedelta(days=1)).isoformat(),
                    "status": "good"
                },
                "health_spending": {
                    "score": 99.0,
                    "last_updated": (datetime.now() - timedelta(days=1)).isoformat(),
                    "status": "excellent"
                }
            },
            "alerts": [],
            "data_sources": [
                {
                    "name": "WHO Global Health Observatory",
                    "coverage": ["life_expectancy", "doctor_density", "nurse_density"],
                    "last_updated": (datetime.now() - timedelta(days=2)).isoformat()
                },
                {
                    "name": "World Bank Data",
                    "coverage": ["health_spending"],
                    "last_updated": (datetime.now() - timedelta(days=1)).isoformat()
                }
            ]
        }
        
        return mock_quality_data
        
    except Exception as e:
        logger.error("Error fetching country quality", country_code=country_code, exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve country quality")

@router.get("/trends", response_model=List[Dict[str, Any]], status_code=status.HTTP_200_OK)
async def get_quality_trends(days: int = 30):
    """
    Get quality trends over specified period.
    """
    logger.info("Fetching quality trends", days=days)
    
    try:
        # Mock trend data for demonstration
        trends = []
        base_date = datetime.now() - timedelta(days=days)
        
        for i in range(days):
            date = base_date + timedelta(days=i)
            trends.append({
                "timestamp": date.isoformat(),
                "overall_score": 98.0 + (i * 0.1) + (i % 3 - 1) * 0.2,  # Simulate trend with some variation
                "completeness_score": 99.0 + (i % 2 - 0.5) * 0.1,
                "validity_score": 97.5 + (i * 0.05) + (i % 4 - 2) * 0.1,
                "consistency_score": 98.5 + (i % 3 - 1) * 0.1,
                "freshness_score": 98.0 + (i * 0.08) + (i % 5 - 2) * 0.15,
                "alert_count": max(0, 2 - (i // 10))  # Decreasing alerts over time
            })
        
        return trends
        
    except Exception as e:
        logger.error("Error fetching quality trends", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve quality trends")

@router.post("/validate", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def validate_data(request: Dict[str, Any]):
    """
    Validate data quality for a specific dataset or indicator.
    """
    logger.info("Validating data", request=request)
    
    try:
        dataset_id = request.get("dataset_id", "unknown")
        validation_type = request.get("validation_type", "comprehensive")
        
        # Mock validation result
        validation_result = {
            "dataset_id": dataset_id,
            "validation_timestamp": datetime.now().isoformat(),
            "overall_status": "pass",
            "completeness_check": {
                "status": "pass",
                "score": 99.2,
                "details": "Completeness: 99.2% (119/120 cells)",
                "recommendations": []
            },
            "validity_check": {
                "status": "pass",
                "score": 97.8,
                "details": "Validity: 97.8% (1 issue found)",
                "recommendations": ["Review outlier in Greece health spending data"]
            },
            "consistency_check": {
                "status": "pass",
                "score": 98.9,
                "details": "Consistency: 98.9% (no issues found)",
                "recommendations": []
            },
            "outlier_check": {
                "status": "warning",
                "score": 95.0,
                "details": "Outlier check: 95.0% (1 outlier found)",
                "recommendations": ["Verify outlier data with source"]
            },
            "issues": [
                {
                    "type": "outlier",
                    "severity": "low",
                    "description": "Greece health spending appears to be an outlier",
                    "affected_records": ["GRC_2022"],
                    "recommendation": "Verify with source data"
                }
            ],
            "quality_score": 97.7,
            "validation_duration_ms": 150
        }
        
        return validation_result
        
    except Exception as e:
        logger.error("Error validating data", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to validate data")

@router.get("/provenance/{dataset_id}", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def get_data_provenance(dataset_id: str):
    """
    Get data provenance information for a specific dataset.
    """
    logger.info("Fetching data provenance", dataset_id=dataset_id)
    
    try:
        # Get provenance data from tracker
        provenance_data = provenance_tracker.get_provenance_data(dataset_id)
        
        if not provenance_data:
            # Create mock provenance data for demonstration
            provenance_data = provenance_tracker.create_provenance_record(
                dataset_id=dataset_id,
                initial_sources=["who_global_health", "world_bank"]
            )
            
            # Add some processing steps
            provenance_tracker.add_processing_step(
                dataset_id=dataset_id,
                step_type=ProcessingStepType.DATA_INGESTION,
                description="Ingested health data from WHO and World Bank",
                input_data="Raw CSV files from external sources",
                output_data="Standardized health indicators dataset",
                parameters={"sources": ["who_global_health", "world_bank"]},
                duration_ms=2500
            )
            
            provenance_tracker.add_processing_step(
                dataset_id=dataset_id,
                step_type=ProcessingStepType.DATA_CLEANING,
                description="Cleaned and validated health data",
                input_data="Standardized health indicators dataset",
                output_data="Validated health indicators dataset",
                parameters={"validation_rules": "completeness, validity, consistency"},
                duration_ms=1200
            )
        
        # Get data lineage
        lineage = provenance_tracker.get_data_lineage(dataset_id)
        
        return lineage
        
    except Exception as e:
        logger.error("Error fetching data provenance", dataset_id=dataset_id, exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve data provenance")

@router.get("/provenance/{dataset_id}/export", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def export_provenance_data(dataset_id: str, format: str = "json"):
    """
    Export data provenance information in specified format.
    """
    logger.info("Exporting provenance data", dataset_id=dataset_id, format=format)
    
    try:
        if format not in ["json", "csv"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported format. Use 'json' or 'csv'")
        
        # Export provenance data
        exported_data = provenance_tracker.export_provenance_data(dataset_id, format)
        
        return {
            "dataset_id": dataset_id,
            "format": format,
            "exported_data": exported_data,
            "export_timestamp": datetime.now().isoformat(),
            "size_bytes": len(exported_data.encode('utf-8'))
        }
        
    except ValueError as e:
        logger.warning("Provenance record not found", dataset_id=dataset_id, error=str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error("Error exporting provenance data", dataset_id=dataset_id, exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to export provenance data")

@router.get("/sources", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def get_data_sources():
    """
    Get information about all data sources.
    """
    logger.info("Fetching data sources information")
    
    try:
        # Get data sources summary
        sources_summary = provenance_tracker.get_data_sources_summary()
        
        return {
            "summary": sources_summary,
            "sources": [
                {
                    "id": "who_global_health",
                    "name": "WHO Global Health Observatory",
                    "url": "https://www.who.int/data/gho",
                    "type": "who_global_health",
                    "reliability_score": 0.95,
                    "coverage": ["life_expectancy", "mortality", "health_workforce"],
                    "last_updated": (datetime.now() - timedelta(days=2)).isoformat(),
                    "status": "active"
                },
                {
                    "id": "world_bank",
                    "name": "World Bank Data",
                    "url": "https://data.worldbank.org/indicator",
                    "type": "world_bank",
                    "reliability_score": 0.92,
                    "coverage": ["health_expenditure", "gdp", "population"],
                    "last_updated": (datetime.now() - timedelta(days=1)).isoformat(),
                    "status": "active"
                },
            ]
        }
        
    except Exception as e:
        logger.error("Error fetching data sources", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve data sources")

@router.get("/alerts", response_model=List[Dict[str, Any]], status_code=status.HTTP_200_OK)
async def get_quality_alerts(severity: Optional[str] = None, resolved: bool = False):
    """
    Get quality alerts with optional filtering.
    """
    logger.info("Fetching quality alerts", severity=severity, resolved=resolved)
    
    try:
        # Mock alerts data
        alerts = [
            {
                "id": "alert_001",
                "type": "freshness",
                "severity": "medium",
                "message": "Greece health spending data 3 days old",
                "affected_indicators": ["health_spending"],
                "affected_countries": ["GRC"],
                "created_at": (datetime.now() - timedelta(hours=2)).isoformat(),
                "resolved": False,
                "recommendations": ["Update data from source", "Check data pipeline"]
            },
            {
                "id": "alert_002",
                "type": "validity",
                "severity": "low",
                "message": "Portugal nurse density outlier detected",
                "affected_indicators": ["nurse_density"],
                "affected_countries": ["PRT"],
                "created_at": (datetime.now() - timedelta(hours=6)).isoformat(),
                "resolved": False,
                "recommendations": ["Verify outlier data with source"]
            },
            {
                "id": "alert_003",
                "type": "completeness",
                "severity": "high",
                "message": "Spain life expectancy data missing for 2022",
                "affected_indicators": ["life_expectancy"],
                "affected_countries": ["ESP"],
                "created_at": (datetime.now() - timedelta(days=1)).isoformat(),
                "resolved": True,
                "resolved_at": (datetime.now() - timedelta(hours=12)).isoformat(),
                "recommendations": ["Data has been updated from source"]
            }
        ]
        
        # Apply filters
        if severity:
            alerts = [alert for alert in alerts if alert["severity"] == severity]
        
        if not resolved:
            alerts = [alert for alert in alerts if not alert.get("resolved", False)]
        
        return alerts
        
    except Exception as e:
        logger.error("Error fetching quality alerts", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve quality alerts")

@router.post("/alerts/{alert_id}/resolve", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def resolve_quality_alert(alert_id: str, resolution_notes: str = ""):
    """
    Resolve a quality alert.
    """
    logger.info("Resolving quality alert", alert_id=alert_id)
    
    try:
        # Mock alert resolution
        resolution_result = {
            "alert_id": alert_id,
            "resolved": True,
            "resolved_at": datetime.now().isoformat(),
            "resolution_notes": resolution_notes,
            "resolved_by": "system",  # In real implementation, this would be the user
            "status": "success"
        }
        
        return resolution_result
        
    except Exception as e:
        logger.error("Error resolving quality alert", alert_id=alert_id, exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to resolve quality alert")
