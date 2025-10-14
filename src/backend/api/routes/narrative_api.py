"""
Narrative generation API routes
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
import structlog
import time
from typing import List, Dict, Any

from src.backend.core.database import get_db
from src.backend.core.exceptions import PolicySimulationException, ValidationError
from src.backend.models.narrative_models import (
    NarrativeRequest,
    NarrativeResponse,
    TemplateInfo,
    NarrativeHistory,
    NarrativeStats,
    ExportRequest,
    ExportResponse,
    FeedbackRequest,
    FeedbackResponse,
    NarrativeType,
    AudienceType,
    ToneType,
    LengthType,
    FocusArea
)
from src.backend.services.narrative_service import NarrativeService

logger = structlog.get_logger()
router = APIRouter(prefix="/api/narratives")


@router.post("/generate", response_model=NarrativeResponse, status_code=status.HTTP_200_OK)
async def generate_narrative(
    request: NarrativeRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Generate a narrative based on the provided request and data source.
    """
    start_time = time.time()
    logger.info("Received narrative generation request", 
               narrative_type=request.narrative_type, 
               audience=request.audience)

    try:
        narrative_service = NarrativeService()
        
        # Generate narrative
        response = narrative_service.generate_narrative(request)
        
        response_time_ms = int((time.time() - start_time) * 1000)
        response.generation_time_ms = response_time_ms

        logger.info(
            "Narrative generation completed successfully",
            narrative_id=response.narrative_id,
            narrative_type=response.narrative_type,
            response_time_ms=response_time_ms,
            cost_usd=response.cost_usd,
            quality_score=response.quality_metrics.overall_score
        )
        
        # In a real application, you might save the narrative to a database
        # background_tasks.add_task(save_narrative_to_db, response)

        return response

    except ValidationError as e:
        logger.warning("Narrative request validation error", error=str(e), request=request.dict())
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PolicySimulationException as e:
        logger.error("Narrative generation error", error=str(e), error_code=e.error_code)
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logger.error("Unexpected error during narrative generation", exc_info=True, request=request.dict())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error during narrative generation")


