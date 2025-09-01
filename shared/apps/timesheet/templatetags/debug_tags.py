"""
Unified Template Debugging System for Shared Timesheet App

Automatically detects deployment mode:
- FamilyHub Integrated Mode: Purple banners
- Standalone Mode: Orange banners

Single source of truth for template debugging across both platforms.
"""

from django import template
from django.conf import settings
import datetime
import os

register = template.Library()

def get_deployment_mode():
    """Detect if we're running in standalone or integrated mode."""
    # Check if we're in standalone mode
    if hasattr(settings, 'IS_STANDALONE') and settings.IS_STANDALONE:
        return {
            'mode': 'STANDALONE',
            'name': 'Timesheet (Standalone)',
            'color': '#ff6b35',  # Orange for standalone
            'port': '8001',
            'banner_class': 'standalone'
        }
    else:
        return {
            'mode': 'INTEGRATED',
            'name': 'Timesheet (FamilyHub)',
            'color': '#764ba2',  # Purple for integrated
            'port': '8000',
            'banner_class': 'integrated'
        }

# Get current deployment configuration
DEPLOYMENT = get_deployment_mode()
APP_NAME = DEPLOYMENT['name']
APP_COLOR = DEPLOYMENT['color']
APP_ICON = 'fas fa-clock'
APP_PORT = DEPLOYMENT['port']
APP_MODE = DEPLOYMENT['mode']

@register.inclusion_tag('partials/debug_widget.html')
def debug_widget():
    """
    Render debug widget with timesheet app information
    Shows in purple for integrated mode vs orange for standalone
    """
    if not settings.DEBUG:
        return {}
    
    # Get current template context
    current_time = datetime.datetime.now()
    
    debug_info = {
        'app_name': APP_NAME,
        'app_color': APP_COLOR,
        'app_icon': APP_ICON,
        'app_port': APP_PORT,
        'app_mode': APP_MODE,
        'current_time': current_time,
        'debug_enabled': settings.DEBUG,
        'template_location': 'shared/apps/timesheet/templates/',
        'debug_type': 'SHARED_INTEGRATED'
    }
    
    return debug_info

@register.simple_tag
def get_app_info():
    """
    Get app deployment information for templates
    """
    deployment = get_deployment_mode()
    return {
        'name': deployment['name'],
        'color': deployment['color'],
        'icon': APP_ICON,
        'port': deployment['port'],
        'mode': deployment['mode']
    }

@register.simple_tag
def template_info(template_name):
    """
    Provide template information for debugging
    """
    if not settings.DEBUG:
        return ""
    
    deployment = get_deployment_mode()
    
    return {
        'name': template_name,
        'path': f'shared/apps/timesheet/templates/{template_name}',
        'mode': deployment['mode'],
        'source': 'shared'
    }

@register.inclusion_tag('partials/debug_widget.html', takes_context=True)
def show_debug_widget(context):
    """
    Show debug widget with current context
    """
    if not settings.DEBUG:
        return {}
    
    deployment = get_deployment_mode()
    current_time = datetime.datetime.now()
    
    return {
        'app_info': {
            'name': deployment['name'],
            'color': deployment['color'],
            'icon': APP_ICON,
            'port': deployment['port'],
            'mode': deployment['mode']
        },
        'template_info': {
            'name': context.get('template_name', 'Unknown'),
            'path': 'shared/apps/timesheet/templates/',
            'source': 'shared'
        },
        'current_time': current_time,
        'debug': True
    }

@register.simple_tag
def debug_context():
    """
    Return debug context information
    """
    if not settings.DEBUG:
        return ""
    
    return f"DEBUG: {APP_NAME} - {APP_MODE} Mode - Port {APP_PORT}"

@register.filter
def debug_highlight(value):
    """
    Add debug highlighting to template values
    """
    if not settings.DEBUG:
        return value
    
    return f'<span style="background-color: rgba(118, 75, 162, 0.2); padding: 2px 4px; border-radius: 3px;">{value}</span>'
