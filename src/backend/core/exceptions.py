"""
Custom exceptions for Policy Simulation Assistant
"""

from fastapi import HTTPException, status
from typing import Optional, Dict, Any


class PolicySimulationException(Exception):
    """Base exception for policy simulation errors"""
    
    def __init__(
        self,
        message: str,
        error_code: str = "policy_simulation_error",
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class DataQualityError(PolicySimulationException):
    """Data quality validation error"""
    
    def __init__(self, message: str, quality_score: Optional[float] = None):
        super().__init__(
            message=message,
            error_code="data_quality_error",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details={"quality_score": quality_score}
        )


class SimulationError(PolicySimulationException):
    """Simulation calculation error"""
    
    def __init__(self, message: str, simulation_params: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="simulation_error",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details={"simulation_params": simulation_params}
        )


class AIError(PolicySimulationException):
    """AI service error"""
    
    def __init__(self, message: str, ai_service: Optional[str] = None):
        super().__init__(
            message=message,
            error_code="ai_error",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details={"ai_service": ai_service}
        )


class RateLimitError(PolicySimulationException):
    """Rate limiting error"""
    
    def __init__(self, message: str, retry_after: Optional[int] = None):
        super().__init__(
            message=message,
            error_code="rate_limit_error",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            details={"retry_after": retry_after}
        )


class CostLimitError(PolicySimulationException):
    """Cost limit exceeded error"""
    
    def __init__(self, message: str, current_cost: Optional[float] = None, limit: Optional[float] = None):
        super().__init__(
            message=message,
            error_code="cost_limit_error",
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            details={"current_cost": current_cost, "limit": limit}
        )


class DataNotFoundError(PolicySimulationException):
    """Data not found error"""
    
    def __init__(self, message: str, country: Optional[str] = None, year: Optional[int] = None):
        super().__init__(
            message=message,
            error_code="data_not_found",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"country": country, "year": year}
        )


class ValidationError(PolicySimulationException):
    """Input validation error"""
    
    def __init__(self, message: str, field_errors: Optional[Dict[str, str]] = None):
        super().__init__(
            message=message,
            error_code="validation_error",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details={"field_errors": field_errors}
        )
