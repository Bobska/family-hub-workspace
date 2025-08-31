"""
Template debugging system for shared timesheet app
Part of FamilyHub integrated mode
"""

from django import template
from django.conf import settings
import datetime
import os

register = template.Library()

# App Configuration for Shared Timesheet (Integrated Mode)
APP_NAME = 'Timesheet (Integrated)'
APP_COLOR = '#764ba2'  # Purple for integrated mode
APP_ICON = 'fas fa-clock'
APP_PORT = '8000'
APP_MODE = 'INTEGRATED'

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
