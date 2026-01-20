"""
Health check endpoints for monitoring application status.

Provides:
- /health/ - Overall health status
- /health/live/ - Liveness probe (is app running?)
- /health/ready/ - Readiness probe (is app ready to serve?)
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from django.db.utils import OperationalError
from django.core.cache import cache
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
def health_check(request):
    """
    Comprehensive health check endpoint.
    
    Checks:
    - Database connectivity
    - Cache connectivity
    - Celery broker
    - Application status
    """
    health_status = {
        'status': 'healthy',
        'checks': {},
    }

    # Database check
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        health_status['checks']['database'] = {'status': 'ok'}
    except OperationalError as e:
        health_status['checks']['database'] = {'status': 'error', 'error': str(e)}
        health_status['status'] = 'unhealthy'
        logger.error(f'Database health check failed: {e}')

    # Cache check
    try:
        cache.set('health_check', 'ok', 10)
        if cache.get('health_check') == 'ok':
            health_status['checks']['cache'] = {'status': 'ok'}
        else:
            health_status['checks']['cache'] = {'status': 'error', 'error': 'Cache miss'}
            health_status['status'] = 'degraded'
    except Exception as e:
        health_status['checks']['cache'] = {'status': 'error', 'error': str(e)}
        logger.warning(f'Cache health check failed: {e}')

    # Celery check
    try:
        from celery import current_app
        if current_app.control.inspect().ping():
            health_status['checks']['celery'] = {'status': 'ok'}
        else:
            health_status['checks']['celery'] = {'status': 'error', 'error': 'No workers'}
            health_status['status'] = 'degraded'
    except Exception as e:
        health_status['checks']['celery'] = {'status': 'warning', 'error': str(e)}
        logger.warning(f'Celery health check failed: {e}')

    http_status = (
        status.HTTP_200_OK
        if health_status['status'] == 'healthy'
        else status.HTTP_503_SERVICE_UNAVAILABLE
    )

    return Response(health_status, status=http_status)


@api_view(['GET'])
def liveness_probe(request):
    """
    Kubernetes liveness probe.
    
    Returns 200 if application is running.
    Used to determine if container should be restarted.
    """
    return Response(
        {
            'status': 'alive',
            'message': 'Application is running',
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def readiness_probe(request):
    """
    Kubernetes readiness probe.
    
    Returns 200 only if application is ready to serve traffic.
    Checks critical dependencies: database, cache.
    """
    try:
        # Check database
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')

        # Check cache
        cache.set('ready_check', 'ok', 5)

        return Response(
            {
                'status': 'ready',
                'message': 'Application is ready to serve traffic',
            },
            status=status.HTTP_200_OK
        )
    except Exception as e:
        logger.error(f'Readiness check failed: {e}')
        return Response(
            {
                'status': 'not_ready',
                'message': str(e),
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )


@api_view(['GET'])
def metrics(request):
    """
    Prometheus-compatible metrics endpoint.
    
    Returns application metrics in text format.
    Compatible with standard monitoring tools.
    """
    from django.db import connections
    from django.contrib.auth.models import User
    from listings.models import Property, Booking

    try:
        # Application metrics
        metrics_lines = [
            '# HELP airbnb_users_total Total number of users',
            f'# TYPE airbnb_users_total gauge',
            f'airbnb_users_total {User.objects.count()}',
            '',
            '# HELP airbnb_properties_total Total number of properties',
            f'# TYPE airbnb_properties_total gauge',
            f'airbnb_properties_total {Property.objects.count()}',
            '',
            '# HELP airbnb_bookings_total Total number of bookings',
            f'# TYPE airbnb_bookings_total gauge',
            f'airbnb_bookings_total {Booking.objects.count()}',
            '',
            '# HELP airbnb_active_bookings_total Active bookings',
            f'# TYPE airbnb_active_bookings_total gauge',
            f'airbnb_active_bookings_total {Booking.objects.filter(reservation_state__in=["approved", "completed"]).count()}',
            '',
        ]

        # Database connection pool stats
        db_stats = connections['default'].get_autocommit()
        metrics_lines.extend([
            '# HELP django_database_connected Database connection status',
            '# TYPE django_database_connected gauge',
            f'django_database_connected {1 if db_stats is not None else 0}',
            '',
        ])

        metrics_text = '\n'.join(metrics_lines)
        return Response(metrics_text, content_type='text/plain', status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f'Metrics endpoint error: {e}')
        return Response(
            f'# Error generating metrics: {str(e)}',
            content_type='text/plain',
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
