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

from FamilyHub.app_registry import app_registry

logger = logging.getLogger(__name__)


def home_dashboard(request):
    """
    Main dashboard view showing all apps overview.
    Uses dynamic app registry to show current app status.
    """
    
    # Get dynamic app data
    apps_data = app_registry.get_dashboard_data()
    
    context = {
        'apps': apps_data,
        'user': request.user,
        'today': timezone.now(),
    }
    
    return render(request, 'home/dashboard.html', context)


def debug_dashboard(request):
    """Visual debug dashboard showing template and app information"""
    
    # Get app statuses for debugging
    app_statuses = app_registry.get_all_app_statuses()
    apps_data = app_registry.get_dashboard_data()
    
    # Get additional debug information
    template_dirs = []
    if hasattr(settings, 'TEMPLATES') and settings.TEMPLATES:
        template_dirs = settings.TEMPLATES[0].get('DIRS', [])
    
    context = {
        'apps': apps_data,
        'app_statuses': app_statuses,
        'user': request.user,
        'today': timezone.now(),
        'settings_info': {
            'DEBUG': settings.DEBUG,
            'INSTALLED_APPS': settings.INSTALLED_APPS,
            'TEMPLATE_DIRS': template_dirs,
            'DATABASE_ENGINE': settings.DATABASES['default']['ENGINE'],
        },
        'registry_stats': {
            'total_apps': len(app_registry.known_apps),
            'available_apps': len(app_registry.get_available_apps()),
            'integrated_apps': len([a for a in app_registry.get_all_app_statuses().values() if a['status'] == 'integrated']),
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
            'total_apps': len(app_registry.known_apps),
            'available_apps': len(app_registry.get_available_apps()),
        }
    }
    
    status_code = 200 if overall_healthy else 503
    response = JsonResponse(health_data, status=status_code)
    response['Cache-Control'] = 'no-store'
    return response
