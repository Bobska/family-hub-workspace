"""
Test script to validate timesheet integration setup.
"""

import os
import sys
from pathlib import Path

# Add Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyHub.settings.development')

# Add FamilyHub to path
familyhub_path = Path(__file__).parent / 'FamilyHub'
sys.path.insert(0, str(familyhub_path))

try:
    # Setup Django
    import django
    django.setup()
    
    # Test timesheet integration
    print("Testing timesheet app integration...")
    
    # Test URL imports
    from django.urls import reverse
    print("✓ Django URLs imported successfully")
    
    # Test if timesheet app is accessible
    try:
        import timesheet_app
        print("✓ timesheet_app module imported successfully")
    except ImportError as e:
        print(f"⚠ timesheet_app import issue: {e}")
    
    # Test URL resolution
    try:
        timesheet_dashboard_url = reverse('timesheet:dashboard')
        print(f"✓ Timesheet dashboard URL resolved: {timesheet_dashboard_url}")
    except Exception as e:
        print(f"⚠ URL resolution issue: {e}")
    
    # Test context processor
    try:
        from apps.timesheet_integration import timesheet_context_processor
        context = timesheet_context_processor(None)
        print(f"✓ Context processor working: {context}")
    except Exception as e:
        print(f"⚠ Context processor issue: {e}")
    
    print("\nIntegration test completed!")
    
except Exception as e:
    print(f"Integration test failed: {e}")
    import traceback
    traceback.print_exc()
