"""
Simulation API routes for Feature 1 implementation.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
import logging
import os
from ...models.simulation_models import (
    SimulationRequest, SimulationResponse, CountriesResponse, 
    CountryInfo, BaselineData, ModelInfo
)
from ...core.database import get_db
from ...services.simulation_engine import PolicySimulationEngine
from ...services.data_processor import HealthDataProcessor

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/simulations", tags=["simulations"])

# Initialize services
simulation_engine = PolicySimulationEngine()
data_processor = HealthDataProcessor()

# Global variables for caching
baseline_data_cache = {}
model_trained = False

async def initialize_services():
    """Initialize the simulation engine with training data."""
    global baseline_data_cache, model_trained
    
    try:
        # Get data directory path
        data_dir = os.path.join(os.path.dirname(__file__), "../../../adapt_context/data")
        
        # Load and merge health data
        health_data = data_processor.merge_health_data(data_dir)
        
        # Train the model
        model_metrics = simulation_engine.train_model(health_data)
        model_trained = True
        
        # Get baseline data
        baseline_data_cache = data_processor.get_baseline_data(health_data)
        
        logger.info(f"Services initialized. Model R² = {model_metrics.get('r2_score', 0):.3f}")
        
    except Exception as e:
        logger.error(f"Error initializing services: {e}")
        raise

@router.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    await initialize_services()

@router.post("/run", response_model=SimulationResponse)
async def run_simulation(request: SimulationRequest):
    """Run a policy simulation with given parameters."""
    try:
        if not model_trained:
            raise HTTPException(status_code=503, detail="Simulation engine not ready")
        
        if request.country not in baseline_data_cache:
            raise HTTPException(
                status_code=404, 
                detail=f"Country {request.country} not found in baseline data"
            )
        
        # Get baseline data for the country
        baseline = baseline_data_cache[request.country]
        
        # Run simulation
        simulation_result = simulation_engine.run_simulation(
            country=request.country,
            baseline_data=baseline,
            parameters=request.parameters.dict()
        )
        
        return SimulationResponse(**simulation_result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error running simulation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/countries", response_model=CountriesResponse)
async def get_available_countries():
    """Get list of available countries for simulation."""
    try:
        if not baseline_data_cache:
            raise HTTPException(status_code=503, detail="Baseline data not loaded")
        
        countries = []
        country_names = {
            'PRT': 'Portugal',
            'ESP': 'Spain', 
            'SWE': 'Sweden',
            'GRC': 'Greece',
            'DEU': 'Germany',
            'FRA': 'France',
            'ITA': 'Italy',
            'GBR': 'United Kingdom',
            'USA': 'United States',
            'CAN': 'Canada'
        }
        
        for country_code, baseline in baseline_data_cache.items():
            country_name = country_names.get(country_code, country_code)
            
            countries.append(CountryInfo(
                code=country_code,
                name=country_name,
                baseline=BaselineData(**baseline),
                data_quality=98.4  # From ADAPT analysis
            ))
        
        return CountriesResponse(countries=countries)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting countries: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/model/info", response_model=ModelInfo)
async def get_model_info():
    """Get information about the trained simulation model."""
    try:
        if not model_trained:
            raise HTTPException(status_code=503, detail="Model not trained")
        
        model_info = simulation_engine.get_model_info()
        return ModelInfo(**model_info)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/model/retrain")
async def retrain_model():
    """Retrain the simulation model with latest data."""
    try:
        # Get data directory path
        data_dir = os.path.join(os.path.dirname(__file__), "../../../adapt_context/data")
        
        # Load and merge health data
        health_data = data_processor.merge_health_data(data_dir)
        
        # Train the model
        model_metrics = simulation_engine.train_model(health_data)
        
        # Update baseline data
        global baseline_data_cache
        baseline_data_cache = data_processor.get_baseline_data(health_data)
        
        return {
            "status": "success",
            "model_metrics": model_metrics,
            "countries_loaded": len(baseline_data_cache)
        }
        
    except Exception as e:
        logger.error(f"Error retraining model: {e}")
        raise HTTPException(status_code=500, detail=str(e))
