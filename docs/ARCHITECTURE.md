# FamilyHub Architecture Reference Document

## CRITICAL CONCEPT: Single Source of Truth

### The Core Problem We're Solving
**Duplication Issue**: Templates and code are being duplicated between:
- `standalone-apps/timesheet/timesheet_app/` (full implementation)
- `FamilyHub/apps/timesheet_app/` (empty stubs or duplicates)

**Solution**: ONE implementation that works in BOTH contexts through symbolic links or intelligent imports.

## Architecture Foundation

### 1. Application Dual-Mode Strategy

Each app has **ONE codebase** that can run in **TWO modes**:

#### Standalone Mode
- Location: `standalone-apps/[app-name]/[app-name]_app/`
- Has its own Django project wrapper for independent development
- Uses its own base template for standalone operation
- Runs on separate port (8001, 8002, etc.)
- Complete, self-contained functionality

#### Integrated Mode
- Location: `FamilyHub/apps/[app-name]_app/` (SYMBOLIC LINK to standalone)
- NOT a copy - links to the standalone implementation
- Templates detect integration and extend FamilyHub base
- Runs as part of FamilyHub on port 8000
- Same code, different context

### 2. Directory Structure - The Truth

```
family-hub-workspace/
├── FamilyHub/                           # Main integrated platform
│   ├── FamilyHub/                       # Django settings directory
│   │   ├── settings.py                  # Main configuration
│   │   └── urls.py                      # Root URL config
│   ├── home/                            # Dashboard app (native to FamilyHub)
│   │   └── templates/home/              # Dashboard templates
│   ├── apps/                            # SYMBOLIC LINKS to standalone apps
│   │   ├── timesheet_app -> ../../standalone-apps/timesheet/timesheet_app
│   │   └── budget_app -> ../../standalone-apps/budget/budget_app
│   ├── templates/                       # Global templates
│   │   └── base.html                    # Master base template
│   └── static/                          # Global static files
│
└── standalone-apps/                     # Independent app development
    ├── timesheet/                       # Timesheet project wrapper
    │   ├── manage.py                    # For standalone running
    │   ├── timesheet_project/           # Project settings for standalone
    │   └── timesheet_app/               # THE ACTUAL APP (single source)
    │       ├── models.py                # Real implementation
    │       ├── views.py                 # Real implementation
    │       ├── urls.py                  # Real implementation
    │       └── templates/               # App templates
    │           └── timesheet/           
    │               └── *.html           # Templates that adapt
    └── budget/                          # Same structure
```

### 3. Template Inheritance Strategy - NO DUPLICATION

#### The Smart Template Pattern

Each app template uses conditional inheritance:

```django
{# timesheet_app/templates/timesheet/dashboard.html #}
{% if integrated_mode %}
    {% extends "base.html" %}  {# FamilyHub base #}
{% else %}
    {% extends "timesheet/standalone_base.html" %}  {# Standalone base #}
{% endif %}

{% block content %}
    {# Same content for both modes #}
{% endblock %}
```

#### Template Locations (NO DUPLICATION)
- **App templates**: `standalone-apps/[app]/[app]_app/templates/[app]/`
- **FamilyHub base**: `FamilyHub/templates/base.html`
- **Standalone base**: Within each app's template directory
- **NEVER**: Create templates in `FamilyHub/apps/` - they're symbolic links

### 4. How Integration Actually Works

#### Step 1: Create Symbolic Link
```bash
cd FamilyHub/apps/
ln -s ../../standalone-apps/timesheet/timesheet_app timesheet_app
```

#### Step 2: App Detects Context
Views pass `integrated_mode` context variable:
```python
def dashboard(request):
    context = {
        'integrated_mode': 'familyhub' in request.resolver_match.app_name,
        # ... other context
    }
    return render(request, 'timesheet/dashboard.html', context)
```

#### Step 3: Template Adapts
Template extends appropriate base based on context.

#### Step 4: URLs Include
FamilyHub includes app URLs:
```python
urlpatterns = [
    path('timesheet/', include('apps.timesheet_app.urls')),
]
```

### 5. Static Files Strategy

#### App Static Files (Single Location)
- Location: `standalone-apps/[app]/[app]_app/static/[app]/`
- Collected by Django's collectstatic
- Same files used in both modes

#### Global Static Files
- Location: `FamilyHub/static/`
- Contains FamilyHub-specific styles
- Apps reference these when integrated

### 6. Settings Configuration

#### FamilyHub Settings
```python
INSTALLED_APPS = [
    # ...
    'apps.timesheet_app',  # Points to symbolic link
]

# Add standalone apps to Python path for imports
import sys
sys.path.insert(0, str(BASE_DIR / 'apps'))
```

#### Standalone Settings
```python
INSTALLED_APPS = [
    # ...
    'timesheet_app',  # Direct reference
]
```

### 7. URL Namespace Strategy

#### App URLs Define Namespace
```python
# timesheet_app/urls.py
app_name = 'timesheet'  # Same in both modes

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # ...
]
```

