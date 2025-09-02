"""
FamilyHub Context Processors

Provides common context data to all templates including debug information.
"""

import os
import sys
from django.conf import settings
from django.db import connection
from django.apps import apps
from .app_registry import apps_registry


def familyhub_context(request):
    """
    Add common FamilyHub context to all templates.
    
    This context processor provides:
    - App registry data for navigation
    - Common settings for templates
    - User-specific data
    - Integration mode detection
    """
    # Detect if we're in integrated mode (running within FamilyHub)
    # vs standalone mode (running as individual app)
    integrated_mode = 'home' in settings.INSTALLED_APPS
    
    return {
        'familyhub_apps': apps_registry.get_active_apps(),
        'familyhub_debug': settings.DEBUG,
        'familyhub_version': getattr(settings, 'APP_VERSION', '1.0.0'),
        'integrated_mode': integrated_mode,
    }


def debug_info(request):
    """
    Context processor that adds debug information to all templates
    Only active when DEBUG=True
    """
    if not getattr(settings, 'DEBUG', False):
        return {}
    
    try:
        # Database Information
        db_config = connection.settings_dict
        db_info = {
            'engine': connection.vendor,
            'name': db_config.get('NAME', 'Unknown'),
            'host': db_config.get('HOST', 'localhost'),
            'port': db_config.get('PORT', 'N/A'),
            'user': db_config.get('USER', 'N/A'),
        }
        
        # Environment Information
        env_info = {
            'django_settings': os.environ.get('DJANGO_SETTINGS_MODULE', 'Not Set'),
            'debug_mode': getattr(settings, 'DEBUG', False),
            'environment': 'Docker' if os.path.exists('/.dockerenv') else 'Local',
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            'is_standalone': getattr(settings, 'IS_STANDALONE', 'Unknown'),
        }
        
        # App Information
        installed_apps = getattr(settings, 'INSTALLED_APPS', [])
        app_info = {
            'total_apps': len(installed_apps),
            'timesheet_integrated': 'timesheet_app' in installed_apps,
            'family_apps': [app for app in installed_apps if any(x in app.lower() for x in ['timesheet', 'daycare', 'employment', 'payments', 'credit', 'budget'])],
        }
        
        # System Information
        system_info = {
            'base_dir': str(getattr(settings, 'BASE_DIR', 'Unknown')),
            'static_url': getattr(settings, 'STATIC_URL', '/static/'),
            'media_url': getattr(settings, 'MEDIA_URL', '/media/'),
            'allowed_hosts': getattr(settings, 'ALLOWED_HOSTS', []),
        }
        
        return {
            'debug_widget': {
                'database': db_info,
                'environment': env_info,
                'apps': app_info,
                'system': system_info,
                'status': 'healthy',
            }
        }
        
    except Exception as e:
        return {
            'debug_widget': {
                'status': 'error',
                'error': str(e),
                'database': {'engine': 'Error loading'},
                'environment': {'django_settings': 'Error loading'},
                'apps': {'total_apps': 0},
                'system': {'base_dir': 'Error loading'},
            }
        }


def app_info(request):
    """
    Provide app information to all templates.
    This provides the same interface as the shared context processor.
    """
    return {
        'app_info': {
            'name': 'FamilyHub',
            'mode': 'Integrated',
            'color': 'purple',
            'url': '/',
            'deployment_mode': {
                'mode': 'INTEGRATED',
                'name': 'FamilyHub (Integrated)',
                'color': '#7c3aed',  # Purple for integrated
                'port': '8000',
                'banner_class': 'integrated'
            }
        }
    }


def navigation_context(request):
    """
    Provide navigation context to all templates.
    Determines current app and provides navigation data.
    """
    # Determine current app from URL
    current_app = 'home'  # Default
    path = request.path
    
    if path.startswith('/timesheet/'):
        current_app = 'timesheet'
    elif path.startswith('/budget/'):
        current_app = 'budget'
    elif path.startswith('/daycare/'):
        current_app = 'daycare'
    
    # Define available apps with navigation data
    available_apps = [
        {
            'name': 'Dashboard',
            'slug': 'home',
            'url': '/',
            'icon': 'bi-speedometer2',
            'color': 'primary',
            'available': True,
            'current': current_app == 'home'
        },
        {
            'name': 'Timesheet',
            'slug': 'timesheet',
            'url': '/timesheet/',
            'icon': 'bi-clock',
            'color': 'primary',
            'available': 'timesheet_app' in getattr(settings, 'INSTALLED_APPS', []),
            'current': current_app == 'timesheet',
            'sub_nav': [
                {'name': 'Dashboard', 'url': 'timesheet:dashboard', 'icon': 'bi-speedometer2'},
                {'name': 'Daily Entry', 'url': 'timesheet:daily_entry', 'icon': 'bi-plus-circle'},
                {'name': 'Weekly Summary', 'url': 'timesheet:weekly_summary', 'icon': 'bi-calendar-week'},
                {'name': 'Jobs', 'url': 'timesheet:job_list', 'icon': 'bi-briefcase'},
            ] if current_app == 'timesheet' else []
        },
        {
            'name': 'Budget',
            'slug': 'budget',
            'url': '/budget/',
            'icon': 'bi-calculator',
            'color': 'success',
            'available': False,  # Coming soon
            'current': current_app == 'budget'
        },
        {
            'name': 'Daycare',
            'slug': 'daycare',
            'url': '/daycare/',
            'icon': 'bi-receipt',
            'color': 'info',
            'available': False,  # Coming soon
            'current': current_app == 'daycare'
        }
    ]
    
    return {
        'current_app': current_app,
        'available_apps': available_apps,
        'current_app_data': next((app for app in available_apps if app['current']), available_apps[0])
    }
