---
applyTo: '**'
---
Complete Copilot Instructions:
FamilyHub Project - Copilot Development Instructions

## Project Overview
FamilyHub is a Django-based family management platform consisting of multiple integrated applications. The project uses a hub-and-spoke architecture where standalone apps can run independently or be integrated into the main FamilyHub dashboard.

## Technology Stack
- **Backend**: Django 5.1+ (Python 3.10+)
- **Frontend**: Bootstrap 5, HTML5, CSS3, Vanilla JavaScript
- **Database**: SQLite (dev), PostgreSQL (prod-ready)
- **Location**: Auckland, New Zealand (Pacific/Auckland timezone)
- **Development Environment**: Windows with Git Bash

## Project Structure
family-hub-workspace/
├── FamilyHub/                    # Main hub project
│   ├── FamilyHub/               # Project settings
│   │   ├── settings.py          # Main configuration
│   │   ├── urls.py              # Root URL configuration
│   │   └── wsgi.py
│   ├── home/                    # Dashboard app
│   │   ├── templates/home/      # App templates
│   │   │   └── dashboard.html   # Main dashboard
│   │   ├── static/home/         # App static files
│   │   ├── management/commands/ # Custom commands
│   │   ├── views.py             # Dashboard views
│   │   ├── urls.py              # App URLs
│   │   └── apps.py              # App config
│   ├── apps/                    # Integrated apps directory
│   ├── static/                  # Global static files
│   ├── templates/               # Global templates
│   ├── media/                   # User uploads
│   └── manage.py
├── standalone-apps/             # Individual app projects
│   ├── timesheet/
│   ├── daycare_invoice/
│   ├── employment_history/
│   ├── upcoming_payments/
│   ├── credit_card_mgmt/
│   └── household_budget/
└── shared/                      # Shared components
├── models/
├── utils/
└── templates/

markdown## ⚠️ CRITICAL: Server & Command Execution Locations

### ALWAYS RUN DJANGO COMMANDS FROM THE CORRECT DIRECTORY:

# ✅ CORRECT - Run server from FamilyHub directory:
cd ~/OneDrive/Development/myprojects/family-hub-workspace/FamilyHub
source venv/Scripts/activate  # Windows Git Bash
python manage.py runserver

# ❌ WRONG - Never run from workspace root:
# DO NOT run from: family-hub-workspace/
# DO NOT run from: standalone-apps/
Directory Navigation for Different Operations:
bash# FOR MAIN FAMILYHUB SERVER:
cd ~/OneDrive/Development/myprojects/family-hub-workspace/FamilyHub
source venv/Scripts/activate
python manage.py runserver  # Runs on port 8000

# FOR STANDALONE APP DEVELOPMENT (example: timesheet):
cd ~/OneDrive/Development/myprojects/family-hub-workspace/standalone-apps/timesheet
source venv/Scripts/activate
python manage.py runserver 8001  # Use different port

# FOR SHARED COMPONENTS:
cd ~/OneDrive/Development/myprojects/family-hub-workspace/shared
# No server to run here - just shared code
Virtual Environment Activation by Location:
bash# Windows Git Bash (current environment):
source venv/Scripts/activate

# Windows Command Prompt:
venv\Scripts\activate.bat

# Windows PowerShell:
venv\Scripts\Activate.ps1

# Linux/Mac:
source venv/bin/activate
Common Path Issues & Solutions:
bash# Issue: "ModuleNotFoundError: No module named 'FamilyHub'"
# Solution: You're in the wrong directory. Navigate to:
cd ~/OneDrive/Development/myprojects/family-hub-workspace/FamilyHub

# Issue: "No such file or directory: manage.py"
# Solution: You're not in the Django project directory:
cd FamilyHub  # from workspace root

# Issue: "django.core.exceptions.ImproperlyConfigured"
# Solution: Activate virtual environment first:
source venv/Scripts/activate
File Path References in Code:
When writing Django code, use these path patterns:
python# In settings.py or any Django file:
from pathlib import Path

# Correct base directory reference:
BASE_DIR = Path(__file__).resolve().parent.parent  # Points to FamilyHub/

# For templates:
TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']

