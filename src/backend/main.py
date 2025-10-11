"""
Policy Simulation Assistant - FastAPI Backend
GenAI-powered healthcare policy simulation tool
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import structlog
from contextlib import asynccontextmanager

from src.backend.core.config import settings
from src.backend.core.database import init_db
from src.backend.api.routes import health_indicators, simulations, ai_narrative
from src.backend.api.routes.simulation_api import router as simulation_router
from src.backend.core.middleware import LoggingMiddleware, RateLimitMiddleware
from src.backend.core.exceptions import PolicySimulationException

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting Policy Simulation Assistant API")
    await init_db()
    logger.info("Database initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Policy Simulation Assistant API")


# Create FastAPI application
app = FastAPI(
    title="Policy Simulation Assistant API",
    description="GenAI-powered healthcare policy simulation tool for policy makers",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware)

# Include API routes
app.include_router(
    health_indicators.router,
    prefix="/api/health-indicators",
    tags=["Health Indicators"]
)

app.include_router(
    simulations.router,
    prefix="/api/simulations",
    tags=["Policy Simulations"]
)

app.include_router(
    ai_narrative.router,
    prefix="/api/ai",
    tags=["AI Narrative Generation"]
)

app.include_router(
    simulation_router,
    tags=["Feature 1: Policy Simulation Engine"]
)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Policy Simulation Assistant API",
        "version": "1.0.0",
        "description": "GenAI-powered healthcare policy simulation tool",
        "docs_url": "/docs" if settings.DEBUG else "Documentation disabled in production",
        "health_check": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT
    }


@app.exception_handler(PolicySimulationException)
async def policy_simulation_exception_handler(request, exc: PolicySimulationException):
    """Handle custom policy simulation exceptions"""
    logger.error(
        "Policy simulation error",
        error=str(exc),
        error_code=exc.error_code,
        path=request.url.path
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_code,
            "message": str(exc),
            "details": exc.details
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Handle HTTP exceptions with structured logging"""
    logger.error(
        "HTTP error",
        status_code=exc.status_code,
        detail=exc.detail,
        path=request.url.path
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "http_error",
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """Handle unexpected exceptions"""
    logger.error(
        "Unexpected error",
        error=str(exc),
        path=request.url.path,
        exc_info=True
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "internal_server_error",
            "message": "An unexpected error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
