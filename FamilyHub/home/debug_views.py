"""
Debug Template Views

Test views for showcasing template debugging functionality.
Only available in DEBUG mode.
"""

from django.shortcuts import render
from django.conf import settings
from django.http import Http404


def template_debug_showcase(request):
    """
    Debug view to showcase template debugging features.
    Only available when DEBUG=True.
    """
    if not settings.DEBUG:
        raise Http404("Page not available in production mode")
    
    context = {
        'title': 'Template Debug Showcase',
        'debug_mode': settings.DEBUG,
        'sample_data': {
            'string_value': 'Hello, World!',
            'number_value': 42,
            'list_value': ['item1', 'item2', 'item3'],
            'dict_value': {'key1': 'value1', 'key2': 'value2'},
        },
        'template_info': {
            'current_template': 'debug/template_showcase.html',
            'base_template': 'base.html',
            'app_name': 'home',
        },
        'user_info': {
            'authenticated': request.user.is_authenticated,
            'username': request.user.username if request.user.is_authenticated else 'Anonymous',
        }
    }
    
    return render(request, 'debug/template_showcase.html', context)
