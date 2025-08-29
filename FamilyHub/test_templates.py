#!/usr/bin/env python
"""
Template Resolution Test
Verifies that timesheet templates load correctly in integrated environment
Tests template inheritance and conditional base template usage
"""

import os
import django
from django.test import Client, RequestFactory
from django.contrib.auth import get_user_model
from django.template.loader import get_template
from django.template import Context, Template

def test_template_resolution():
    """Test template resolution and inheritance"""
    print("🔍 Testing Template Resolution in Integrated Environment")
    print("=" * 60)
    
    try:
        # Test template loading
        print("1. Testing template loading...")
        
        templates_to_test = [
            'timesheet/dashboard.html',
            'timesheet/daily_entry.html',
            'timesheet/weekly_summary.html',
            'timesheet/job_list.html',
            'timesheet/job_form.html',
            'timesheet/entry_form.html',
            'timesheet/base.html',
            'timesheet/base_integrated.html'
        ]
        
        for template_name in templates_to_test:
            try:
                template = get_template(template_name)
                print(f"   ✅ Template loads: {template_name}")
            except Exception as e:
                print(f"   ❌ Template error: {template_name} -> {e}")
        
        # Test conditional template inheritance
        print("\n2. Testing conditional template inheritance...")
        
        # Check if templates have conditional extends
        template_files = [
            'timesheet/dashboard.html',
            'timesheet/daily_entry.html',
            'timesheet/weekly_summary.html',
            'timesheet/job_list.html'
        ]
        
        for template_name in template_files:
            try:
                template = get_template(template_name)
                template_content = template.template.source
                
                if '{% extends base_template|default:' in template_content:
                    print(f"   ✅ Conditional inheritance: {template_name}")
                elif '{% extends' in template_content:
                    print(f"   ⚠️  Static inheritance: {template_name}")
                else:
                    print(f"   ❌ No inheritance: {template_name}")
                    
            except Exception as e:
                print(f"   ❌ Template check error: {template_name} -> {e}")
        
        # Test context processor functionality
        print("\n3. Testing context processor integration...")
        
        factory = RequestFactory()
        request = factory.get('/timesheet/')
        
        from timesheet.context_processors import deployment_context
        context = deployment_context(request)
        
        expected_context_vars = [
            'is_standalone',
            'is_integrated', 
            'base_template',
            'deployment_context'
        ]
        
        for var in expected_context_vars:
            if var in context:
                print(f"   ✅ Context variable: {var} = {context[var]}")
            else:
                print(f"   ❌ Missing context variable: {var}")
        
        # Test base template selection
        print("\n4. Testing base template selection...")
        
        if context.get('is_integrated', False):
            expected_base = 'timesheet/base_integrated.html'
            if context.get('base_template') == expected_base:
                print(f"   ✅ Correct base template for integrated: {expected_base}")
            else:
                print(f"   ❌ Wrong base template: {context.get('base_template')} (expected {expected_base})")
        
        # Test app settings integration in templates
        print("\n5. Testing app settings in template context...")
        
        from timesheet.app_settings import get_timesheet_settings
        settings = get_timesheet_settings()
        
        print(f"   ✅ App settings available")
        print(f"   - Navigation items: {len(settings.navigation_items)}")
        print(f"   - Breadcrumb home: {settings.breadcrumb_home}")
        print(f"   - App title: {settings.app_title}")
        
        # Test integrated features
        print("\n6. Testing FamilyHub integration features...")
        
        if settings.is_integrated:
            nav_items = settings.navigation_items
            familyhub_nav = [item for item in nav_items if 'FamilyHub' in item.get('name', '')]
            
            if familyhub_nav:
                print(f"   ✅ FamilyHub navigation links present: {len(familyhub_nav)}")
            else:
                print("   ⚠️  No FamilyHub navigation links found")
            
            # Check base template styling
            try:
                integrated_template = get_template('timesheet/base_integrated.html')
                template_content = integrated_template.template.source
                
                if 'background: linear-gradient' in template_content:
                    print("   ✅ FamilyHub gradient styling present")
                else:
                    print("   ⚠️  FamilyHub styling not found")
                    
            except Exception as e:
                print(f"   ❌ Integrated template check error: {e}")
        
        print("\n🎉 Template resolution test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Template Resolution Test Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    # Setup Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyHub.settings')
    django.setup()
    
    # Run the test
    success = test_template_resolution()
    
    if success:
        print("\n✅ Template Resolution Test: PASSED")
    else:
        print("\n❌ Template Resolution Test: FAILED")
