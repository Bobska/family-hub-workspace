# Template Debugging for Standalone Apps - Implementation Guide

## Overview

This guide shows how to add the template debugging system to FamilyHub standalone apps, providing visual debugging capabilities during development.

## What We've Implemented

### ✅ **Timesheet App (Complete)**
- **Location**: `standalone-apps/timesheet/`
- **Status**: ✅ FULLY IMPLEMENTED
- **Features**: Orange debug banners, template info cards, context debugging
- **Test URL**: `http://127.0.0.1:8001/debug/templates/`

### 🔄 **Other Standalone Apps (Ready for Setup)**
- **Daycare Invoice**: `standalone-apps/daycare_invoice/`
- **Credit Card Management**: `standalone-apps/credit_card_mgmt/`
- **Upcoming Payments**: `standalone-apps/upcoming_payments/`
- **Employment History**: `standalone-apps/employment_history/`
- **Household Budget**: `standalone-apps/household_budget/`

## Files Created

### 1. **Universal Debug Template Tags**
```
shared/templatetags/
├── __init__.py
└── debug_tags_universal.py    # Generic template tags for any app
```

### 2. **Timesheet App Debug Implementation**
```
standalone-apps/timesheet/timesheet_app/
├── templatetags/
│   ├── __init__.py
│   └── debug_tags.py          # Timesheet-specific debug tags
├── templates/timesheet/
│   ├── base.html              # Updated with debug banner
│   ├── dashboard.html         # Updated with debug info
│   ├── entry_form.html        # Updated with context debugging
│   ├── daily_entry.html       # Updated with template info
│   └── debug_showcase.html    # Complete debug demonstration
├── debug_views.py             # Debug showcase view
└── urls.py                    # Updated with debug URL
```

### 3. **Setup Automation**
```
setup_template_debug.py        # Script to add debugging to any app
```

## Visual Features

### 🎨 **Debug Banner Colors by App**
- **Timesheet**: Orange gradient (`#f59e0b` → `#d97706`) 🕒
- **FamilyHub Integrated**: Purple gradient (`#667eea` → `#764ba2`) 🔧
- **Future Apps**: Each app gets unique colors and icons

### 📊 **Information Displayed**
1. **Template Path**: Relative path from workspace root
2. **App Context**: Independent Mode, Integrated Mode, etc.
3. **Template Directory**: Standalone App, Global Templates, etc.
4. **Request Method**: GET, POST, etc.
5. **Context Variables**: Type, length, content preview

## Testing Results

### ✅ **Timesheet Standalone App**
```bash
# Server running on port 8001
cd standalone-apps/timesheet
python manage.py runserver 8001
```

**Working URLs:**
- `http://127.0.0.1:8001/` - Dashboard with debug banner
- `http://127.0.0.1:8001/debug/templates/` - Debug showcase
- `http://127.0.0.1:8001/entries/add/` - Form with context debugging
- `http://127.0.0.1:8001/daily/` - Daily view with template info

**Server Output:**
```
System check identified no issues (0 silenced).
Django version 5.0.14, using settings 'timesheet_project.settings'
Starting development server at http://127.0.0.1:8001/
```

## Setup Guide for Other Apps

### Method 1: Automatic Setup (Recommended)
```bash
# For Daycare Invoice app
python setup_template_debug.py standalone-apps/daycare_invoice "Daycare Invoice" "#ef4444" "🧾"

# For Credit Card Management
python setup_template_debug.py standalone-apps/credit_card_mgmt "Credit Card" "#10b981" "💳"

# For Upcoming Payments
python setup_template_debug.py standalone-apps/upcoming_payments "Upcoming Payments" "#f59e0b" "📅"

# For Employment History
python setup_template_debug.py standalone-apps/employment_history "Employment" "#8b5cf6" "💼"

# For Household Budget
python setup_template_debug.py standalone-apps/household_budget "Budget" "#06b6d4" "💰"
```

### Method 2: Manual Setup
1. **Copy template tags**:
   ```bash
   mkdir your_app/templatetags
   cp shared/templatetags/debug_tags_universal.py your_app/templatetags/debug_tags.py
   ```

2. **Customize the debug_tags.py**:
   ```python
   APP_NAME = "Your App Name"
   APP_COLOR = "#your-color"
   APP_ICON = "🎯"
   ```

3. **Update templates**:
   ```django
   {% load debug_tags %}
   {% template_debug_banner %}
   ```

