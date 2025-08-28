# 🏠 FamilyHub Timesheet App - Development Guide

## 📋 Overview
A Django-based timesheet tracking application for the FamilyHub family management platform. This standalone app can run independently or be integrated into the main FamilyHub dashboard.

## 🛠️ Technical Stack
- **Backend**: Django 5.2.5
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Database**: SQLite (development), PostgreSQL (production-ready)
- **Python**: 3.10+
- **Location**: Auckland, New Zealand (Pacific/Auckland timezone)

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Git
- Virtual environment activated

### Setup
```powershell
# Navigate to project
cd C:\Users\Dmitry\OneDrive\Development\myprojects\family-hub-workspace\standalone-apps\timesheet

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver 8001
```

Visit: http://127.0.0.1:8001/

## 🔄 Development Workflow

### ✅ Best Practices
1. **Always work on feature branches** - Never commit directly to main
2. **Test before committing** - Ensure all functionality works
3. **Use descriptive commit messages** - Follow conventional commit format
4. **Regular commits** - Small, focused commits are better
5. **Code review** - Use pull requests for all changes

### 🌿 Branch Management

#### Creating a New Feature
```powershell
# Option 1: Use the workflow script
.\dev-workflow.ps1 start

# Option 2: Manual process
git checkout main
git pull origin main
git checkout -b feature/your-feature-name
```

#### Working on Your Feature
```powershell
# Test your changes
.\dev-workflow.ps1 test

# Commit changes
.\dev-workflow.ps1 commit

# Push to remote
.\dev-workflow.ps1 push
```

#### Merging Back to Main
```powershell
# After code review approval
.\dev-workflow.ps1 merge
```

### 📝 Commit Message Convention
Follow conventional commits format:
```
type(scope): description

Examples:
feat: add time entry validation
fix: resolve template syntax error
docs: update installation instructions
style: format code with black
refactor: simplify time calculation logic
test: add unit tests for models
chore: update dependencies
```

## 🧪 Testing

### Manual Testing Checklist
- [ ] Dashboard loads without errors
- [ ] Can create/edit/delete jobs
- [ ] Can add time entries
- [ ] Time calculations are correct
- [ ] Weekly summary displays properly
- [ ] User authentication works
- [ ] All forms validate properly
- [ ] Mobile responsive design works

### Django Checks
```powershell
# Check for common issues
python manage.py check

# Check for migration issues
python manage.py makemigrations --dry-run

# Run tests
python manage.py test
```

## 📁 Project Structure
```
timesheet/
├── manage.py                   # Django management script
├── requirements.txt           # Python dependencies
├── dev-workflow.ps1          # Development workflow script
├── dev-workflow.sh           # Development workflow script (bash)
├── timesheet_project/        # Project settings
│   ├── settings.py           # Django configuration
│   ├── urls.py              # Root URL patterns
│   └── wsgi.py              # WSGI configuration
├── timesheet_app/            # Main application
│   ├── models.py            # Data models (Job, TimeEntry)
│   ├── views.py             # View logic (12 views)
│   ├── forms.py             # Form definitions (4 forms)
│   ├── urls.py              # App URL patterns
│   ├── admin.py             # Admin interface
│   ├── templates/           # HTML templates (8 templates)
│   │   └── timesheet/       # App-specific templates
│   └── static/              # CSS, JS, images
└── db.sqlite3               # Development database
```

## 🎨 UI/UX Guidelines

### Design Principles
- **Responsive First**: Mobile-friendly design
- **Bootstrap 5**: Use Bootstrap components and utilities
- **Consistent Icons**: Font Awesome icons throughout
- **Professional Colors**: Blue-purple gradient theme
- **User-Friendly**: Intuitive navigation and forms

### Template Structure
```django
{% extends 'timesheet/base.html' %}

{% block title %}Page Title{% endblock %}

{% block content %}
<!-- Page content here -->
{% endblock %}
```

## 🔧 Common Development Tasks

### Adding a New Model Field
1. Edit `models.py`
2. Create migration: `python manage.py makemigrations`
3. Apply migration: `python manage.py migrate`
4. Update forms and templates as needed

### Adding a New View
1. Add view function to `views.py`
2. Add URL pattern to `urls.py`
3. Create template in `templates/timesheet/`
4. Test functionality

### Debugging Template Issues
1. Check Django debug toolbar output
2. Verify template syntax with `{% load %}` tags
3. Use `{{ variable|pprint }}` for debugging
4. Check context variables in view

## 🔒 Security Considerations
- All views use `@login_required` decorator
- CSRF protection on all forms
- User data isolation (users only see their own data)
- Input validation in forms and models
- SQL injection prevention via Django ORM

## 📊 Performance Tips
- Use `select_related()` for foreign key relationships
- Use `prefetch_related()` for many-to-many relationships
- Implement pagination for large datasets
- Optimize database queries
- Use Django debug toolbar to identify bottlenecks

## 🐛 Troubleshooting

### Common Issues

#### Template Syntax Errors
```
TemplateSyntaxError: Invalid filter: 'div'
```
**Solution**: Use view calculations instead of template filters for math

#### Migration Issues
```
django.db.utils.OperationalError: no such table
```
**Solution**: Run `python manage.py migrate`

#### Import Errors
```
ModuleNotFoundError: No module named 'timesheet_app'
```
**Solution**: Ensure you're in the correct directory with `manage.py`

#### Server Won't Start
```
Error: That port is already in use
```
**Solution**: Use different port or kill existing process

### Debug Mode
Enable detailed error pages in `settings.py`:
```python
DEBUG = True
```

## 🚀 Deployment Preparation

### Production Checklist
- [ ] `DEBUG = False`
- [ ] Configure production database
- [ ] Set up static file serving
- [ ] Configure email backend
- [ ] Set up logging
- [ ] Use environment variables for secrets
- [ ] Configure HTTPS
- [ ] Set `ALLOWED_HOSTS`

## 📚 Additional Resources
- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)
- [Font Awesome Icons](https://fontawesome.com/icons)
- [FamilyHub Integration Guide](../../../README.md)

## 👥 Team Collaboration

### Code Review Process
1. Create feature branch
2. Implement changes
3. Push to remote repository
4. Create pull request
5. Request code review
6. Address feedback
7. Merge after approval

### Communication
- Use descriptive pull request titles
- Link issues in PR descriptions
- Comment on complex code sections
- Update documentation when needed

---

**Happy Coding! 🎉**

For questions or support, refer to the main FamilyHub documentation or create an issue in the repository.
