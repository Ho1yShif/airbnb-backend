"""
Caching utilities and decorators for API endpoints.

Implements caching strategy for:
- Property listings (cache for 1 hour)
- Reviews (cache for 30 minutes)
- User profiles (cache for 15 minutes)
- Search results (cache for 5 minutes)
"""

from django.views.decorators.cache import cache_page
from django.views.decorators.http import condition
from django.core.cache import cache
from django.utils.decorators import method_decorator
from functools import wraps
import hashlib
import logging

logger = logging.getLogger(__name__)

# Cache TTL (Time To Live) in seconds
CACHE_TTL = {
    'properties': 3600,      # 1 hour
    'property_detail': 1800, # 30 minutes
    'reviews': 1800,         # 30 minutes
    'profiles': 900,         # 15 minutes
    'search': 300,           # 5 minutes
    'bookings': 600,         # 10 minutes
}


def cache_response(ttl_key='properties', cache_key_func=None):
    """
    Decorator to cache API responses.
    
    Usage:
        @cache_response(ttl_key='properties')
        def list_properties(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Generate cache key
            if cache_key_func:
                cache_key = cache_key_func(request, *args, **kwargs)
            else:
                cache_key = f"{view_func.__name__}_{request.path}_{request.GET.urlencode()}"
            
            # Try to get from cache
            cached_response = cache.get(cache_key)
            if cached_response is not None:
                logger.debug(f'Cache HIT: {cache_key}')
                return cached_response
            
            # Call view and cache result
            logger.debug(f'Cache MISS: {cache_key}')
            response = view_func(request, *args, **kwargs)
            
            ttl = CACHE_TTL.get(ttl_key, 600)
            cache.set(cache_key, response, ttl)
            
            return response
        
        return wrapper
    return decorator


def get_properties_cache_key(request, *args, **kwargs):
    """Generate cache key for property listings"""
    page = request.GET.get('page', '1')
    filters = request.GET.urlencode()
    return f'properties_page_{page}_{filters}'


def get_property_detail_cache_key(request, *args, **kwargs):
    """Generate cache key for single property"""
    property_id = kwargs.get('pk')
    return f'property_detail_{property_id}'


def get_reviews_cache_key(request, *args, **kwargs):
    """Generate cache key for reviews"""
    page = request.GET.get('page', '1')
    property_id = request.GET.get('property', '')
    return f'reviews_property_{property_id}_page_{page}'


def get_profile_cache_key(request, *args, **kwargs):
    """Generate cache key for user profile"""
    user_id = request.user.id if request.user.is_authenticated else 'anon'
    return f'profile_{user_id}'


def invalidate_cache(pattern):
    """
    Invalidate cache entries matching a pattern.
    
    Usage:
        invalidate_cache('property_*')
    """
    # Note: Redis-specific implementation
    # For other backends, you may need different approaches
    try:
        from django_redis import get_redis_connection
        redis_conn = get_redis_connection('default')
        
        # Find all keys matching pattern
        keys = redis_conn.keys(pattern)
        if keys:
            redis_conn.delete(*keys)
            logger.info(f'Invalidated {len(keys)} cache keys matching {pattern}')
    except Exception as e:
        logger.warning(f'Failed to invalidate cache: {e}')


def cache_bust_on_change(cache_patterns):
    """
    Decorator to bust cache when data changes (POST, PUT, PATCH, DELETE).
    
    Usage:
        @cache_bust_on_change(['property_*', 'properties_*'])
        def create_property(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)
            
            # Bust cache on mutations
            if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                for pattern in cache_patterns:
                    invalidate_cache(pattern)
            
            return response
        
        return wrapper
    return decorator


class CachedPropertyMixin:
    """
    Mixin for ViewSets to add caching to list and retrieve actions.
    
    Usage:
        class PropertyViewSet(CachedPropertyMixin, viewsets.ModelViewSet):
            queryset = Property.objects.all()
            serializer_class = PropertySerializer
    """
    
    @method_decorator(cache_page(CACHE_TTL['properties']))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(CACHE_TTL['property_detail']))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class CachedReviewMixin:
    """Mixin for caching review list and detail endpoints"""
    
    @method_decorator(cache_page(CACHE_TTL['reviews']))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(CACHE_TTL['reviews']))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


# Cache warming functions
def warm_popular_properties_cache():
    """
    Pre-load cache with popular/frequently accessed properties.
    Run periodically via Celery task.
    """
    from listings.models import Property
    
    # Get top 10 rated properties
    popular = Property.objects.filter(
        listing_status='available'
    ).order_by('-listed_on')[:10]
    
    for prop in popular:
        cache_key = f'property_detail_{prop.id}'
        from listings.serializers import PropertySerializer
        serialized = PropertySerializer(prop).data
        cache.set(cache_key, serialized, CACHE_TTL['property_detail'])
    
    logger.info(f'Warmed cache for {len(popular)} properties')


def warm_homepage_cache():
    """
    Pre-load cache with homepage data.
    Run periodically via Celery task.
    """
    from listings.models import Property, Review
    
    # Cache featured properties
    cache_key = 'homepage_featured_properties'
    properties = Property.objects.filter(
        listing_status='available'
    ).order_by('-listed_on')[:6]
    
    from listings.serializers import PropertySerializer
    serialized = PropertySerializer(properties, many=True).data
    cache.set(cache_key, serialized, CACHE_TTL['properties'])
    
    logger.info('Warmed homepage cache')


# Cache statistics
def get_cache_stats():
    """Get cache performance statistics"""
    try:
        from django_redis import get_redis_connection
        redis_conn = get_redis_connection('default')
        
        info = redis_conn.info()
        return {
            'used_memory': info.get('used_memory_human'),
            'connected_clients': info.get('connected_clients'),
            'total_commands': info.get('total_commands_processed'),
            'hits': info.get('keyspace_hits', 0),
            'misses': info.get('keyspace_misses', 0),
            'total_keys': sum(info.get(f'db{i}', {}).get('keys', 0) for i in range(16)),
        }
    except Exception as e:
        logger.warning(f'Failed to get cache stats: {e}')
        return None


def clear_all_cache():
    """Clear entire cache (use with caution)"""
    try:
        cache.clear()
        logger.warning('All cache cleared')
    except Exception as e:
        logger.error(f'Failed to clear cache: {e}')
