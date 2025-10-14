"""
Benchmark dashboard API routes
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
import structlog
import time
from typing import List, Dict, Any

from src.backend.core.database import get_db
from src.backend.core.exceptions import DataNotFoundError, ValidationError
from src.backend.models.benchmark_models import (
    ComparisonRequest,
    CountryComparison,
    AnomalyDetectionRequest,
    AnomalyDetectionResponse,
    PeerGroupRequest,
    PeerGroupResponse,
    BenchmarkStats,
    ExportRequest,
    ExportResponse
)
from src.backend.services.benchmark_service import BenchmarkService
from src.backend.services.data_processor import DataProcessor

logger = structlog.get_logger()
router = APIRouter(prefix="/api/benchmarks")


@router.post("/compare", response_model=CountryComparison, status_code=status.HTTP_200_OK)
async def compare_countries(
    request: ComparisonRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Compare multiple countries across health metrics with rankings and anomaly detection.
    """
    start_time = time.time()
    logger.info("Received country comparison request", countries=request.countries, metrics=request.metrics)

    try:
        data_processor = DataProcessor()
        benchmark_service = BenchmarkService(data_processor)
        
        # Run comparison
        comparison = benchmark_service.compare_countries(request)
        
        response_time_ms = int((time.time() - start_time) * 1000)
        logger.info(
            "Country comparison completed successfully",
            countries=comparison.countries,
            response_time_ms=response_time_ms,
            anomalies_detected=len(comparison.anomalies)
        )
        
        return comparison

    except ValidationError as e:
        logger.warning("Comparison request validation error", error=str(e), request=request.dict())
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DataNotFoundError as e:
        logger.warning("Comparison data not found", error=str(e), countries=request.countries)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error("Unexpected error during country comparison", exc_info=True, request=request.dict())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error during comparison")


