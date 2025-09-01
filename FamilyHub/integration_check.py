#!/usr/bin/env python3
"""
Comprehensive Integration Status Check
"""
import os
import sys
from pathlib import Path

# Add the FamilyHub directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from FamilyHub.app_registry import app_registry
    
    print("=== APP INTEGRATION STATUS ===")
    statuses = app_registry.get_all_app_statuses()
    
    for app_key, status in statuses.items():
        print(f"App: {app_key}")
        print(f"  Available: {status['available']}")
        print(f"  Status: {status['status']}")
        print(f"  Mode: {status['mode']}")
        print(f"  URLs Available: {status['urls_available']}")
        print(f"  Integrated Exists: {status['integrated_exists']}")
        print(f"  Standalone Exists: {status['standalone_exists']}")
        print()
    
    print("=== DJANGO INSTALLED APPS ===")
    from FamilyHub.app_registry import get_dynamic_installed_apps
    apps = get_dynamic_installed_apps()
    for app in apps:
        print(f"  - {app}")
    
    print("\n=== PYTHON PATH ===")
    for path in sys.path[:5]:  # Show first 5 paths
        print(f"  - {path}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
