#!/usr/bin/env python
"""
Test script to verify app settings configuration
Tests deployment detection and context in both standalone and integrated modes
"""

import os
import sys
import django
from django.conf import settings as django_settings

def test_standalone_settings():
    """Test app settings in standalone deployment"""
    print("=== Testing Standalone Deployment ===")
    
    # Set up Django for standalone project
    os.chdir(r'c:\Users\Dmitry\OneDrive\Development\myprojects\family-hub-workspace\standalone-apps\timesheet')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timesheet_project.settings')
    
    # Configure Django
    django.setup()
    
    # Import and test app settings
    sys.path.insert(0, r'c:\Users\Dmitry\OneDrive\Development\myprojects\family-hub-workspace\shared\apps')
    from timesheet.app_settings import get_timesheet_settings
    
    settings = get_timesheet_settings()
    
    print(f"Deployment Context: {settings.deployment_context}")
    print(f"Is Standalone: {settings.is_standalone}")
    print(f"Is Integrated: {settings.is_integrated}")
    print(f"Base Template: {settings.base_template}")
    print(f"App Title: {settings.app_title}")
    print(f"App Description: {settings.app_description}")
    print(f"Pagination Per Page: {settings.pagination_per_page}")
    print(f"Dashboard Widgets: {settings.dashboard_widgets}")
    print(f"Breadcrumb Home: {settings.breadcrumb_home}")
    print(f"Navigation Items: {len(settings.navigation_items)} items")
    print()

def test_integrated_settings():
    """Test app settings in FamilyHub integrated deployment"""
    print("=== Testing FamilyHub Integration ===")
    
    # Note: This would need a separate Python process to properly test
    # For now, we'll simulate by checking the detection logic
    print("(Note: Full integration test requires separate process)")
    print("Simulating FamilyHub context...")
    
    # We can test the logic directly
    sys.path.insert(0, r'c:\Users\Dmitry\OneDrive\Development\myprojects\family-hub-workspace\shared\apps')
    from timesheet.app_settings import TimesheetSettings
    
    # Create a settings instance and manually test detection
    settings = TimesheetSettings()
    print(f"Current Detection Result: {settings._deployment_context}")
    print()

if __name__ == '__main__':
    try:
        print("Timesheet App Settings Test")
        print("=" * 50)
        
        # Test standalone
        test_standalone_settings()
        
        # Test integrated simulation
        test_integrated_settings()
        
        print("✅ Tests completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
