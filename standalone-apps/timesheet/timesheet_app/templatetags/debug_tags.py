"""
Standalone Timesheet App Debug Template Tags
Orange-themed debug banners for standalone mode
"""

from django import template
from django.conf import settings
import os
import sys
from datetime import datetime

register = template.Library()

@register.inclusion_tag('timesheet/debug/debug_banner.html')
def debug_banner():
    """Display debug banner with orange theme for standalone mode"""
    
    if not settings.DEBUG:
        return {'show_debug': False}
    
    # Get template information
    context = {
        'show_debug': True,
        'mode': 'STANDALONE',
        'theme_color': 'warning',  # Orange theme for standalone
        'theme_bg': 'bg-warning',
        'theme_text': 'text-dark',
        'app_name': 'Timesheet (Standalone)',
        'port': '8001',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'debug_info': {
            'django_version': '5.2.5',
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}",
            'template_debug': settings.DEBUG,
            'project_root': settings.BASE_DIR,
            'architecture': 'Independent Standalone App'
        }
    }
    
    return context

@register.simple_tag
def debug_badge(label, value, color="warning"):
    """Generate a debug badge with orange theme"""
    if not settings.DEBUG:
        return ""
    
    return f'<span class="badge bg-{color} me-1">{label}: {value}</span>'

@register.simple_tag
def debug_info_panel():
    """Generate debug information panel for standalone mode"""
    if not settings.DEBUG:
        return ""
    
    info = {
        'Mode': 'Standalone Server',
        'Port': '8001',
        'Architecture': 'Independent App',
        'Theme': 'Orange/Warning'
    }
    
    badges = []
    for key, value in info.items():
        badges.append(f'<span class="badge bg-warning text-dark me-1">{key}: {value}</span>')
    
    return ' '.join(badges)
