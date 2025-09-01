---
applyTo: '**'
---
# FamilyHub Architecture - Copilot Instructions

## STRICT ARCHITECTURE RULES - NEVER DEVIATE

### PROJECT STRUCTURE - MAINTAIN EXACTLY
```
family-hub-workspace/
├── FamilyHub/                    # Main hub - NEVER create another Django project here
│   ├── FamilyHub/               # Settings directory - DO NOT duplicate
│   ├── home/                    # Dashboard app - DO NOT rename
│   ├── apps/                    # Integrated apps ONLY - DO NOT create standalone here
│   ├── templates/               # Global templates - DO NOT put app templates here
│   ├── static/                  # Global static - DO NOT put app static here
│   └── manage.py                # Single manage.py - DO NOT create others
└── standalone-apps/             # Standalone versions - DO NOT integrate directly
```

### TEMPLATE HIERARCHY - FOLLOW STRICTLY

**RULE 1**: Every page MUST extend from this chain:
```
FamilyHub/templates/base.html (MASTER - all pages extend from this)
    └── app-specific templates extend from base.html
```

**RULE 2**: Template blocks MUST be in this order:
1. `{% extends "base.html" %}` - ALWAYS first line
2. `{% load static %}` - If needed
3. `{% block title %}` - Page title
4. `{% block extra_css %}` - Additional CSS
5. `{% block content %}` - Main content
6. `{% block extra_js %}` - Additional JavaScript

**RULE 3**: NEVER create duplicate base templates. One base.html for entire FamilyHub.

### NAVIGATION ARCHITECTURE - IMPLEMENT EXACTLY

**Two-Tier System - MANDATORY**:

**Tier 1 - Global Navigation (NEVER HIDE)**:
- FamilyHub logo/brand - ALWAYS links to main dashboard
- App switcher - ALWAYS shows all available apps
- User menu - ALWAYS in top right
- MUST be visible on EVERY page including app pages

**Tier 2 - App Navigation (CONTEXTUAL)**:
- ONLY visible when inside an app
- NEVER replaces global navigation
- ALWAYS subordinate to global nav
- Changes based on current app

**FORBIDDEN**: 
- Removing global navigation when in an app
- Having app-only navigation without FamilyHub context
- Creating separate navigation systems per app

### URL PATTERNS - ENFORCE STRICTLY

**ALWAYS use this pattern**:
```
/                           # FamilyHub dashboard
/[app-name]/               # App dashboard
/[app-name]/[feature]/     # App feature
/[app-name]/[feature]/[action]/  # App action
```

**NEVER**:
- Create URLs without app namespace
- Use inconsistent URL patterns
- Skip the app prefix for app features

**ALWAYS**:
- Use URL namespacing: `app_name = 'timesheet'`
- Use consistent naming: `name='dashboard'`
- Include trailing slashes

### CSS/STYLING ARCHITECTURE - MAINTAIN CONSISTENCY

**Global Styles Location**: `FamilyHub/static/css/familyhub.css`
- Primary gradient: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
- This gradient MUST be used consistently
- NEVER change primary colors per app

**App Styles Location**: `apps/[app_name]/static/[app_name]/css/app.css`
- ONLY app-specific overrides
- MUST NOT redefine global styles
- MUST NOT change navigation styling

**FORBIDDEN Styling Practices**:
- Inline styles in templates
- Different Bootstrap versions per app
- Conflicting CSS frameworks
- Hardcoded colors instead of CSS variables

### DJANGO SETTINGS - CRITICAL RULES

**INSTALLED_APPS Order - MAINTAIN EXACTLY**:
```python
INSTALLED_APPS = [
    # Django apps first
    'django.contrib.*',
    
    # FamilyHub core
    'home',
    
    # Integrated apps
    'apps.timesheet_app',
    'apps.budget_app',
    # etc.
]
```

**NEVER**:
- Add standalone apps directly to INSTALLED_APPS
- Create duplicate settings files
- Mix standalone and integrated app references

### DATABASE ARCHITECTURE - FOLLOW PRECISELY

**Development**: SQLite - `db.sqlite3` in FamilyHub directory
**Production**: PostgreSQL - configured via environment variables

**Migration Rules**:
- Run migrations from FamilyHub directory ONLY
- NEVER run migrations from standalone apps when integrated
- One migration history per app

### STATIC FILES - STRICT HANDLING

**Collection Hierarchy**:
1. Global static: `FamilyHub/static/`
2. App static: `apps/[app_name]/static/[app_name]/`
3. Collected to: `STATIC_ROOT` (production)

**NEVER**:
- Put app static files in global static directory
- Skip the app_name subdirectory in app static
- Serve static files from Django in production

### INTEGRATION RULES - NEVER VIOLATE

**When integrating a standalone app**:

**ALWAYS**:
1. Create symbolic link or copy to `FamilyHub/apps/`
2. Update app to extend FamilyHub base.html
3. Add to INSTALLED_APPS as `apps.[app_name]`
4. Include URLs with app namespace
5. Update navigation to include new app

