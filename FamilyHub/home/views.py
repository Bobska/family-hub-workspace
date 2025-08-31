from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page
import logging
import time

from .app_registry import apps_registry

logger = logging.getLogger(__name__)


def home_dashboard(request):
    """
    Main dashboard view showing all apps overview.
    App data is now provided by the familyhub_context processor.
    """
    
    context = {
        'user': request.user,
        'today': timezone.now(),
    }
    
    return render(request, 'home/dashboard.html', context)


def debug_dashboard(request):
    """Visual debug dashboard showing template and app information"""
    
    # Get additional debug information
    template_dirs = []
    if hasattr(settings, 'TEMPLATES') and settings.TEMPLATES:
        template_dirs = settings.TEMPLATES[0].get('DIRS', [])
    
    context = {
        'apps': apps_registry.to_dict_list(),
        'all_apps': apps_registry.get_all_apps(),
        'integrated_apps': apps_registry.get_integrated_apps(),
        'user': request.user,
        'today': timezone.now(),
        'settings_info': {
            'DEBUG': settings.DEBUG,
            'INSTALLED_APPS': settings.INSTALLED_APPS,
            'TEMPLATE_DIRS': template_dirs,
            'DATABASE_ENGINE': settings.DATABASES['default']['ENGINE'],
        },
        'registry_stats': {
            'total_apps': len(apps_registry.get_all_apps()),
            'active_apps': len(apps_registry.get_active_apps()),
            'integrated_apps': len(apps_registry.get_integrated_apps()),
        }
    }
    
    return render(request, 'home/debug_dashboard.html', context)


@require_http_methods(["GET"])
@cache_page(60)  # Cache for 1 minute
def health_check(request):
    """Health check endpoint for production monitoring"""
    start_time = time.monotonic()
    
    # Check database connection
    db_healthy = True
    db_duration = 0
    try:
        db_start = time.monotonic()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_duration = (time.monotonic() - db_start) * 1000  # Convert to ms
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_healthy = False
    
    # Check cache connection  
    cache_healthy = True
    cache_duration = 0
    try:
        cache_start = time.monotonic()
        cache.set('health_check', 'test', 1)
        cache_result = cache.get('health_check')
        cache_duration = (time.monotonic() - cache_start) * 1000  # Convert to ms
        cache_healthy = cache_result == 'test'
    except Exception as e:
        logger.error(f"Cache health check failed: {e}")
        cache_healthy = False
    
    # Overall status
    overall_healthy = db_healthy and cache_healthy
    total_duration = (time.monotonic() - start_time) * 1000
    
    health_data = {
        'status': 'healthy' if overall_healthy else 'unhealthy',
        'timestamp': timezone.now().isoformat(),
        'version': getattr(settings, 'APP_VERSION', '1.0.0'),
        'services': {
            'database': {
                'status': 'healthy' if db_healthy else 'unhealthy',
                'duration_ms': round(db_duration, 2)
            },
            'cache': {
                'status': 'healthy' if cache_healthy else 'unhealthy', 
                'duration_ms': round(cache_duration, 2)
            },
        },
        'total_duration_ms': round(total_duration, 2),
        'app_registry': {
            'total_apps': len(apps_registry.get_all_apps()),
            'active_apps': len(apps_registry.get_active_apps()),
        }
    }
    
    status_code = 200 if overall_healthy else 503
    response = JsonResponse(health_data, status=status_code)
    response['Cache-Control'] = 'no-store'
    return response
