"""
Analytics API routes for Policy Simulation Assistant
Provides endpoints for advanced analytics, report generation, and visualization.
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
import structlog
import time
from typing import List, Dict, Any, Optional, Tuple

from src.backend.core.database import get_db
from src.backend.core.exceptions import PolicySimulationException, DataNotFoundError, ValidationError
from src.backend.models.analytics_models import (
    TrendAnalysisRequest,
    TrendAnalysisResponse,
    CorrelationAnalysisRequest,
    CorrelationAnalysisResponse,
    ForecastRequest,
    ForecastResponse,
    StatisticalTestRequest,
    StatisticalTestResponse,
    RegressionAnalysisRequest,
    RegressionAnalysisResponse,
    ReportGenerationRequest,
    ReportGenerationResponse,
    VisualizationRequest,
    VisualizationResponse,
    DashboardRequest,
    DashboardResponse
)
from src.backend.services.advanced_analytics import AdvancedAnalyticsService
from src.backend.services.report_generation import ReportGenerationEngine
from src.backend.services.visualization_service import VisualizationService
from src.backend.services.data_processor import DataProcessor

logger = structlog.get_logger()
router = APIRouter(prefix="/api/analytics")

# Initialize services
data_processor = DataProcessor()
analytics_service = AdvancedAnalyticsService(data_processor)
report_engine = ReportGenerationEngine()
visualization_service = VisualizationService()

@router.post("/trends", response_model=TrendAnalysisResponse, status_code=status.HTTP_200_OK)
async def analyze_trends(
    request: TrendAnalysisRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Perform trend analysis on health indicators over time.
    """
    start_time = time.time()
    logger.info("Received trend analysis request", 
               indicator=request.indicator, 
               country=request.country)

    try:
        # Perform trend analysis
        result = analytics_service.perform_trend_analysis(
            indicator=request.indicator,
            country=request.country,
            time_period=request.time_period
        )
        
        if "error" in result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
        
        response_time_ms = int((time.time() - start_time) * 1000)
        
        response = TrendAnalysisResponse(
            indicator=result["indicator"],
            country=result["country"],
            time_period=result["time_period"],
            trend_direction=result["trend_direction"],
            trend_strength=result["trend_strength"],
            annual_change=result["annual_change"],
            total_change=result["total_change"],
            change_percentage=result["change_percentage"],
            statistical_significance=result["statistical_significance"],
            confidence_interval=result["confidence_interval"],
            r_squared=result["r_squared"],
            sample_size=result["sample_size"],
            data_points=result["data_points"],
            response_time_ms=response_time_ms,
            generated_at=result.get("generated_at", time.time())
        )

        logger.info("Trend analysis completed successfully",
                   indicator=response.indicator,
                   country=response.country,
                   trend_direction=response.trend_direction,
                   response_time_ms=response_time_ms)

        return response

    except ValidationError as e:
        logger.warning("Trend analysis validation error", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DataNotFoundError as e:
        logger.warning("Trend analysis data not found", error=str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error("Unexpected error during trend analysis", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error during trend analysis")

@router.post("/correlations", response_model=CorrelationAnalysisResponse, status_code=status.HTTP_200_OK)
async def analyze_correlations(
    request: CorrelationAnalysisRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Calculate correlation matrix between health indicators.
    """
    start_time = time.time()
    logger.info("Received correlation analysis request", 
               indicators=request.indicators, 
               countries=request.countries)

    try:
        # Perform correlation analysis
        result = analytics_service.calculate_correlations(
            indicators=request.indicators,
            countries=request.countries,
            time_period=request.time_period
        )
        
        if "error" in result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
        
        response_time_ms = int((time.time() - start_time) * 1000)
        
        response = CorrelationAnalysisResponse(
            indicators=result["indicators"],
            countries=result["countries"],
            time_period=result["time_period"],
            correlation_matrix=result["correlation_matrix"],
            significance_matrix=result["significance_matrix"],
            interpretation=result["interpretation"],
            sample_size=result["sample_size"],
            response_time_ms=response_time_ms,
            generated_at=result["generated_at"]
        )

        logger.info("Correlation analysis completed successfully",
                   indicators_count=len(response.indicators),
                   response_time_ms=response_time_ms)

        return response

    except ValidationError as e:
        logger.warning("Correlation analysis validation error", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error("Unexpected error during correlation analysis", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error during correlation analysis")

@router.post("/forecast", response_model=ForecastResponse, status_code=status.HTTP_200_OK)
async def generate_forecast(
    request: ForecastRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Generate forecast for health indicators.
    """
    start_time = time.time()
    logger.info("Received forecast request", 
               indicator=request.indicator, 
               country=request.country,
               forecast_years=request.forecast_years)

    try:
        # Generate forecast
        result = analytics_service.generate_forecast(
            indicator=request.indicator,
            country=request.country,
            forecast_years=request.forecast_years,
            confidence_level=request.confidence_level
        )
        
        if "error" in result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
        
        response_time_ms = int((time.time() - start_time) * 1000)
        
        response = ForecastResponse(
            indicator=result["indicator"],
            country=result["country"],
            forecast_years=result["forecast_years"],
            confidence_level=result["confidence_level"],
            model_performance=result["model_performance"],
            historical_data=result["historical_data"],
            forecast_data=result["forecast_data"],
            response_time_ms=response_time_ms,
            generated_at=result["generated_at"]
        )

        logger.info("Forecast generated successfully",
                   indicator=response.indicator,
                   country=response.country,
                   r_squared=response.model_performance["r_squared"],
                   response_time_ms=response_time_ms)

        return response

    except ValidationError as e:
        logger.warning("Forecast validation error", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DataNotFoundError as e:
        logger.warning("Forecast data not found", error=str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error("Unexpected error during forecast generation", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error during forecast generation")

@router.post("/statistical-test", response_model=StatisticalTestResponse, status_code=status.HTTP_200_OK)
async def perform_statistical_test(
    request: StatisticalTestRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Perform statistical significance test between two countries.
    """
    start_time = time.time()
    logger.info("Received statistical test request", 
               indicator=request.indicator, 
               country1=request.country1,
               country2=request.country2)

    try:
        # Perform statistical test
        result = analytics_service.statistical_significance_test(
            indicator=request.indicator,
            country1=request.country1,
            country2=request.country2,
            time_period=request.time_period
        )
        
        if "error" in result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
        
        response_time_ms = int((time.time() - start_time) * 1000)
        
        response = StatisticalTestResponse(
            indicator=result["indicator"],
            country1=result["country1"],
            country2=result["country2"],
            time_period=result["time_period"],
            test_results=result["test_results"],
            descriptive_statistics=result["descriptive_statistics"],
            interpretation=result["interpretation"],
            response_time_ms=response_time_ms,
            generated_at=result["generated_at"]
        )

        logger.info("Statistical test completed successfully",
                   indicator=response.indicator,
                   p_value=response.test_results["p_value"],
                   response_time_ms=response_time_ms)

        return response

    except ValidationError as e:
        logger.warning("Statistical test validation error", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DataNotFoundError as e:
        logger.warning("Statistical test data not found", error=str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error("Unexpected error during statistical test", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error during statistical test")

@router.post("/regression", response_model=RegressionAnalysisResponse, status_code=status.HTTP_200_OK)
async def perform_regression_analysis(
    request: RegressionAnalysisRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Perform multi-variable regression analysis.
    """
    start_time = time.time()
    logger.info("Received regression analysis request", 
               target=request.target_indicator, 
               predictors=request.predictor_indicators)

    try:
        # Perform regression analysis
        result = analytics_service.multi_variable_regression(
            target_indicator=request.target_indicator,
            predictor_indicators=request.predictor_indicators,
            countries=request.countries,
            time_period=request.time_period
        )
        
        if "error" in result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
        
        response_time_ms = int((time.time() - start_time) * 1000)
        
        response = RegressionAnalysisResponse(
            target_indicator=result["target_indicator"],
            predictor_indicators=result["predictor_indicators"],
            countries=result["countries"],
            time_period=result["time_period"],
            model_performance=result["model_performance"],
            feature_importance=result["feature_importance"],
            coefficient_significance=result["coefficient_significance"],
            sample_size=result["sample_size"],
            degrees_of_freedom=result["degrees_of_freedom"],
            interpretation=result["interpretation"],
            response_time_ms=response_time_ms,
            generated_at=result["generated_at"]
        )

        logger.info("Regression analysis completed successfully",
                   target=response.target_indicator,
                   r_squared=response.model_performance["r_squared"],
                   response_time_ms=response_time_ms)

        return response

    except ValidationError as e:
        logger.warning("Regression analysis validation error", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DataNotFoundError as e:
        logger.warning("Regression analysis data not found", error=str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error("Unexpected error during regression analysis", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error during regression analysis")

@router.post("/reports/generate", response_model=ReportGenerationResponse, status_code=status.HTTP_200_OK)
async def generate_report(
    request: ReportGenerationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Generate automated report with customizable templates.
    """
    start_time = time.time()
    logger.info("Received report generation request", 
               template=request.template,
               title=request.title)

    try:
        # Prepare report data
        report_data = {
            "simulation_results": request.simulation_data,
            "analytics_results": request.analytics_data,
            "data_sources": request.data_sources
        }
        
        # Generate report based on template
        if request.template == "executive_summary":
            result = report_engine.generate_executive_summary(report_data, request.config)
        elif request.template == "detailed_analysis":
            result = report_engine.create_detailed_report(report_data, request.config)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unknown template: {request.template}")
        
        if "error" in result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
        
        response_time_ms = int((time.time() - start_time) * 1000)
        
        response = ReportGenerationResponse(
            report_id=result["report_id"],
            title=result["title"],
            format=result["format"],
            content=result["content"],
            metadata=result["metadata"],
            response_time_ms=response_time_ms,
            generated_at=time.time()
        )

        logger.info("Report generated successfully",
                   report_id=response.report_id,
                   template=request.template,
                   response_time_ms=response_time_ms)

        return response

    except ValidationError as e:
        logger.warning("Report generation validation error", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error("Unexpected error during report generation", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error during report generation")

@router.post("/reports/export/{format}", status_code=status.HTTP_200_OK)
async def export_report(
    format: str,
    report_data: Dict[str, Any],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Export report to various formats (PDF, DOCX, PPTX).
    """
    start_time = time.time()
    logger.info("Received report export request", format=format)

    try:
        if format not in ["pdf", "docx", "pptx"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unsupported export format: {format}")
        
        # Export report based on format
        if format == "pdf":
            result = report_engine.export_to_pdf(
                report_data.get("content", ""), 
                report_data.get("filename", f"report_{int(time.time())}.pdf")
            )
        elif format == "docx":
            result = report_engine.export_to_docx(
                report_data.get("content", ""), 
                report_data.get("filename", f"report_{int(time.time())}.docx")
            )
        elif format == "pptx":
            result = report_engine.export_to_powerpoint(
                report_data, 
                report_data.get("filename", f"report_{int(time.time())}.pptx")
            )
        
        if "error" in result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
        
        response_time_ms = int((time.time() - start_time) * 1000)
        result["response_time_ms"] = response_time_ms

        logger.info("Report exported successfully",
                   format=format,
                   filename=result.get("filename"),
                   response_time_ms=response_time_ms)

        return result

    except ValidationError as e:
        logger.warning("Report export validation error", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error("Unexpected error during report export", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error during report export")

@router.post("/visualizations/create", response_model=VisualizationResponse, status_code=status.HTTP_200_OK)
async def create_visualization(
    request: VisualizationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Create advanced visualization (heatmap, scatter plot, etc.).
    """
    start_time = time.time()
    logger.info("Received visualization request", 
               chart_type=request.chart_type,
               title=request.title)

    try:
        # Create visualization based on type
        if request.chart_type == "heatmap":
            result = visualization_service.create_heatmap(request.data, request.config)
        elif request.chart_type == "scatter":
            result = visualization_service.generate_scatter_plot(request.data, request.config)
        elif request.chart_type == "custom":
            result = visualization_service.custom_chart_builder(request.chart_spec, request.data)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unsupported chart type: {request.chart_type}")
        
        if "error" in result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
        
        response_time_ms = int((time.time() - start_time) * 1000)
        
        response = VisualizationResponse(
            chart_id=result.get("chart_id", f"chart_{int(time.time())}"),
            chart_type=result.get("chart_type", request.chart_type),
            data=result.get("data", {}),
            config=result.get("config", {}),
            analysis=result.get("analysis", {}),
            metadata=result.get("metadata", {}),
            response_time_ms=response_time_ms,
            generated_at=time.time()
        )

        logger.info("Visualization created successfully",
                   chart_id=response.chart_id,
                   chart_type=response.chart_type,
                   response_time_ms=response_time_ms)

        return response

    except ValidationError as e:
        logger.warning("Visualization creation validation error", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error("Unexpected error during visualization creation", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error during visualization creation")

@router.post("/visualizations/export/{chart_id}/{format}", status_code=status.HTTP_200_OK)
async def export_visualization(
    chart_id: str,
    format: str,
    chart_data: Dict[str, Any],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Export visualization to various formats (PNG, SVG, PDF, HTML).
    """
    start_time = time.time()
    logger.info("Received visualization export request", 
               chart_id=chart_id, 
               format=format)

    try:
        if format not in ["png", "svg", "pdf", "html"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unsupported export format: {format}")
        
        # Export visualization
        result = visualization_service.export_visualization(
            chart_data, 
            format, 
            chart_data.get("export_options", {})
        )
        
        if "error" in result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
        
        response_time_ms = int((time.time() - start_time) * 1000)
        result["response_time_ms"] = response_time_ms

        logger.info("Visualization exported successfully",
                   chart_id=chart_id,
                   format=format,
                   response_time_ms=response_time_ms)

        return result

    except ValidationError as e:
        logger.warning("Visualization export validation error", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error("Unexpected error during visualization export", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error during visualization export")

@router.post("/dashboard", response_model=DashboardResponse, status_code=status.HTTP_200_OK)
async def build_dashboard(
    request: DashboardRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Build interactive dashboard with multiple visualizations.
    """
    start_time = time.time()
    logger.info("Received dashboard request", 
               title=request.title,
               components_count=len(request.components))

    try:
        # Build dashboard
        result = visualization_service.build_dashboard(
            request.dashboard_config, 
            request.data_sources
        )
        
        if "error" in result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["error"])
        
        response_time_ms = int((time.time() - start_time) * 1000)
        
        response = DashboardResponse(
            dashboard_id=result["dashboard_id"],
            dashboard=result["dashboard"],
            export_options=result["export_options"],
            metadata=result["metadata"],
            response_time_ms=response_time_ms,
            generated_at=time.time()
        )

        logger.info("Dashboard built successfully",
                   dashboard_id=response.dashboard_id,
                   components_count=response.metadata["components_count"],
                   response_time_ms=response_time_ms)

        return response

    except ValidationError as e:
        logger.warning("Dashboard building validation error", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error("Unexpected error during dashboard building", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error during dashboard building")

@router.get("/templates", status_code=status.HTTP_200_OK)
async def get_report_templates(db: Session = Depends(get_db)):
    """
    Get available report templates.
    """
    logger.info("Fetching report templates")
    
    try:
        templates = report_engine.templates
        return {
            "templates": templates,
            "count": len(templates)
        }
    except Exception as e:
        logger.error("Error fetching report templates", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch report templates")

@router.get("/chart-types", status_code=status.HTTP_200_OK)
async def get_chart_types(db: Session = Depends(get_db)):
    """
    Get available chart types for visualization.
    """
    logger.info("Fetching chart types")
    
    try:
        chart_types = visualization_service.chart_types
        return {
            "chart_types": chart_types,
            "count": len(chart_types)
        }
    except Exception as e:
        logger.error("Error fetching chart types", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch chart types")
