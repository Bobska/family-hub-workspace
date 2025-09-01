#!/usr/bin/env python3
"""
Check app registry status and URL patterns
"""
import sys
import os
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyHub.settings.development')

import django
django.setup()

from FamilyHub.app_registry import app_registry

print('Available apps:')
for app in app_registry.known_apps:
    status = app_registry.get_app_status(app)
    print(f'  {app}: available={status["available"]}, urls_available={status["urls_available"]}')
    print(f'    integrated_path: {status["integrated_path"]}')
    print(f'    standalone_path: {status["standalone_path"]}')

print('\nURL patterns:')
for pattern in app_registry.get_app_urls():
    print(f'  {pattern}')

print('\nInstalled apps containing timesheet:')
from django.conf import settings
for app in settings.INSTALLED_APPS:
    if 'timesheet' in app:
        print(f'  {app}')
