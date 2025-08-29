#!/usr/bin/env python
"""
Test Python Path Integration for FamilyHub Timesheet App
Verifies that shared timesheet app can be imported correctly in FamilyHub context
"""

import os
import sys
import django
from django.conf import settings

def test_timesheet_imports():
    """Test importing timesheet app models and components"""
    print("🔍 Testing Timesheet App Python Path Integration")
    print("=" * 60)
    
    try:
        # Test importing models
        print("1. Testing model imports...")
        from timesheet.models import Job, TimeEntry
        print("   ✅ Successfully imported Job and TimeEntry models")
        
        # Test importing forms
        print("2. Testing form imports...")
        from timesheet.forms import JobForm, TimeEntryForm, QuickTimeEntryForm
        print("   ✅ Successfully imported timesheet forms")
        
        # Test importing views
        print("3. Testing view imports...")
        from timesheet import views
        print("   ✅ Successfully imported timesheet views")
        
        # Test importing app settings
        print("4. Testing app settings imports...")
        from timesheet.app_settings import get_timesheet_settings
        settings_obj = get_timesheet_settings()
        print(f"   ✅ App settings loaded - Deployment context: {settings_obj.deployment_context}")
        
        # Test context processor
        print("5. Testing context processor...")
        from timesheet.context_processors import deployment_context
        print("   ✅ Successfully imported context processor")
        
        # Verify deployment detection
        print("6. Testing deployment detection...")
        print(f"   - Is Standalone: {settings_obj.is_standalone}")
        print(f"   - Is Integrated: {settings_obj.is_integrated}")
        print(f"   - Base Template: {settings_obj.base_template}")
        
        print("\n🎉 All imports successful! Python path integration working correctly.")
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

if __name__ == '__main__':
    # Setup Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyHub.settings')
    django.setup()
    
    # Run the test
    success = test_timesheet_imports()
    
    if success:
        print("\n✅ Python Path Integration Test: PASSED")
    else:
        print("\n❌ Python Path Integration Test: FAILED")
        sys.exit(1)
