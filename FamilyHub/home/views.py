from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def home_dashboard(request):
    """Main dashboard view showing all apps overview"""
    
    # Prepare app cards with their information
    apps = [
        {
            'name': 'Timesheet',
            'icon': '⏰',
            'description': 'Track your work hours and projects',
            'url': '/timesheet/',
            'color': 'primary'
        },
        {
            'name': 'Household Budget',
            'icon': '💰',
            'description': 'Manage family finances and budgets',
            'url': '/budget/',
            'color': 'success'
        },
        {
            'name': 'Daycare Invoices',
            'icon': '🧒',
            'description': 'Track daycare bills and payments',
            'url': '/daycare/',
            'color': 'info'
        },
        {
            'name': 'Employment History',
            'icon': '💼',
            'description': 'Your career journey and records',
            'url': '/employment/',
            'color': 'warning'
        },
        {
            'name': 'Upcoming Payments',
            'icon': '📅',
            'description': 'Never miss a payment deadline',
            'url': '/payments/',
            'color': 'danger'
        },
        {
            'name': 'Credit Cards',
            'icon': '💳',
            'description': 'Manage credit cards and limits',
            'url': '/creditcards/',
            'color': 'secondary'
        },
    ]
    
    context = {
        'apps': apps,
        'user': request.user,
        'today': datetime.now(),
    }
    
    return render(request, 'home/dashboard.html', context)


def health_check(request):
    """Health check endpoint for production monitoring"""
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "unhealthy"
    
    # Check cache connection
    try:
        cache.set('health_check', 'test', 1)
        cache_result = cache.get('health_check')
        cache_status = "healthy" if cache_result == 'test' else "unhealthy"
    except Exception as e:
        logger.error(f"Cache health check failed: {e}")
        cache_status = "unhealthy"
    
    # Overall status
    overall_status = "healthy" if db_status == "healthy" and cache_status == "healthy" else "unhealthy"
    
    health_data = {
        'status': overall_status,
        'timestamp': datetime.now().isoformat(),
        'services': {
            'database': db_status,
            'cache': cache_status,
        },
        'version': '1.0.0'
    }
    
    status_code = 200 if overall_status == "healthy" else 503
    return JsonResponse(health_data, status=status_code)
