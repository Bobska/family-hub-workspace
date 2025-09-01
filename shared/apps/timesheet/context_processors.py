"""
Context processors for shared timesheet app
Provides deployment information to all templates automatically
"""

import os
from django.conf import settings

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

def app_info(request):
    """
    Context processor to provide app deployment information to all templates
    """
    deployment = get_deployment_mode()
    
    return {
        'app_info': {
            'name': deployment['name'],
            'color': deployment['color'],
            'icon': 'fas fa-clock',
            'port': deployment['port'],
            'mode': deployment['mode']
        }
    }
