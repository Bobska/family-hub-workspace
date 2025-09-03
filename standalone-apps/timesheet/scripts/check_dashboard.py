import os
import django
from django.contrib.auth import get_user_model
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timesheet_project.settings')
django.setup()

User = get_user_model()
if not User.objects.filter(username='testuser').exists():
    User.objects.create_user('testuser', 'test@example.com', 'testpass')

c = Client()
logged = c.login(username='testuser', password='testpass')
print('login', logged)
resp = c.get('/')
print('status', resp.status_code)
content = resp.content
print('has_dashboard_marker:', b'Timesheet Dashboard' in content or b'Dashboard (Shared)' in content)
print(content.decode('utf-8')[:2000])
