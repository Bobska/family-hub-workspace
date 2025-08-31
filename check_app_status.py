#!/usr/bin/env python
import os
import sys
import django

# Add the FamilyHub directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'FamilyHub'))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyHub.settings.development')
django.setup()

from FamilyHub.app_registry import app_registry

def check_app_statuses():
    """Check the status of all apps in the registry."""
    print("=== FamilyHub App Registry Status ===\n")
    
    statuses = app_registry.get_all_app_statuses()
    
    for app_key, status in statuses.items():
        print(f"App: {app_key}")
        print(f"  Status: {status['status']}")
        print(f"  Available: {status['available']}")
        print(f"  Mode: {status.get('mode', 'unknown')}")
        
        if app_key == 'timesheet':
            print(f"  === TIMESHEET DETAILS ===")
            print(f"  Integrated path: {status['integrated_path']}")
            print(f"  Standalone path: {status['standalone_path']}")
            print(f"  Integrated exists: {status['integrated_exists']}")
            print(f"  Standalone exists: {status['standalone_exists']}")
            print(f"  URLs available: {status.get('urls_available', False)}")
        print()

if __name__ == "__main__":
    check_app_statuses()
