"""
Debug Views for Standalone Timesheet App

Test views for showcasing template debugging functionality in standalone mode.
Only available in DEBUG mode.
"""

from django.shortcuts import render
from django.conf import settings
from django.http import Http404


def template_debug_showcase(request):
    """
    Debug view to showcase template debugging features for standalone timesheet app.
    Only available when DEBUG=True.
    """
    if not settings.DEBUG:
        raise Http404("Page not available in production mode")
    
    context = {
        'title': 'Standalone Timesheet Debug Showcase',
        'debug_mode': settings.DEBUG,
        'app_mode': 'Standalone',
        'sample_data': {
            'string_value': 'Standalone Timesheet App',
            'number_value': 42,
            'list_value': ['time_entry_1', 'time_entry_2', 'time_entry_3'],
            'dict_value': {'job_name': 'Example Job', 'hours': '8.5'},
        },
        'template_info': {
            'current_template': 'timesheet/debug_showcase.html',
            'base_template': 'timesheet/base.html',
            'app_name': 'timesheet_app',
            'mode': 'standalone',
        },
        'user_info': {
            'authenticated': request.user.is_authenticated,
            'username': request.user.username if request.user.is_authenticated else 'Anonymous',
        },
        'standalone_features': [
            'Independent Django project',
            'Own database and settings',
            'Can run on separate port',
            'Complete authentication system',
            'Dedicated template debugging',
        ]
    }
    
    return render(request, 'timesheet/debug_showcase.html', context)
