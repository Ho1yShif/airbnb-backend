"""
Rate limiting and throttling configuration for API endpoints.
"""

from django.core.cache import cache
from django.http import JsonResponse
from rest_framework.throttling import SimpleRateThrottle, UserRateThrottle, AnonRateThrottle
import logging

logger = logging.getLogger(__name__)


class CustomUserRateThrottle(UserRateThrottle):
    """
    Custom rate throttle for authenticated users.
    Limit: 1000 requests per hour per user
    """
    scope = 'user_throttle'
    
    def get_cache_key(self):
        if self.request.user and self.request.user.is_authenticated:
            return f'rate_limit_user_{self.request.user.id}'
        return None


class CustomAnonRateThrottle(AnonRateThrottle):
    """
    Custom rate throttle for anonymous users.
    Limit: 100 requests per hour per IP
    """
    scope = 'anon_throttle'
    
    def get_cache_key(self):
        if self.request.user and self.request.user.is_authenticated:
            return None  # Skip for authenticated users
        return f'rate_limit_anon_{self.get_ident(self.request)}'


class StrictRateThrottle(UserRateThrottle):
    """
    Strict rate throttle for sensitive endpoints (auth, payments).
    Limit: 10 requests per minute per user
    """
    scope = 'strict_throttle'
    
    def get_cache_key(self):
        ident = self.request.user.id if self.request.user and self.request.user.is_authenticated else self.get_ident(self.request)
        return f'rate_limit_strict_{ident}'


class BurstRateThrottle(AnonRateThrottle):
    """
    Burst throttle for public endpoints (listings).
    Limit: 5000 requests per hour
    """
    scope = 'burst_throttle'
    
    def get_cache_key(self):
        ident = self.request.user.id if self.request.user and self.request.user.is_authenticated else self.get_ident(self.request)
        return f'rate_limit_burst_{ident}'


class RateLimitMiddleware:
    """
    Custom middleware for advanced rate limiting with per-endpoint configuration.
    """
    
    # Endpoints with special rate limits (key: path pattern, value: requests per hour)
    ENDPOINT_LIMITS = {
        '/api/register/': 5,           # 5 per hour
        '/api/token/': 10,             # 10 per hour (login attempts)
        '/api/password-reset/': 3,     # 3 per hour
        '/api/send-email/': 20,        # 20 per hour
        '/api/bookings/': 50,          # 50 per hour
        '/api/reviews/': 50,           # 50 per hour
    }
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check rate limit
        if not self.is_rate_limited(request):
            response = self.get_response(request)
            return response
        else:
            return JsonResponse(
                {'error': 'Rate limit exceeded. Please try again later.'},
                status=429
            )
    
    def is_rate_limited(self, request):
        """
        Check if request exceeds rate limit.
        Returns True if limited, False if allowed.
        """
        # Skip rate limiting for health checks
        if request.path in ['/health/', '/health/live/', '/health/ready/', '/metrics/']:
            return False
        
        # Get client identifier
        client_id = self.get_client_id(request)
        cache_key = f'rate_limit_{client_id}_{self.get_path_pattern(request.path)}'
        
        # Get limit for this endpoint
        limit = self.get_rate_limit(request.path)
        
        # Check current request count
        current_count = cache.get(cache_key, 0)
        
        if current_count >= limit:
            logger.warning(f'Rate limit exceeded for {client_id} on {request.path}')
            return True
        
        # Increment counter (expire after 1 hour)
        cache.set(cache_key, current_count + 1, 3600)
        return False
    
    def get_client_id(self, request):
        """Get unique identifier for client (user ID or IP address)"""
        if request.user and request.user.is_authenticated:
            return f'user_{request.user.id}'
        
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        return f'ip_{ip}'
    
    def get_path_pattern(self, path):
        """Normalize path for rate limiting"""
        # Extract base path
        parts = path.strip('/').split('/')
        if parts:
            return parts[0]  # e.g., 'api', 'health'
        return 'root'
    
    def get_rate_limit(self, path):
        """Get rate limit for a specific path"""
        for pattern, limit in self.ENDPOINT_LIMITS.items():
            if pattern in path:
                return limit
        
        # Default limits
        if path.startswith('/api/'):
            return 1000  # 1000 requests per hour for general API
        elif path.startswith('/health'):
            return 10000  # Health checks have higher limit
        else:
            return 100  # Conservative default