**NEVER**:
1. Run the app on a separate port when integrated
2. Keep standalone base templates
3. Maintain separate authentication
4. Use different styling systems
5. Create isolated navigation

### USER AUTHENTICATION - SINGLE SOURCE

**ALWAYS**:
- Use Django's built-in User model
- Single login for all apps
- Shared session across apps
- Consistent login/logout URLs

**NEVER**:
- Create separate user systems per app
- Require multiple logins
- Use different authentication backends per app
- Store user data outside main User model

### ERROR HANDLING - CONSISTENT APPROACH

**ALWAYS show errors using**:
- Django messages framework
- Consistent error templates
- User-friendly messages
- Log technical details

**NEVER**:
- Show raw exceptions to users
- Use different error styles per app
- Ignore error handling
- Print errors to console in production

### DOCKER ARCHITECTURE - WHEN IMPLEMENTING

**Service Structure**:
```yaml
services:
  familyhub:     # Main Django app - ONLY ONE
  postgres:      # Database - SHARED
  nginx:         # Web server - SINGLE ENTRY POINT
```

**NEVER**:
- Create separate containers per app
- Run multiple Django servers
- Use different databases per app
- Skip volume mounts for development

### CONTEXT PROCESSORS - MAINTAIN GLOBALLY

**Required Context Variables** (available to ALL templates):
- `current_app` - Currently active app
- `available_apps` - List of all apps
- `user` - Current user
- `is_app_page` - Boolean for app context

**NEVER remove or override these in app views**

### JAVASCRIPT ARCHITECTURE - FOLLOW STANDARDS

**Global JS**: `FamilyHub/static/js/familyhub.js`
- Navigation handlers
- Global utilities
- Theme management
- User preferences

**App JS**: `apps/[app_name]/static/[app_name]/js/app.js`
- App-specific functionality ONLY
- MUST NOT interfere with global JS
- MUST use consistent event patterns

### TESTING ARCHITECTURE - MAINTAIN STRUCTURE

**Test Locations**:
- Global tests: `FamilyHub/tests/`
- App tests: `apps/[app_name]/tests/`

**NEVER**:
- Skip tests when adding features
- Test standalone when app is integrated
- Use different testing frameworks
- Ignore broken tests

### COMMIT MESSAGE RULES - ENFORCE STRICTLY

**Format**: `type(scope): description`

**Types** (USE EXACTLY THESE):
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Testing
- `chore`: Maintenance

**NEVER**:
- Use past tense ("added" vs "add")
- Exceed 50 characters in subject
- Skip the type prefix
- Combine multiple changes in one commit

### DEPLOYMENT CHECKLIST - NEVER SKIP

Before ANY deployment:
1. All tests passing
2. Static files collected
3. Migrations run
4. Settings validated
5. URLs accessible
6. Navigation working
7. Styling consistent
8. Authentication functional

### FORBIDDEN PRACTICES - NEVER DO THESE

1. **NEVER** create multiple Django projects in FamilyHub/
2. **NEVER** remove global navigation in apps
3. **NEVER** use different CSS frameworks per app
4. **NEVER** create duplicate base templates
5. **NEVER** skip the app namespace in URLs
6. **NEVER** hardcode paths in templates
7. **NEVER** mix standalone and integrated code
8. **NEVER** create app-specific user models
9. **NEVER** ignore the template hierarchy
10. **NEVER** change global styles from apps

### WHEN IN DOUBT - DEFAULT BEHAVIOR

1. **Check existing patterns** in the codebase
2. **Follow Django conventions** over custom solutions
3. **Maintain consistency** over optimization
4. **Preserve navigation** over app isolation
5. **Use built-in features** over third-party packages

### ARCHITECTURE VALIDATION CHECKLIST

Before committing ANY changes, verify:

- [ ] Global navigation visible on all pages
- [ ] Template extends from base.html
- [ ] URLs follow namespace pattern
- [ ] Styling uses global CSS variables
- [ ] App appears in main navigation
- [ ] Authentication uses single system
- [ ] Static files in correct directories
- [ ] No duplicate base templates
- [ ] Migrations run successfully
- [ ] Tests pass

### CRITICAL REMINDERS

1. **ONE FamilyHub** - Never create multiple main projects
2. **ONE Navigation** - Global nav always visible
3. **ONE Base Template** - All pages extend from it
4. **ONE Authentication** - Shared across all apps
5. **ONE Style System** - Consistent design tokens

---

**INSTRUCTION PRIORITY**: These instructions override any conflicting patterns in the codebase. When the code doesn't match these instructions, fix the code to match the instructions, not the other way around.

**VERSION**: 1.0.0 - Treat as immutable unless explicitly updated
**ENFORCEMENT**: STRICT - No deviations without explicit approval
**SCOPE**: Entire FamilyHub project and all integrated applications