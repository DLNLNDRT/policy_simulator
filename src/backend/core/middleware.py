"""
Middleware for Policy Simulation Assistant
"""

from fastapi import Request, Response
from fastapi.responses import JSONResponse
import time
import structlog
from typing import Callable
import asyncio
from collections import defaultdict, deque
from datetime import datetime, timedelta

from src.backend.core.config import settings
from src.backend.core.exceptions import RateLimitError

logger = structlog.get_logger()


class LoggingMiddleware:
    """Request/response logging middleware"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        request = Request(scope, receive)
        start_time = time.time()
        
        # Log request
        logger.info(
            "Request started",
            method=request.method,
            url=str(request.url),
            client_ip=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent")
        )
        
        # Process request
        response_sent = False
        
        async def send_wrapper(message):
            nonlocal response_sent
            if message["type"] == "http.response.start" and not response_sent:
                response_sent = True
                process_time = time.time() - start_time
                
                logger.info(
                    "Request completed",
                    method=request.method,
                    url=str(request.url),
                    status_code=message["status"],
                    process_time=process_time
                )
            
            await send(message)
        
        await self.app(scope, receive, send_wrapper)


class RateLimitMiddleware:
    """Rate limiting middleware"""
    
    def __init__(self, app):
        self.app = app
        self.requests = defaultdict(lambda: deque())
        self.cleanup_interval = 60  # Clean up every minute
        self.last_cleanup = time.time()
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        request = Request(scope, receive)
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()
        
        # Clean up old requests periodically
        if current_time - self.last_cleanup > self.cleanup_interval:
            await self._cleanup_old_requests(current_time)
            self.last_cleanup = current_time
        
        # Check rate limit
        if await self._is_rate_limited(client_ip, current_time):
            response = JSONResponse(
                status_code=429,
                content={
                    "error": "rate_limit_exceeded",
                    "message": "Too many requests. Please try again later.",
                    "retry_after": 60
                }
            )
            await response(scope, receive, send)
            return
        
        # Record request
        self.requests[client_ip].append(current_time)
        
        await self.app(scope, receive, send)
    
    async def _is_rate_limited(self, client_ip: str, current_time: float) -> bool:
        """Check if client is rate limited"""
        client_requests = self.requests[client_ip]
        
        # Remove requests older than 1 minute
        cutoff_time = current_time - 60
        while client_requests and client_requests[0] < cutoff_time:
            client_requests.popleft()
        
        # Check if limit exceeded
        return len(client_requests) >= settings.RATE_LIMIT_PER_MINUTE
    
    async def _cleanup_old_requests(self, current_time: float):
        """Clean up old request records"""
        cutoff_time = current_time - 300  # 5 minutes
        
        for client_ip in list(self.requests.keys()):
            client_requests = self.requests[client_ip]
            
            # Remove old requests
            while client_requests and client_requests[0] < cutoff_time:
                client_requests.popleft()
            
            # Remove empty entries
            if not client_requests:
                del self.requests[client_ip]
