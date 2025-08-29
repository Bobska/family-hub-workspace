from django.http import JsonResponse
from django.db import connection
from django.conf import settings
import redis
import logging

logger = logging.getLogger(__name__)

def health_check(request):
    """
    Health check endpoint for Docker and monitoring systems.
    Returns JSON with status of database, cache, and overall system health.
    """
    health_status = {
        'status': 'healthy',
        'timestamp': None,
        'services': {
            'database': 'unknown',
            'cache': 'unknown',
            'application': 'healthy'
        },
        'version': '1.0.0'
    }
    
    from django.utils import timezone
    health_status['timestamp'] = timezone.now().isoformat()
    
    # Check database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        health_status['services']['database'] = 'healthy'
        logger.info("Database health check: PASSED")
    except Exception as e:
        health_status['services']['database'] = f'unhealthy: {str(e)}'
        health_status['status'] = 'unhealthy'
        logger.error(f"Database health check: FAILED - {str(e)}")
    
    # Check Redis cache (if configured)
    try:
        if hasattr(settings, 'CACHES') and 'django_redis' in str(settings.CACHES.get('default', {})):
            r = redis.Redis.from_url(settings.CACHES['default']['LOCATION'])
            r.ping()
            health_status['services']['cache'] = 'healthy'
            logger.info("Cache health check: PASSED")
        else:
            health_status['services']['cache'] = 'not_configured'
    except Exception as e:
        health_status['services']['cache'] = f'unhealthy: {str(e)}'
        health_status['status'] = 'degraded'  # Cache failure doesn't make the whole system unhealthy
        logger.warning(f"Cache health check: FAILED - {str(e)}")
    
    # Determine HTTP status code
    status_code = 200
    if health_status['status'] == 'unhealthy':
        status_code = 503
    elif health_status['status'] == 'degraded':
        status_code = 200  # Still functional, just degraded
    
    return JsonResponse(health_status, status=status_code)