4. **Add debug URLs**:
   ```python
   path('debug/templates/', debug_views.template_debug_showcase, name='template_debug'),
   ```

## Template Tag Usage

### Basic Usage
```django
{% load debug_tags %}
{% template_debug_banner %}                    <!-- Main debug banner -->
{% template_info "template_name.html" %}       <!-- Template info card -->
{% show_template_path %}                       <!-- Simple path display -->
```

### Advanced Usage
```django
{% debug_context_vars "user" "data" "form" %}  <!-- Context inspection -->
{% template_hierarchy %}                       <!-- Template inheritance -->
{% app_debug_info %}                          <!-- App-specific info -->
```

### Filter Usage
```django
{{ some_variable|debug_type }}                <!-- Show variable type -->
{{ some_list|debug_length }}                  <!-- Show length -->
```

## Security Features

### 🔒 **Production Safety**
- **DEBUG-only activation**: All features disabled when `DEBUG=False`
- **No data exposure**: Safe for production deployment
- **Clean templates**: Debug tags return empty strings in production

### 🛡️ **Development Mode**
- **Visual indicators**: Clear banners showing debug mode
- **Context inspection**: Safe preview of variable contents
- **Path information**: Helpful for development navigation

## App-Specific Configurations

### 🕒 **Timesheet App**
- **Color**: Orange (`#f59e0b`)
- **Icon**: 🕒
- **Context**: "Standalone Timesheet"
- **Special**: Time entry context debugging

### 🧾 **Daycare Invoice App (Planned)**
- **Color**: Red (`#ef4444`)
- **Icon**: 🧾
- **Context**: "Standalone Invoice"
- **Special**: Invoice data debugging

### 💳 **Credit Card Management (Planned)**
- **Color**: Green (`#10b981`)
- **Icon**: 💳
- **Context**: "Standalone Credit"
- **Special**: Financial data debugging

### 📅 **Upcoming Payments (Planned)**
- **Color**: Amber (`#f59e0b`)
- **Icon**: 📅
- **Context**: "Standalone Payments"
- **Special**: Payment schedule debugging

### 💼 **Employment History (Planned)**
- **Color**: Purple (`#8b5cf6`)
- **Icon**: 💼
- **Context**: "Standalone Employment"
- **Special**: Career data debugging

### 💰 **Household Budget (Planned)**
- **Color**: Cyan (`#06b6d4`)
- **Icon**: 💰
- **Context**: "Standalone Budget"
- **Special**: Financial planning debugging

## Development Workflow

### 1. **Start Development**
```bash
cd standalone-apps/your-app
source venv/Scripts/activate  # Windows
python manage.py runserver 8001  # Use different port for each app
```

### 2. **Access Debug Features**
- Visit: `http://127.0.0.1:8001/debug/templates/`
- Check debug banners on all pages
- Inspect context variables in forms
- Review template hierarchy

### 3. **Debug Template Issues**
- Use `{% show_template_path %}` to confirm template loading
- Use `{% debug_context_vars %}` to inspect available data
- Check debug banner for app context information

## Comparison: Integrated vs Standalone

### 🏠 **FamilyHub Integrated Mode**
- **Banner Color**: Purple gradient
- **Context**: "FamilyHub Core", "Integrated App"
- **URL**: `http://127.0.0.1:8000/debug/templates/`
- **Navigation**: Unified navigation with other apps

### 🔧 **Standalone Mode**
- **Banner Color**: App-specific (Orange for timesheet)
- **Context**: "Independent Mode", "Standalone App"
- **URL**: `http://127.0.0.1:8001/debug/templates/` (unique port)
- **Navigation**: App-specific navigation

## Benefits for Development

### 🎯 **Immediate Benefits**
1. **Visual template identification** - Know which template is rendering
2. **Context debugging** - See available variables and their types
3. **Template path tracking** - Understand template loading order
4. **App mode awareness** - Know if running standalone or integrated

### 🚀 **Long-term Benefits**
1. **Faster debugging** - Quickly identify template issues
2. **Better understanding** - See how templates inherit and include
3. **Context awareness** - Know what data is available where
4. **Development confidence** - Visual confirmation of template behavior

---

**Status**: Template debugging successfully implemented for standalone timesheet app, with universal system ready for other apps.

**Next Steps**: Use the setup script to add debugging to other standalone apps as they develop templates and views.
