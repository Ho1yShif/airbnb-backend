"""
Performance monitoring and request tracking middleware.

Tracks:
- Response times
- Request/response sizes
- Database query counts
- Cache hits/misses
"""

import time
import logging
from django.db import connection
from django.conf import settings

logger = logging.getLogger(__name__)


class PerformanceMonitoringMiddleware:
    """
    Middleware to monitor request performance and log slow requests.
    
    Logs:
    - Request duration
    - Database queries executed
    - Response size
    - Status code
    """

    SLOW_REQUEST_THRESHOLD = 1.0  # seconds

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip health check endpoints to reduce logging noise
        if self._should_skip(request.path):
            return self.get_response(request)

        start_time = time.time()
        start_queries = len(connection.queries)

        response = self.get_response(request)

        duration = time.time() - start_time
        query_count = len(connection.queries) - start_queries

        # Log slow requests
        if duration > self.SLOW_REQUEST_THRESHOLD:
            logger.warning(
                f'Slow request: {request.method} {request.path} '
                f'took {duration:.2f}s, {query_count} queries, '
                f'status {response.status_code}'
            )
        else:
            logger.debug(
                f'Request: {request.method} {request.path} '
                f'duration {duration:.3f}s, {query_count} queries, '
                f'status {response.status_code}'
            )

        # Add performance headers to response
        response['X-Response-Time'] = f'{duration:.3f}s'
        response['X-DB-Queries'] = str(query_count)

        return response

    @staticmethod
    def _should_skip(path):
        """Skip logging for health checks and static files."""
        skip_paths = ['/health/', '/health/ready/', '/health/live/', '/static/']
        return any(path.startswith(p) for p in skip_paths)
