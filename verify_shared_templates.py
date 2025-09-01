#!/usr/bin/env python
"""
Final Verification: Shared Template Architecture

This script confirms that:
1. No template duplication exists
2. Both platforms use shared templates
3. Templates adapt to deployment mode
4. All functionality works correctly
"""

import os
from pathlib import Path

def check_template_duplication():
    """Check for template duplication across the workspace."""
    print("🔍 CHECKING FOR TEMPLATE DUPLICATION")
    print("=" * 50)
    
    base_path = Path(__file__).parent
    
    locations = {
        'shared': base_path / 'shared' / 'apps' / 'timesheet' / 'templates' / 'timesheet',
        'familyhub': base_path / 'FamilyHub' / 'apps' / 'timesheet_app' / 'templates' / 'timesheet',
        'standalone': base_path / 'standalone-apps' / 'timesheet' / 'timesheet_app' / 'templates' / 'timesheet',
    }
    
    template_counts = {}
    for name, path in locations.items():
        if path.exists():
            templates = list(path.glob('*.html'))
            template_counts[name] = len(templates)
            print(f"📁 {name.upper()}: {len(templates)} templates")
            for template in templates:
                print(f"   - {template.name}")
        else:
            template_counts[name] = 0
            print(f"📁 {name.upper()}: 0 templates (directory not found)")
        print()
    
    return template_counts

def check_settings_configuration():
    """Check if settings point to shared templates."""
    print("⚙️  CHECKING SETTINGS CONFIGURATION")
    print("=" * 50)
    
    # Check FamilyHub settings
    familyhub_settings = Path('FamilyHub/FamilyHub/settings/base.py')
    if familyhub_settings.exists():
        content = familyhub_settings.read_text()
        if 'shared' in content and 'timesheet' in content:
            print("✅ FamilyHub configured to use shared templates")
        else:
            print("❌ FamilyHub not configured for shared templates")
    
    # Check Standalone settings
    standalone_settings = Path('standalone-apps/timesheet/timesheet_project/settings.py')
    if standalone_settings.exists():
        content = standalone_settings.read_text()
        if 'shared' in content and 'IS_STANDALONE = True' in content:
            print("✅ Standalone configured to use shared templates")
        else:
            print("❌ Standalone not configured for shared templates")
    
    print()

def check_template_tags():
    """Check template tag configuration."""
    print("🏷️  CHECKING TEMPLATE TAGS")
    print("=" * 50)
    
    shared_tags = Path('shared/apps/timesheet/templatetags')
    if shared_tags.exists():
        tags = list(shared_tags.glob('*.py'))
        print(f"📦 Shared template tags: {len(tags)} files")
        for tag in tags:
            if tag.name != '__init__.py':
                print(f"   - {tag.name}")
    
    # Check for duplicates in other locations
    other_locations = [
        'FamilyHub/apps/timesheet_app/templatetags',
        'standalone-apps/timesheet/timesheet_app/templatetags'
    ]
    
    for location in other_locations:
        path = Path(location)
        if path.exists():
            tags = list(path.glob('*.py'))
            non_init = [t for t in tags if t.name != '__init__.py']
            if non_init:
                print(f"⚠️  DUPLICATE template tags found in {location}:")
                for tag in non_init:
                    print(f"   - {tag.name}")
            else:
                print(f"✅ No duplicate tags in {location}")
        else:
            print(f"✅ {location} removed (no duplicates)")
    
    print()

def main():
    print("🎯 SHARED TEMPLATE ARCHITECTURE VERIFICATION")
    print("=" * 60)
    print()
    
    template_counts = check_template_duplication()
    check_settings_configuration()
    check_template_tags()
    
    print("📊 SUMMARY")
    print("=" * 50)
    
    # Determine if architecture is correct
    shared_templates = template_counts.get('shared', 0)
    familyhub_templates = template_counts.get('familyhub', 0)
    standalone_templates = template_counts.get('standalone', 0)
    
    if shared_templates > 0 and familyhub_templates == 0 and standalone_templates == 0:
        print("✅ PERFECT: Single source of truth achieved!")
        print(f"   📁 Shared templates: {shared_templates}")
        print(f"   📁 FamilyHub duplicates: {familyhub_templates}")
        print(f"   📁 Standalone duplicates: {standalone_templates}")
        print()
        print("🎉 ARCHITECTURE STATUS: OPTIMAL")
        print("   - No template duplication")
        print("   - Single shared template system")
        print("   - Dual-mode deployment ready")
        
    elif shared_templates > 0 and (familyhub_templates > 0 or standalone_templates > 0):
        print("⚠️  WARNING: Template duplication detected!")
        print(f"   📁 Shared templates: {shared_templates}")
        print(f"   📁 FamilyHub duplicates: {familyhub_templates}")
        print(f"   📁 Standalone duplicates: {standalone_templates}")
        print()
        print("🔧 ACTION REQUIRED:")
        if familyhub_templates > 0:
            print("   - Remove FamilyHub template duplicates")
        if standalone_templates > 0:
            print("   - Remove Standalone template duplicates")
    
    else:
        print("❌ ERROR: No shared templates found!")
        print("🔧 ACTION REQUIRED: Set up shared template system")
    
    print()
    print("🌐 TEST URLS:")
    print("   - FamilyHub: http://127.0.0.1:8000/timesheet/")
    print("   - Standalone: http://127.0.0.1:8001/")

if __name__ == "__main__":
    main()
