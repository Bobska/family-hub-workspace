"""
Debug Context Processor for Standalone Timesheet App
Provides debug information for the visual debug widget and integration context
"""

import os
import sys
from django.conf import settings
from django.db import connection
from django.apps import apps


def integration_context(request):
    """
    Provides integration context to all templates.
    
    This context processor automatically detects whether the app is running
    in standalone mode or integrated with FamilyHub and makes this information
    available to all templates.
    
    Returns:
        dict: Context variables for integration mode detection
    """
    # Detect integration mode based on settings
    integrated_mode = (
        hasattr(settings, 'IS_STANDALONE') and not settings.IS_STANDALONE
    ) or (
        'apps.timesheet_app' in settings.INSTALLED_APPS
    )
    
    return {
        'integrated_mode': integrated_mode,
        'standalone_mode': not integrated_mode,
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
            'is_standalone': getattr(settings, 'IS_STANDALONE', True),  # Default True for standalone
            'app_type': 'Standalone Timesheet',
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
                'environment': {'django_settings': 'Error loading', 'app_type': 'Standalone Timesheet'},
                'apps': {'total_apps': 0},
                'system': {'base_dir': 'Error loading'},
            }
        }


def deployment_context(request):
    """
    Context processor that provides deployment information for standalone mode
    """
    if not getattr(settings, 'DEBUG', False):
        return {}
    
    return {
        'deployment_info': {
            'mode': 'standalone',
            'port': 8001,
            'app_name': 'Timesheet Standalone',
            'theme': 'orange',
            'architecture': 'Independent Django App'
        }
    }


def app_info(request):
    """
    Context processor that provides app information for templates
    Local implementation for standalone mode - no shared imports
    """
    return {
        'app_info': {
            'name': 'Timesheet (Standalone)',
            'color': '#ff6b35',  # Orange for standalone
            'mode': 'STANDALONE',
            'port': '8001'
        }
    }
