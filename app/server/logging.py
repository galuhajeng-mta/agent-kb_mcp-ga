# app/server/logging.py
# Placeholder for server logging configuration

import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger("api-logger")
logger.setLevel(logging.INFO)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log request info
        logger.info(f"Incoming request: {request.method} {request.url}")

        response = await call_next(request)

        # Log response info
        process_time = (time.time() - start_time) * 1000
        logger.info(
            f"Completed in {process_time:.2f}ms with status {response.status_code}"
        )

        return response
