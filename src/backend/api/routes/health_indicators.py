"""
Health indicators API routes
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import structlog

from src.backend.core.database import get_db, HealthIndicator
from src.backend.core.exceptions import DataNotFoundError, ValidationError
from src.backend.models.health_indicators import HealthIndicatorResponse, HealthIndicatorRequest
from src.backend.services.health_indicators import HealthIndicatorService

logger = structlog.get_logger()
router = APIRouter()


@router.get("/", response_model=List[HealthIndicatorResponse])
async def get_health_indicators(
    country: Optional[str] = Query(None, description="ISO3 country code"),
    year: Optional[int] = Query(None, description="Year (2000-2024)"),
    metric_name: Optional[str] = Query(None, description="Metric name filter"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    db: Session = Depends(get_db)
):
    """Get health indicators with optional filtering"""
    
    logger.info(
        "Fetching health indicators",
        country=country,
        year=year,
        metric_name=metric_name,
        limit=limit,
        offset=offset
    )
    
    try:
        service = HealthIndicatorService(db)
        indicators = await service.get_indicators(
            country=country,
            year=year,
            metric_name=metric_name,
            limit=limit,
            offset=offset
        )
        
        logger.info(
            "Health indicators retrieved",
            count=len(indicators),
            country=country,
            year=year
        )
        
        return indicators
        
    except Exception as e:
        logger.error(
            "Error fetching health indicators",
            error=str(e),
            country=country,
            year=year
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/country/{country_code}", response_model=HealthIndicatorResponse)
async def get_country_indicators(
    country_code: str,
    year: Optional[int] = Query(None, description="Year (2000-2024)"),
    db: Session = Depends(get_db)
):
    """Get health indicators for a specific country"""
    
    logger.info(
        "Fetching country indicators",
        country_code=country_code,
        year=year
    )
    
    try:
        service = HealthIndicatorService(db)
        indicators = await service.get_country_indicators(
            country_code=country_code,
            year=year
        )
        
        if not indicators:
            raise DataNotFoundError(
                f"No health indicators found for country {country_code}",
                country=country_code,
                year=year
            )
        
        logger.info(
            "Country indicators retrieved",
            country_code=country_code,
            year=year,
            metrics_count=len(indicators.metrics)
        )
        
        return indicators
        
    except DataNotFoundError:
        raise
    except Exception as e:
        logger.error(
            "Error fetching country indicators",
            error=str(e),
            country_code=country_code,
            year=year
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/countries", response_model=List[str])
async def get_available_countries(db: Session = Depends(get_db)):
    """Get list of available countries"""
    
    logger.info("Fetching available countries")
    
    try:
        service = HealthIndicatorService(db)
        countries = await service.get_available_countries()
        
        logger.info(
            "Available countries retrieved",
            count=len(countries)
        )
        
        return countries
        
    except Exception as e:
        logger.error(
            "Error fetching available countries",
            error=str(e)
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/metrics", response_model=List[str])
async def get_available_metrics(db: Session = Depends(get_db)):
    """Get list of available health metrics"""
    
    logger.info("Fetching available metrics")
    
    try:
        service = HealthIndicatorService(db)
        metrics = await service.get_available_metrics()
        
        logger.info(
            "Available metrics retrieved",
            count=len(metrics)
        )
        
        return metrics
        
    except Exception as e:
        logger.error(
            "Error fetching available metrics",
            error=str(e)
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/years", response_model=List[int])
async def get_available_years(
    country: Optional[str] = Query(None, description="ISO3 country code"),
    db: Session = Depends(get_db)
):
    """Get list of available years"""
    
    logger.info(
        "Fetching available years",
        country=country
    )
    
    try:
        service = HealthIndicatorService(db)
        years = await service.get_available_years(country=country)
        
        logger.info(
            "Available years retrieved",
            count=len(years),
            country=country
        )
        
        return years
        
    except Exception as e:
        logger.error(
            "Error fetching available years",
            error=str(e),
            country=country
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/quality", response_model=dict)
async def get_data_quality_metrics(db: Session = Depends(get_db)):
    """Get data quality metrics"""
    
    logger.info("Fetching data quality metrics")
    
    try:
        service = HealthIndicatorService(db)
        quality_metrics = await service.get_data_quality_metrics()
        
        logger.info(
            "Data quality metrics retrieved",
            overall_score=quality_metrics.get("overall_score")
        )
        
        return quality_metrics
        
    except Exception as e:
        logger.error(
            "Error fetching data quality metrics",
            error=str(e)
        )
        raise HTTPException(status_code=500, detail="Internal server error")