@router.get("/templates", response_model=List[TemplateInfo], status_code=status.HTTP_200_OK)
async def get_narrative_templates():
    """
    Get available narrative templates.
    """
    logger.info("Fetching narrative templates")
    try:
        narrative_service = NarrativeService()
        templates = narrative_service._load_templates()
        
        template_infos = []
        for narrative_type, template_data in templates.items():
            template_info = TemplateInfo(
                template_id=narrative_type.value,
                name=template_data['name'],
                description=template_data['description'],
                narrative_type=narrative_type,
                audience=AudienceType.POLICY_MAKERS,
                tone=ToneType.FORMAL,
                length=LengthType.STANDARD,
                focus_areas=[FocusArea.POLICY_RECOMMENDATIONS],
                sections=template_data['sections'],
                word_count_range={"min": 500, "max": 2000}
            )
            template_infos.append(template_info)
        
        return template_infos
        
    except Exception as e:
        logger.error("Error fetching narrative templates", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve narrative templates")


@router.get("/history", response_model=List[NarrativeHistory], status_code=status.HTTP_200_OK)
async def get_narrative_history(
    limit: int = 10,
    offset: int = 0,
    narrative_type: Optional[NarrativeType] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve a history of generated narratives.
    """
    logger.info("Fetching narrative history", limit=limit, offset=offset, narrative_type=narrative_type)
    try:
        # In a real application, this would query the database
        # For now, return mock data
        mock_history = [
            NarrativeHistory(
                narrative_id="narr_001",
                title="Portugal Health Policy Impact Analysis",
                narrative_type=NarrativeType.SIMULATION_IMPACT,
                audience=AudienceType.POLICY_MAKERS,
                quality_score=4.2,
                word_count=1200,
                cost_usd=0.15,
                generated_at=time.time() - 3600  # 1 hour ago
            ),
            NarrativeHistory(
                narrative_id="narr_002",
                title="Southern Europe Health Benchmark Report",
                narrative_type=NarrativeType.BENCHMARK_COMPARISON,
                audience=AudienceType.MINISTERS,
                quality_score=4.5,
                word_count=1800,
                cost_usd=0.22,
                generated_at=time.time() - 7200  # 2 hours ago
            )
        ]
        
        return mock_history
        
    except Exception as e:
        logger.error("Error fetching narrative history", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve narrative history")


@router.get("/stats", response_model=NarrativeStats, status_code=status.HTTP_200_OK)
async def get_narrative_statistics(db: Session = Depends(get_db)):
    """
    Get narrative generation statistics.
    """
    logger.info("Fetching narrative statistics")
    try:
        # In a real application, this would query the database
        stats = NarrativeStats(
            total_narratives=25,
            narratives_by_type={
                "simulation_impact": 12,
                "benchmark_comparison": 8,
                "anomaly_alert": 3,
                "trend_analysis": 2
            },
            narratives_by_audience={
                "policy_makers": 15,
                "ministers": 6,
                "ngos": 3,
                "researchers": 1
            },
            average_quality_score=4.3,
            average_cost_usd=0.18,
            total_cost_usd=4.50,
            most_used_template="simulation_impact",
            last_24h_narratives=5
        )
        
        return stats
        
    except Exception as e:
        logger.error("Error fetching narrative statistics", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve narrative statistics")


@router.post("/export", response_model=ExportResponse, status_code=status.HTTP_200_OK)
async def export_narrative(
    request: ExportRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Export a narrative in the specified format.
    """
    start_time = time.time()
    logger.info("Received narrative export request", 
               narrative_id=request.narrative_id, 
               format=request.format)

    try:
        # In a real application, this would:
        # 1. Retrieve the narrative from the database
        # 2. Format it according to the requested format
        # 3. Generate a download URL
        
        # For now, return a mock response
        export_response = ExportResponse(
            download_url=f"https://api.example.com/exports/narrative_{request.narrative_id}.{request.format}",
            file_size=1024 * 1024,  # 1MB mock size
            format=request.format,
            expires_at=time.time() + 3600  # 1 hour from now
        )
        
        response_time_ms = int((time.time() - start_time) * 1000)
        logger.info(
            "Narrative export completed successfully",
            narrative_id=request.narrative_id,
            format=request.format,
            response_time_ms=response_time_ms
        )
        
        return export_response

    except ValidationError as e:
        logger.warning("Export request validation error", error=str(e), request=request.dict())
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error("Unexpected error during narrative export", exc_info=True, request=request.dict())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error during narrative export")


@router.post("/feedback", response_model=FeedbackResponse, status_code=status.HTTP_200_OK)
async def submit_feedback(
    request: FeedbackRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Submit feedback for a generated narrative.
    """
    logger.info("Received narrative feedback", narrative_id=request.narrative_id)
    try:
        # In a real application, this would save feedback to the database
        feedback_response = FeedbackResponse(
            feedback_id=f"feedback_{int(time.time())}",
            narrative_id=request.narrative_id,
            overall_rating=request.overall_rating,
            thank_you_message="Thank you for your feedback! It will help us improve our narrative generation."
        )
        
        logger.info("Feedback submitted successfully", 
                   narrative_id=request.narrative_id, 
                   overall_rating=request.overall_rating)
        
        return feedback_response

    except ValidationError as e:
        logger.warning("Feedback validation error", error=str(e), request=request.dict())
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error("Unexpected error during feedback submission", exc_info=True, request=request.dict())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error during feedback submission")


@router.get("/options", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def get_narrative_options():
    """
    Get available options for narrative generation.
    """
    logger.info("Fetching narrative options")
    try:
        options = {
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
        
        return options
        
    except Exception as e:
        logger.error("Error fetching narrative options", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve narrative options")


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint for narrative API.
    """
    return {
        "status": "healthy",
        "service": "narrative-api",
        "timestamp": time.time(),
        "version": "1.0.0"
    }
