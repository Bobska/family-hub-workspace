#!/usr/bin/env python
"""Debug timesheet template rendering"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyHub.settings.development')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

client = Client()
try:
    user = User.objects.get(username='testuser')
except:
    user = User.objects.create_user('testuser', 'test@test.com', 'testpass123')

client.login(username='testuser', password='testpass123')

response = client.get('/timesheet/')
content = response.content.decode()

print('=== TIMESHEET PAGE CONTENT ANALYSIS ===')
print('Status:', response.status_code)
print('Contains FamilyHub brand:', 'FamilyHub' in content)
print('Contains primary navbar:', 'navbar' in content and 'FamilyHub' in content)
print('Contains secondary nav:', 'secondary-nav' in content)
print('Contains breadcrumb:', 'breadcrumb' in content)

# Check if we can find key elements
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'navbar' in line.lower() and i < 50:  # Top of page
        print(f'Navbar found at line {i}: {line.strip()[:100]}...')
        break

# Check template hierarchy
if 'extends "base.html"' in content[:1000]:
    print('✅ Template extends base.html')
elif 'extends "timesheet/base_unified.html"' in content[:1000]:
    print('✅ Template extends base_unified.html')
else:
    print('❌ Template inheritance unclear')

print('\n=== First 20 lines of response ===')
for i, line in enumerate(lines[:20]):
    print(f'{i+1:2d}: {line}')
