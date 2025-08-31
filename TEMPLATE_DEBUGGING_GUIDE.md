# Template Debugging System for FamilyHub

## Overview

The FamilyHub template debugging system provides visual indicators and debugging information to help developers understand which templates are being rendered and their context during development.

## Features

### 🎯 Debug Banner
- **Location**: Appears at the top of every page when `DEBUG=True`
- **Information Displayed**:
  - Current template path
  - Template directory context (Global, App-specific, etc.)
  - App context (FamilyHub Core, Integrated App, etc.)
  - HTTP request method
- **Visual Design**: Purple gradient banner with clear typography

### 🔍 Template Tags

#### `{% template_debug_banner %}`
Displays the main debug banner with comprehensive template information.
```django
{% load debug_tags %}
{% template_debug_banner %}
```

#### `{% template_info "template_name.html" %}`
Shows specific template information in a small alert box.
```django
{% template_info "timesheet/dashboard.html" %}
{% template_info "base.html" True %}  <!-- Show full path -->
```

#### `{% show_template_path %}`
Displays just the current template path.
```django
{% show_template_path %}
```

#### `{% debug_context_vars "var1" "var2" "var3" %}`
Shows context variable information including type and content preview.
```django
{% debug_context_vars "user" "apps" "request" %}
```

#### `{% template_hierarchy %}`
Displays template inheritance hierarchy (simplified version).
```django
{% template_hierarchy %}
```

### 🛠️ Filter Tags

#### `{{ variable|debug_type }}`
Returns the Python type of a variable.
```django
{{ some_list|debug_type }}  <!-- Output: list -->
```

#### `{{ variable|debug_length }}`
Returns the length of a variable if applicable.
```django
{{ some_list|debug_length }}  <!-- Output: 5 -->
```

## Implementation

### Template Updates Made

1. **Base Templates**: Added debug banners to:
   - `FamilyHub/templates/base.html` - Main layout template
   - `FamilyHub/apps/timesheet_app/templates/timesheet/base.html` - Timesheet base

2. **Page Templates**: Added debug info to:
   - `home/templates/home/dashboard.html` - Main dashboard
   - `timesheet_app/templates/timesheet/dashboard.html` - Timesheet dashboard
   - `timesheet_app/templates/timesheet/entry_form.html` - Entry forms

3. **Debug Showcase**: Created comprehensive demo at `/debug/templates/`

### File Structure
```
FamilyHub/
├── home/
│   ├── templatetags/
│   │   ├── __init__.py
│   │   └── debug_tags.py          # Main template tags
│   ├── debug_views.py             # Debug showcase view
│   └── urls.py                    # Includes debug URLs
├── templates/
│   ├── base.html                  # Updated with debug banner
│   └── debug/
│       └── template_showcase.html # Debug demonstration page
└── apps/
    └── timesheet_app/
        └── templates/
            └── timesheet/
                ├── base.html      # Updated with debug banner
                ├── dashboard.html # Updated with debug info
                └── entry_form.html # Updated with context debug
```

## Usage Guide

### For Developers

1. **Enable Debug Mode**: Ensure `DEBUG=True` in your Django settings
2. **Load Template Tags**: Add `{% load debug_tags %}` to any template
3. **Add Debug Banners**: Use `{% template_debug_banner %}` in base templates
4. **Debug Context**: Use `{% debug_context_vars %}` to inspect context data
5. **Test Templates**: Visit `/debug/templates/` for comprehensive debugging info

### Debug Information Available

- **Template Path**: Full file path from workspace root
- **Template Directory Context**: Whether it's Global, App-specific, etc.
- **App Context**: Which app/component is rendering the template
- **Request Method**: GET, POST, etc.
- **Context Variables**: Type, length, and content preview
- **Template Hierarchy**: Inheritance chain (simplified)

### Visual Indicators

1. **Debug Banner**: Purple gradient bar at top with template info
2. **Template Info Cards**: Blue info alerts with template details
3. **Context Debug**: Secondary alerts showing variable information
4. **Warning Banners**: Yellow alerts for debug-mode-only features

## Testing URLs

Visit these URLs to see template debugging in action:

- `/` - Main dashboard with debug banner
- `/debug/templates/` - Comprehensive debug showcase
- `/timesheet/` - Timesheet dashboard (after login)
- `/timesheet/entries/add/` - Form with context debugging (after login)

## Security Notes

⚠️ **Important**: All debugging features are **only active when `DEBUG=True`**

- Template tags return empty strings in production (`DEBUG=False`)
- Debug views raise 404 errors in production
- No sensitive information is exposed in production mode

## Development Workflow

### Adding Debug Info to New Templates

1. Load the debug tags:
```django
{% load debug_tags %}
```

2. Add template info at the top of content blocks:
```django
{% block content %}
{% template_info "your_app/your_template.html" %}
<!-- Your content here -->
{% endblock %}
```

3. Debug specific context variables:
```django
{% debug_context_vars "form" "user" "custom_data" %}
```

### Creating Debug Views

For testing specific template scenarios:

```python
# In your debug_views.py
def template_test_view(request):
    if not settings.DEBUG:
        raise Http404("Page not available in production mode")
    
    context = {
        'test_data': 'Your test data here',
        # ... other context
    }
    return render(request, 'debug/test_template.html', context)
```

## Troubleshooting

### Common Issues

1. **Debug banner not showing**: Check that `DEBUG=True` in settings
2. **Template tags not found**: Ensure `{% load debug_tags %}` is at top of template
3. **Module import errors**: Verify `home` app is in `INSTALLED_APPS`

### Debug Information Not Accurate

The template debugging system tries to extract template path information from Django's template system. In some cases, the path information might be:

- Showing absolute paths instead of relative paths
- Missing for dynamically generated templates
- Incorrect for included templates or template fragments

This is normal and the system provides the best available information.

## Future Enhancements

Potential improvements to the debugging system:

1. **Template Performance**: Add rendering time information
2. **Context Inspector**: Interactive context variable browser
3. **Template Graph**: Visual template inheritance diagram
4. **Cache Information**: Show template caching status
5. **SQL Queries**: Display related database queries (requires django-debug-toolbar integration)

---

**Last Updated**: September 1, 2025
**Version**: 1.0
**Compatibility**: Django 5.1+, FamilyHub Project
