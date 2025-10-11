"""
Database configuration and models for Policy Simulation Assistant
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
from typing import Generator
import os

from src.backend.core.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


class HealthIndicator(Base):
    """Health indicators data model"""
    __tablename__ = "health_indicators"
    
    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(3), nullable=False, index=True)  # ISO3 code
    year = Column(Integer, nullable=False, index=True)
    metric_name = Column(String(100), nullable=False, index=True)
    value = Column(Float, nullable=False)
    unit = Column(String(50))
    source = Column(String(200))
    quality_score = Column(Float, default=100.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SimulationCache(Base):
    """Simulation results cache model"""
    __tablename__ = "simulation_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(3), nullable=False, index=True)
    baseline_data = Column(JSON, nullable=False)
    simulation_params = Column(JSON, nullable=False)
    predicted_outcome = Column(JSON, nullable=False)
    confidence_interval = Column(JSON)
    narrative_text = Column(Text)
    model_version = Column(String(50))
    cost_usd = Column(Float, default=0.0)
    response_time_ms = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DataQualityMetrics(Base):
    """Data quality metrics model"""
    __tablename__ = "data_quality_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    dataset_name = Column(String(100), nullable=False, index=True)
    quality_score = Column(Float, nullable=False)
    completeness_pct = Column(Float)
    validity_pct = Column(Float)
    consistency_pct = Column(Float)
    issues = Column(JSON)
    measured_at = Column(DateTime(timezone=True), server_default=func.now())


class UserSession(Base):
    """User session tracking model"""
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), nullable=False, unique=True, index=True)
    user_agent = Column(String(500))
    ip_address = Column(String(45))
    simulations_run = Column(Integer, default=0)
    total_cost_usd = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_activity = Column(DateTime(timezone=True), onupdate=func.now())


def get_db() -> Generator[Session, None, None]:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_db():
    """Initialize database tables"""
    # Create data directory if it doesn't exist
    if "sqlite" in settings.DATABASE_URL:
        data_dir = os.path.dirname(settings.DATABASE_URL.replace("sqlite:///", ""))
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir, exist_ok=True)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