# For static files:
STATICFILES_DIRS = [BASE_DIR / 'static']

# For media files:
MEDIA_ROOT = BASE_DIR / 'media'
Quick Command Reference by Location:
TaskDirectoryCommandRun FamilyHubFamilyHub/python manage.py runserverMake migrationsFamilyHub/python manage.py makemigrationsRun migrationsFamilyHub/python manage.py migrateCreate superuserFamilyHub/python manage.py createsuperuserCheck healthFamilyHub/python manage.py check_healthRun testsFamilyHub/python manage.py testCollect staticFamilyHub/python manage.py collectstatic
Project Structure Reminder:
family-hub-workspace/           # ← NOT HERE for Django commands
├── FamilyHub/                 # ← ✅ RUN DJANGO COMMANDS HERE
│   ├── manage.py             # ← This file must be in current directory
│   ├── venv/                 # ← Virtual environment for this project
│   ├── FamilyHub/           # ← Settings directory
│   ├── home/                # ← Dashboard app
│   └── apps/                # ← Integrated apps
├── standalone-apps/          # ← Each has its own manage.py
│   ├── timesheet/           # ← Run separately on port 8001
│   └── ...
└── shared/                  # ← No manage.py here

## Coding Standards & Patterns

### Django App Structure
When creating new Django apps, follow this pattern:
```python
# apps.py
from django.apps import AppConfig

class AppNameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_name'
    verbose_name = 'Readable App Name'
Model Patterns
pythonfrom django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class BaseModel(models.Model):
    """Abstract base model with common fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='%(class)s_created'
    )
    
    class Meta:
        abstract = True

class AppModel(BaseModel):
    """Example model inheriting from BaseModel"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Model Name'
        verbose_name_plural = 'Model Names'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
View Patterns
pythonfrom django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import datetime

@login_required
def app_dashboard(request):
    """Dashboard view with context data"""
    context = {
        'title': 'Dashboard',
        'user': request.user,
        'today': datetime.now(),
        'stats': {
            'total': Model.objects.count(),
            'active': Model.objects.filter(is_active=True).count(),
        }
    }
    return render(request, 'app_name/dashboard.html', context)

@login_required
def model_list(request):
    """List view with pagination"""
    queryset = Model.objects.filter(created_by=request.user)
    paginator = Paginator(queryset, 10)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    
    return render(request, 'app_name/model_list.html', {
        'items': items,
        'title': 'My Items'
    })
Template Patterns
django<!-- templates/app_name/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}FamilyHub{% endblock %}</title>
    
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% include 'partials/navbar.html' %}
    
    <main class="container my-4">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        {% endif %}
        
        {% block content %}{% endblock %}
    </main>
    
    <!-- Bootstrap JS Bundle -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
URL Patterns
python# app_name/urls.py
from django.urls import path
from . import views

app_name = 'app_name'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('items/', views.item_list, name='item_list'),
    path('items/add/', views.item_create, name='item_create'),
    path('items/<int:pk>/', views.item_detail, name='item_detail'),
    path('items/<int:pk>/edit/', views.item_update, name='item_update'),
    path('items/<int:pk>/delete/', views.item_delete, name='item_delete'),
]
Form Patterns
pythonfrom django import forms
from .models import Model

class ModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Model.objects.filter(name=name).exists():
            raise forms.ValidationError('This name already exists.')
        return name
UI/UX Standards
Color Scheme
css/* FamilyHub Brand Colors */
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --primary: #667eea;
    --secondary: #764ba2;
    --success: #10b981;
    --info: #06b6d4;
    --warning: #f59e0b;
    --danger: #ef4444;
}
Card Components
html<!-- Standard app card -->
<div class="card app-card h-100 shadow">
    <div class="card-body text-center">
        <div class="app-icon">{{ app.icon }}</div>
        <h5 class="card-title">{{ app.name }}</h5>
        <p class="card-text text-muted">{{ app.description }}</p>
        <a href="{{ app.url }}" class="btn btn-{{ app.color }} w-100">
            Open {{ app.name }}
        </a>
    </div>
</div>
Status Indicators
python# Status choices for models
STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]

# Template badge colors
STATUS_COLORS = {
    'pending': 'warning',
    'in_progress': 'info',
    'completed': 'success',
    'cancelled': 'danger',
}
App Integration Guidelines
When Creating New Apps:

Start in standalone-apps/ for independent development
Create full Django project structure
Test independently on different port (8001, 8002, etc.)
Once stable, integrate into FamilyHub

Integration Steps:

Copy app to FamilyHub/apps/
Add to INSTALLED_APPS in settings
Include app URLs in main urls.py
Add app card to dashboard view
Update navigation menus
Test integrated functionality

Database Guidelines
Migrations:

Always create migrations after model changes
Use descriptive migration names
Test migrations on clean database
Never edit migration files directly

Model Relationships:
python# Use related_name for clarity
class Invoice(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='invoices'
    )
    
# Use through models for complex relationships
class Family(models.Model):
    members = models.ManyToManyField(
        User,
        through='FamilyMembership',
        related_name='families'
    )
Security Best Practices
Always:

Use @login_required decorator for protected views
Validate user permissions in views
Use Django's CSRF protection
Sanitize user inputs
Use parameterized queries (Django ORM)
Store sensitive data in environment variables

Never:

Hardcode secrets in code
Trust user input without validation
Use raw SQL without parameterization
Expose internal IDs in URLs when possible
Store passwords in plain text

Testing Guidelines
Test Structure:
pythonfrom django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Model

User = get_user_model()

class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = Client()
        
    def test_model_creation(self):
        obj = Model.objects.create(
            name='Test',
            created_by=self.user
        )
        self.assertEqual(str(obj), 'Test')
        
    def test_view_requires_login(self):
        response = self.client.get('/app/dashboard/')
        self.assertEqual(response.status_code, 302)
Error Handling
View Error Handling:
pythonfrom django.shortcuts import render
from django.http import Http404

def safe_view(request, pk):
    try:
        obj = Model.objects.get(pk=pk, user=request.user)
    except Model.DoesNotExist:
        raise Http404("Item not found")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('app_name:dashboard')
    
    return render(request, 'template.html', {'object': obj})
Performance Considerations
Query Optimization:
python# Use select_related for ForeignKeys
items = Model.objects.select_related('user', 'category')

# Use prefetch_related for ManyToMany
items = Model.objects.prefetch_related('tags', 'comments')

# Use only() for specific fields
items = Model.objects.only('id', 'name', 'created_at')

# Use pagination for large datasets
from django.core.paginator import Paginator
paginator = Paginator(queryset, 25)
Deployment Readiness
Environment-specific settings:
python# settings.py
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])

if DEBUG:
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}
else:
    DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql'}}
Development Workflow

Feature Development:

Create feature branch
Develop in standalone app
Test thoroughly
Integrate into FamilyHub
Create pull request


Bug Fixes:

Identify in issue tracker
Create fix branch
Write test to reproduce
Implement fix
Verify test passes


Documentation:

Update docstrings
Add inline comments for complex logic
Update README if needed
Document API changes



Common Commands
bash# Development
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py check_health

# Testing
python manage.py test
python manage.py test app_name
python manage.py test --verbosity=2

# Database
python manage.py dbshell
python manage.py flush
python manage.py dumpdata > backup.json
python manage.py loaddata backup.json
Important Notes

## ⚠️ Most Common Copilot Mistakes to Avoid:

1. **NEVER suggest running server from workspace root** - Always cd to FamilyHub/
2. **NEVER forget virtual environment activation** - Must activate before any Python/Django commands
3. **NEVER use `python3`** - Use `python` in this Windows Git Bash environment
4. **NEVER run on port 8000 for standalone apps** - Use 8001, 8002, etc.
5. **NEVER mix standalone app code with FamilyHub** - Keep them separate until integration

Always work in virtual environment
Follow PEP 8 style guide
Write descriptive commit messages
Document complex business logic
Keep apps modular and reusable
Prioritize user experience
Ensure mobile responsiveness
Maintain backwards compatibility

Contact & Support
Project: FamilyHub
Location: Auckland, New Zealand
Timezone: Pacific/Auckland
Python: 3.10+
Django: 5.1+
Bootstrap: 5.3.0