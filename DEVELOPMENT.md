# FamilyHub Development Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Django 5.1+
- Git
- PowerShell (Windows) or Bash (Linux/Mac)

### Development Setup
```bash
# Clone repository
git clone <repository-url>
cd family-hub-workspace

# Setup FamilyHub (Integrated Mode)
cd FamilyHub
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate      # Linux/Mac
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver    # Port 8000

# Setup Standalone Apps (Development)
cd ../standalone-apps/timesheet
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8001  # Port 8001
```

## 🏗️ Architecture Overview

### Project Structure
```
family-hub-workspace/
├── FamilyHub/                    # Main integrated hub
│   ├── apps/                    # Symbolic links to standalone apps
│   ├── home/                    # Dashboard app
│   └── manage.py
├── standalone-apps/             # Independent app development
│   ├── timesheet/
│   ├── daycare_invoice/
│   └── ...
└── shared/                      # Shared components
```

### Two-Mode Development
- **Integrated Mode**: Apps run within FamilyHub (port 8000)
- **Standalone Mode**: Apps run independently (port 8001+)

## 🛠️ Development Workflow

### Using Makefile (Recommended)
```bash
# Start FamilyHub integrated mode
make local-start

# Start timesheet standalone mode  
make local-start-timesheet

# Run tests
make test

# Check code quality
make check
```

### Manual Commands
```bash
# FamilyHub Development
cd FamilyHub
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
python manage.py test

# Standalone App Development
cd standalone-apps/timesheet
python manage.py runserver 8001
python manage.py makemigrations timesheet_app
python manage.py migrate
```

## 📝 Code Standards

### Template Architecture
- **Integrated**: Use `dashboard_integrated.html` (extends "base.html")
- **Standalone**: Use `dashboard_standalone.html` (extends 'timesheet/base.html')
- **Shared Content**: Use `dashboard_content.html` for common elements

### Model Standards
```python
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        abstract = True
```

### View Standards
```python
@login_required
def view_name(request):
    # Choose template based on integration mode
    integrated_mode = 'apps.timesheet_app' in settings.INSTALLED_APPS
    template_name = 'app/template_integrated.html' if integrated_mode else 'app/template_standalone.html'
    return render(request, template_name, context)
```

## 🧪 Testing

### Running Tests
```bash
# All tests
python manage.py test

# Specific app tests
python manage.py test timesheet_app

# Integration tests
python manage.py test tests.test_integration
```

### Test Structure
```
FamilyHub/
├── tests/                       # Integration tests
│   ├── test_integration.py
│   └── test_context_processors.py
└── apps/
    └── timesheet_app/
        └── tests.py            # App-specific tests
```

## 🔍 Debugging

### Debug Mode
Set `DEBUG = True` in settings for development features:
- Detailed error pages
- Debug toolbar (if installed)
- Template debugging

### Template Debugging
```django
<!-- Only in development -->
{% if debug %}
    {% load debug_tags %}
    {% show_template_path %}
{% endif %}
```

### Common Issues
1. **Port Conflicts**: Use different ports for each mode
2. **Template Not Found**: Check template selection logic in views
3. **Import Errors**: Verify symbolic links are correct

## 📦 Deployment

### Production Setup
```bash
# Environment variables
export DEBUG=False
export SECRET_KEY=your-secret-key
export DATABASE_URL=your-database-url

# Collect static files
python manage.py collectstatic

# Run with WSGI server
gunicorn FamilyHub.wsgi:application
```

### Docker Deployment
```bash
# Build and run
docker-compose up --build

# Production
docker-compose -f docker-compose.prod.yml up
```

## 🤝 Contributing

### Branch Strategy
- `main`: Production-ready code
- `feature/app-name`: App-specific features
- `feature/app-name/feature-name`: Specific feature development

### Commit Standards
```
feat(scope): description
fix(scope): description  
docs(scope): description
test(scope): description
```

### Before Committing
1. Run tests: `python manage.py test`
2. Check code quality: `python manage.py check`
3. Verify both modes work
4. Update documentation if needed

## 📚 Additional Resources

- [Architecture Instructions](.github/instructions/Architecture.instructions.md)
- [Branching Strategy](.github/instructions/Git-Branching-Strategy.instructions.md)
- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)

---

**Need Help?** Check the architecture documentation or create an issue for support.
