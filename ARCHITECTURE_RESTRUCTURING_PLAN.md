# FamilyHub Architecture Restructuring Plan
=============================================

## 🎯 OBJECTIVE
Restructure codebase to follow Architecture.instructions.md and docs/ARCHITECTURE.md EXACTLY with no deviations.

## 🚨 VIOLATIONS IDENTIFIED

### 1. Template Hierarchy Violations
**RULE**: "NEVER create duplicate base templates. One base.html for entire FamilyHub."
**VIOLATIONS**:
- ❌ Multiple base templates exist
- ❌ App-specific base templates (base_unified.html, timesheet/base.html)
- ❌ Templates not extending directly from master base.html
- ❌ Global template directory contains app-specific templates

### 2. Project Structure Violations  
**RULE**: "apps/ - Integrated apps ONLY - DO NOT create standalone here"
**VIOLATIONS**:
- ❌ Duplicate template structures in multiple locations
- ❌ shared/ directory referenced but not in official architecture
- ❌ Template directory precedence conflicts

### 3. Navigation Architecture Violations
**RULE**: "Two-Tier System - MANDATORY"
**VIOLATIONS**:
- ❌ Complex navigation hierarchy instead of simple two-tier
- ❌ App navigation not properly subordinate to global navigation

## 🔧 RESTRUCTURING ACTIONS

### Phase 1: Template Structure Cleanup
1. **REMOVE all duplicate base templates**
2. **ENFORCE single base.html inheritance**
3. **MOVE app-specific templates to proper locations**
4. **CLEAN UP template directory references**

### Phase 2: Navigation Simplification
1. **IMPLEMENT exact two-tier navigation as specified**
2. **REMOVE complex navigation hierarchies**
3. **ENSURE global nav always visible**

### Phase 3: Directory Structure Compliance
1. **REMOVE unauthorized directories (shared/)**
2. **CONSOLIDATE app templates in FamilyHub/apps/[app_name]/templates/**
3. **ENSURE proper INSTALLED_APPS configuration**

### Phase 4: Settings Compliance
1. **FIX template DIRS to match architecture**
2. **REMOVE non-compliant context processors**
3. **ENSURE proper app registration**

## 📋 IMPLEMENTATION CHECKLIST

### Template Cleanup ✅ TODO
- [ ] Delete all duplicate base templates
- [ ] Ensure ALL templates extend "base.html" directly
- [ ] Move global templates to proper locations
- [ ] Remove shared/ template references
- [ ] Update template block structure compliance

### Navigation Compliance ✅ TODO  
- [ ] Implement EXACT two-tier navigation system
- [ ] Remove complex navigation hierarchies
- [ ] Ensure global navigation always visible
- [ ] Make app navigation truly subordinate

### Directory Structure ✅ TODO
- [ ] Remove unauthorized shared/ directory references
- [ ] Consolidate templates in FamilyHub/apps/ only
- [ ] Clean up standalone-apps duplicates
- [ ] Ensure single source of truth for templates

### Settings Compliance ✅ TODO
- [ ] Fix TEMPLATES['DIRS'] to architecture specification
- [ ] Clean up context processors
- [ ] Ensure proper INSTALLED_APPS structure
- [ ] Remove temporary workarounds

## 🎯 TARGET ARCHITECTURE

### EXACT Template Hierarchy (ENFORCED)
```
FamilyHub/templates/base.html (MASTER - all pages extend from this)
    └── All app templates extend directly from base.html
```

### EXACT Directory Structure (ENFORCED)
```
family-hub-workspace/
├── FamilyHub/                    # Main hub
│   ├── FamilyHub/               # Settings directory  
│   ├── home/                    # Dashboard app
│   ├── apps/                    # Integrated apps ONLY
│   │   └── timesheet_app/
│   │       └── templates/       # App templates extend base.html DIRECTLY
│   ├── templates/               # Global templates ONLY (base.html, etc.)
│   ├── static/                  # Global static ONLY
│   └── manage.py                # Single manage.py
└── standalone-apps/             # Standalone versions (DO NOT integrate directly)
```

### EXACT Navigation (ENFORCED)
```
Tier 1 - Global Navigation (ALWAYS VISIBLE):
- FamilyHub logo/brand (links to dashboard)
- App switcher (shows all available apps)  
- User menu (profile, logout)

Tier 2 - App Navigation (CONTEXTUAL):
- ONLY visible when inside an app
- App-specific menu items
- NEVER replaces global navigation
```

## 🚀 EXECUTION PLAN

1. **IMMEDIATE**: Remove all architecture violations
2. **SYSTEMATIC**: Implement exact architecture compliance
3. **VERIFY**: Test all functionality after restructuring
4. **DOCUMENT**: Update all references to match new structure

---

**STATUS**: 🔄 IN PROGRESS
**PRIORITY**: 🚨 CRITICAL - Architecture compliance required
**TIMELINE**: Complete restructuring in this session
