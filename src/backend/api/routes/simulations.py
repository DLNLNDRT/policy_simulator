"""
Policy simulation API routes
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import structlog
import time

from src.backend.core.database import get_db
from src.backend.core.exceptions import SimulationError, DataNotFoundError, ValidationError
from src.backend.models.simulations import (
    SimulationRequest,
    SimulationResponse,
    SimulationHistoryResponse
)
from src.backend.services.simulation import SimulationService
from src.backend.services.cost_tracking import CostTrackingService

logger = structlog.get_logger()
router = APIRouter()


@router.post("/", response_model=SimulationResponse)
async def run_simulation(
    request: SimulationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Run a policy simulation"""
    
    start_time = time.time()
    
    logger.info(
        "Starting policy simulation",
        country=request.country,
        doctor_density_change=request.doctor_density_change,
        nurse_density_change=request.nurse_density_change,
        spending_change=request.spending_change
    )
    
    try:
        # Initialize services
        simulation_service = SimulationService(db)
        cost_service = CostTrackingService(db)
        
        # Validate request
        await simulation_service.validate_simulation_request(request)
        
        # Check for cached results
        cached_result = await simulation_service.get_cached_simulation(request)
        if cached_result:
            logger.info(
                "Using cached simulation result",
                country=request.country,
                cache_hit=True
            )
            return cached_result
        
        # Run simulation
        simulation_result = await simulation_service.run_simulation(request)
        
        # Generate AI narrative
        narrative_result = await simulation_service.generate_narrative(simulation_result)
        
        # Calculate response time
        response_time_ms = int((time.time() - start_time) * 1000)
        
        # Create response
        response = SimulationResponse(
            country=request.country,
            baseline_data=simulation_result.baseline_data,
            simulation_params=request.dict(),
            predicted_outcome=simulation_result.predicted_outcome,
            confidence_interval=simulation_result.confidence_interval,
            narrative=narrative_result.narrative,
            disclaimers=narrative_result.disclaimers,
            citations=narrative_result.citations,
            model_version=simulation_result.model_version,
            response_time_ms=response_time_ms,
            cost_usd=narrative_result.cost_usd
        )
        
        # Cache result in background
        background_tasks.add_task(
            simulation_service.cache_simulation_result,
            request,
            response
        )
        
        # Track cost in background
        background_tasks.add_task(
            cost_service.track_simulation_cost,
            response.cost_usd,
            request.country
        )
        
        logger.info(
            "Simulation completed successfully",
            country=request.country,
            predicted_change=simulation_result.predicted_outcome.get("life_expectancy_change"),
            response_time_ms=response_time_ms,
            cost_usd=response.cost_usd
        )
        
        return response
        
    except ValidationError as e:
        logger.warning(
            "Simulation validation failed",
            error=str(e),
            country=request.country
        )
        raise
    except DataNotFoundError as e:
        logger.warning(
            "Data not found for simulation",
            error=str(e),
            country=request.country
        )
        raise
    except SimulationError as e:
        logger.error(
            "Simulation calculation failed",
            error=str(e),
            country=request.country
        )
        raise
    except Exception as e:
        logger.error(
            "Unexpected simulation error",
            error=str(e),
            country=request.country,
            exc_info=True
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/history", response_model=List[SimulationHistoryResponse])
async def get_simulation_history(
    country: str = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Get simulation history"""
    
    logger.info(
        "Fetching simulation history",
        country=country,
        limit=limit,
        offset=offset
    )
    
    try:
        service = SimulationService(db)
        history = await service.get_simulation_history(
            country=country,
            limit=limit,
            offset=offset
        )
        
        logger.info(
            "Simulation history retrieved",
            count=len(history),
            country=country
        )
        
        return history
        
    except Exception as e:
        logger.error(
            "Error fetching simulation history",
            error=str(e),
            country=country
        )
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/stats", response_model=dict)
async def get_simulation_stats(db: Session = Depends(get_db)):
    """Get simulation statistics"""
    
    logger.info("Fetching simulation statistics")
    
    try:
        service = SimulationService(db)
        stats = await service.get_simulation_statistics()
        
        logger.info(
            "Simulation statistics retrieved",
            total_simulations=stats.get("total_simulations"),
            avg_response_time=stats.get("avg_response_time_ms")
        )
        
        return stats
        
    except Exception as e:
        logger.error(
            "Error fetching simulation statistics",
            error=str(e)
        )
        raise HTTPException(status_code=500, detail="Internal server error")