#### FamilyHub Includes with Prefix
```python
# FamilyHub/urls.py
urlpatterns = [
    path('timesheet/', include('apps.timesheet_app.urls')),
    # Results in: /timesheet/ URLs in integrated mode
]
```

#### Standalone Direct Include
```python
# standalone-apps/timesheet/timesheet_project/urls.py
urlpatterns = [
    path('', include('timesheet_app.urls')),
    # Results in: / URLs in standalone mode
]
```

### 8. Development Workflow

#### Working on an App
1. Develop in `standalone-apps/timesheet/`
2. Run standalone: `python manage.py runserver 8001`
3. Test in isolation
4. Changes automatically reflected in FamilyHub (symbolic link)
5. Test integrated: Run FamilyHub on port 8000

#### Adding New App
1. Create in `standalone-apps/new_app/`
2. Develop and test standalone
3. Create symbolic link in `FamilyHub/apps/`
4. Add to FamilyHub's INSTALLED_APPS
5. Include URLs in FamilyHub

### 9. Migration Strategy

#### Development
- Run migrations from app's standalone directory during development
- Run from FamilyHub after integration

#### Production
- All migrations run from FamilyHub
- Single database for all integrated apps

### 10. Context Processors

#### Integration Detection
```python
def integration_context(request):
    """Provides integration context to all templates"""
    return {
        'integrated_mode': 'FamilyHub' in settings.ROOT_URLCONF,
        'familyhub_nav': True if 'FamilyHub' in settings.ROOT_URLCONF else False,
    }
```

### 11. Docker Considerations

#### Symbolic Links in Docker
```dockerfile
# Create symbolic links in Dockerfile
RUN ln -s /app/standalone-apps/timesheet/timesheet_app /app/FamilyHub/apps/timesheet_app
```

#### Volume Mounts for Development
```yaml
volumes:
  - ./standalone-apps:/app/standalone-apps
  - ./FamilyHub:/app/FamilyHub
```

### 12. Testing Strategy

#### Standalone Tests
```bash
cd standalone-apps/timesheet
python manage.py test timesheet_app
```

#### Integration Tests
```bash
cd FamilyHub
python manage.py test apps.timesheet_app
```

### 13. Common Pitfalls to Avoid

#### NEVER DO:
1. Copy app code to FamilyHub/apps/ - use symbolic links
2. Create templates in FamilyHub/apps/ - they live in standalone
3. Duplicate static files - single source in standalone
4. Hard-code paths in templates - use URL reversal
5. Create app-specific base templates in FamilyHub

#### ALWAYS DO:
1. Develop in standalone-apps/
2. Use symbolic links for integration
3. Make templates context-aware
4. Test in both modes
5. Keep single source of truth

### 14. Navigation Architecture in Practice

#### Two-Tier System Implementation
- **Tier 1**: FamilyHub navigation (in FamilyHub base.html)
- **Tier 2**: App navigation (in app templates, conditional on integration)

#### Navigation Visibility
- Standalone: Only app navigation visible
- Integrated: Both FamilyHub and app navigation visible

### 15. Deployment Strategy

#### Production Build
1. Collect all apps via symbolic links
2. Run collectstatic from FamilyHub
3. Single deployment unit
4. Environment variables determine mode

### 16. Database Relationships

#### Shared User Model
- Both modes use Django's User model
- No duplicate user systems
- Session sharing when integrated

#### App-Specific Models
- Defined once in standalone app
- Same models used in both modes
- Foreign keys work identically

### 17. Authentication Flow

#### Standalone Mode
- App handles its own login/logout
- Uses Django's built-in auth

#### Integrated Mode
- FamilyHub handles authentication
- Apps check authentication status
- Single sign-on experience

### 18. Error Handling

#### App Errors
- Handled by app's error views
- Styled appropriately for mode

#### Integration Errors
- FamilyHub provides fallback error pages
- Consistent error experience

### 19. Performance Optimization

#### Static File Serving
- Single collection point
- CDN-ready structure
- Cached appropriately

#### Database Queries
- Same optimizations work in both modes
- Shared query patterns

### 20. Future Scalability

#### Adding Apps
- Simple symbolic link process
- No code changes needed
- Automatic integration

#### Removing Apps
- Remove symbolic link
- Remove from INSTALLED_APPS
- No residual code

## Architecture Decision Log

### Decision: Symbolic Links Over Copying
**Rationale**: Maintains single source of truth, eliminates sync issues
**Trade-off**: Requires filesystem support for symbolic links

### Decision: Context-Aware Templates
**Rationale**: Same templates work in both modes
**Trade-off**: Slightly more complex template logic

### Decision: Single App Implementation
**Rationale**: No code duplication, easier maintenance
**Trade-off**: Apps must be designed for dual-mode operation

## Success Metrics

1. **Zero Code Duplication**: Each app has one implementation
2. **Seamless Integration**: Apps work identically in both modes
3. **Developer Efficiency**: Changes reflected immediately
4. **Maintainability**: Single point of updates
5. **Scalability**: Easy to add/remove apps

---

**Version**: 2.0.0  
**Last Updated**: Current  
**Purpose**: Eliminate duplication and confusion in app integration