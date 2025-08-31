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
    """
    return {
        'familyhub_apps': apps_registry.get_active_apps(),
        'familyhub_debug': settings.DEBUG,
        'familyhub_version': getattr(settings, 'APP_VERSION', '1.0.0'),
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