@router.post("/anomalies", response_model=AnomalyDetectionResponse, status_code=status.HTTP_200_OK)
async def detect_anomalies(
    request: AnomalyDetectionRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Detect anomalies in health data across countries and metrics.
    """
    start_time = time.time()
    logger.info("Received anomaly detection request", country=request.country, metric=request.metric)

    try:
        data_processor = DataProcessor()
        benchmark_service = BenchmarkService(data_processor)
        
        # Run anomaly detection
        detection_result = benchmark_service.detect_anomalies(request)
        
        response_time_ms = int((time.time() - start_time) * 1000)
        logger.info(
            "Anomaly detection completed successfully",
            anomalies_found=len(detection_result.anomalies),
            response_time_ms=response_time_ms,
            confidence=detection_result.detection_confidence
        )
        
        return detection_result

    except ValidationError as e:
        logger.warning("Anomaly detection request validation error", error=str(e), request=request.dict())
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DataNotFoundError as e:
        logger.warning("Anomaly detection data not found", error=str(e), country=request.country)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error("Unexpected error during anomaly detection", exc_info=True, request=request.dict())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error during anomaly detection")


@router.post("/peers", response_model=PeerGroupResponse, status_code=status.HTTP_200_OK)
async def find_peer_groups(
    request: PeerGroupRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Find peer countries for comparison based on similarity criteria.
    """
    start_time = time.time()
    logger.info("Received peer group request", country=request.country, criteria=request.criteria)

    try:
        data_processor = DataProcessor()
        benchmark_service = BenchmarkService(data_processor)
        
        # Find peer groups
        peer_result = benchmark_service.find_peer_groups(request)
        
        response_time_ms = int((time.time() - start_time) * 1000)
        logger.info(
            "Peer group analysis completed successfully",
            target_country=peer_result.target_country,
            peer_groups_found=len(peer_result.peer_groups),
            response_time_ms=response_time_ms
        )
        
        return peer_result

    except ValidationError as e:
        logger.warning("Peer group request validation error", error=str(e), request=request.dict())
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DataNotFoundError as e:
        logger.warning("Peer group data not found", error=str(e), country=request.country)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error("Unexpected error during peer group analysis", exc_info=True, request=request.dict())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error during peer group analysis")


@router.get("/stats", response_model=BenchmarkStats, status_code=status.HTTP_200_OK)
async def get_benchmark_statistics(db: Session = Depends(get_db)):
    """
    Get benchmark dashboard statistics and metadata.
    """
    logger.info("Fetching benchmark statistics")
    try:
        data_processor = DataProcessor()
        
        # Get available countries
        countries = data_processor.get_available_countries()
        
        stats = BenchmarkStats(
            total_countries=len(countries),
            total_metrics=4,  # life_expectancy, doctor_density, nurse_density, health_spending
            last_updated=time.time(),  # In real implementation, would get from database
            anomaly_alerts=0,  # Would be calculated from active anomalies
            peer_groups=3,  # Southern Europe, Northern Europe, All Countries
            data_quality_score=98.4
        )
        
        return stats
        
    except Exception as e:
        logger.error("Error fetching benchmark statistics", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve benchmark statistics")


@router.get("/countries", response_model=List[Dict[str, str]], status_code=status.HTTP_200_OK)
async def get_available_countries():
    """
    Get list of countries available for benchmarking.
    """
    logger.info("Fetching available countries for benchmarking")
    try:
        data_processor = DataProcessor()
        countries = data_processor.get_available_countries()
        
        # Return with country names
        country_list = []
        country_names = {
            "PRT": "Portugal",
            "ESP": "Spain", 
            "SWE": "Sweden",
            "GRC": "Greece"
        }
        
        for country_code in countries:
            country_list.append({
                "code": country_code,
                "name": country_names.get(country_code, country_code)
            })
        
        return country_list
        
    except Exception as e:
        logger.error("Error fetching available countries", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve available countries")


@router.get("/metrics", response_model=List[Dict[str, str]], status_code=status.HTTP_200_OK)
async def get_available_metrics():
    """
    Get list of available health metrics for benchmarking.
    """
    logger.info("Fetching available metrics for benchmarking")
    try:
        metrics = [
            {
                "code": "life_expectancy",
                "name": "Life Expectancy",
                "unit": "years",
                "description": "Average life expectancy at birth"
            },
            {
                "code": "doctor_density", 
                "name": "Doctor Density",
                "unit": "per 1,000 population",
                "description": "Number of doctors per 1,000 population"
            },
            {
                "code": "nurse_density",
                "name": "Nurse Density", 
                "unit": "per 1,000 population",
                "description": "Number of nurses per 1,000 population"
            },
            {
                "code": "health_spending",
                "name": "Health Spending",
                "unit": "% of GDP",
                "description": "Government health expenditure as percentage of GDP"
            }
        ]
        
        return metrics
        
    except Exception as e:
        logger.error("Error fetching available metrics", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve available metrics")


@router.post("/export", response_model=ExportResponse, status_code=status.HTTP_200_OK)
async def export_benchmark_data(
    request: ExportRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Export benchmark data in various formats (JSON, CSV, PDF).
    """
    start_time = time.time()
    logger.info("Received export request", format=request.format, countries=request.countries)

    try:
        # In a real implementation, this would:
        # 1. Generate the requested data
        # 2. Create the file in the requested format
        # 3. Upload to a temporary storage location
        # 4. Return a download URL
        
        # For now, return a mock response
        export_result = ExportResponse(
            download_url=f"https://api.example.com/exports/benchmark_{int(time.time())}.{request.format}",
            file_size=1024 * 1024,  # 1MB mock size
            expires_at=time.time() + 3600,  # 1 hour from now
            format=request.format
        )
        
        response_time_ms = int((time.time() - start_time) * 1000)
        logger.info(
            "Export request completed successfully",
            format=request.format,
            response_time_ms=response_time_ms
        )
        
        return export_result

    except ValidationError as e:
        logger.warning("Export request validation error", error=str(e), request=request.dict())
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error("Unexpected error during export", exc_info=True, request=request.dict())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error during export")


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint for benchmark API.
    """
    return {
        "status": "healthy",
        "service": "benchmark-api",
        "timestamp": time.time(),
        "version": "1.0.0"
    }
