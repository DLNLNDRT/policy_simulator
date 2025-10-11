"""
AI narrative generation API routes
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import structlog

from src.backend.core.database import get_db
from src.backend.core.exceptions import AIError, ValidationError
from src.backend.models.ai import (
    NarrativeRequest,
    NarrativeResponse,
    NarrativeValidationRequest
)
from src.backend.services.ai import AIService
from src.backend.services.cost_tracking import CostTrackingService

logger = structlog.get_logger()
router = APIRouter()


@router.post("/narrative", response_model=NarrativeResponse)
async def generate_narrative(
    request: NarrativeRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Generate AI narrative for simulation results"""
    
    logger.info(
        "Generating AI narrative",
        country=request.country,
        simulation_type=request.simulation_type
    )
    
    try:
        # Initialize services
        ai_service = AIService()
        cost_service = CostTrackingService(db)
        
        # Validate request
        await ai_service.validate_narrative_request(request)
        
        # Generate narrative
        narrative_result = await ai_service.generate_narrative(request)
        
        # Track cost in background
        background_tasks.add_task(
            cost_service.track_ai_cost,
            narrative_result.cost_usd,
            request.country
        )
        
        logger.info(
            "AI narrative generated successfully",
            country=request.country,
            cost_usd=narrative_result.cost_usd,
            narrative_length=len(narrative_result.narrative)
        )
        
        return narrative_result
        
    except ValidationError as e:
        logger.warning(
            "Narrative validation failed",
            error=str(e),
            country=request.country
        )
        raise
    except AIError as e:
        logger.error(
            "AI narrative generation failed",
            error=str(e),
            country=request.country
        )
        raise
    except Exception as e:
        logger.error(
            "Unexpected AI narrative error",
            error=str(e),
            country=request.country,
            exc_info=True
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/validate", response_model=dict)
async def validate_narrative(
    request: NarrativeValidationRequest,
    db: Session = Depends(get_db)
):
    """Validate AI-generated narrative for safety and accuracy"""
    
    logger.info(
        "Validating AI narrative",
        narrative_length=len(request.narrative)
    )
    
    try:
        ai_service = AIService()
        validation_result = await ai_service.validate_narrative(request)
        
        logger.info(
            "Narrative validation completed",
            is_valid=validation_result["is_valid"],
            issues_count=len(validation_result.get("issues", []))
        )
        
        return validation_result
        
    except Exception as e:
        logger.error(
            "Error validating narrative",
            error=str(e)
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/costs", response_model=dict)
async def get_ai_costs(
    time_period: str = "24h",
    db: Session = Depends(get_db)
):
    """Get AI usage costs and statistics"""
    
    logger.info(
        "Fetching AI cost statistics",
        time_period=time_period
    )
    
    try:
        cost_service = CostTrackingService(db)
        cost_stats = await cost_service.get_ai_cost_statistics(time_period)
        
        logger.info(
            "AI cost statistics retrieved",
            total_cost=cost_stats.get("total_cost_usd"),
            total_requests=cost_stats.get("total_requests")
        )
        
        return cost_stats
        
    except Exception as e:
        logger.error(
            "Error fetching AI cost statistics",
            error=str(e)
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/health", response_model=dict)
async def check_ai_health():
    """Check AI service health and availability"""
    
    logger.info("Checking AI service health")
    
    try:
        ai_service = AIService()
        health_status = await ai_service.check_health()
        
        logger.info(
            "AI service health check completed",
            status=health_status["status"],
            services=health_status.get("services", {})
        )
        
        return health_status
        
    except Exception as e:
        logger.error(
            "AI service health check failed",
            error=str(e)
        )
        raise HTTPException(status_code=503, detail="AI service unavailable")
