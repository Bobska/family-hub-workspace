#!/usr/bin/env python
"""
App Registry Diagnostic Script
"""
import os
import sys
import django
from pathlib import Path

# Setup Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyHub.settings.development')
django.setup()

from FamilyHub.app_registry import app_registry

def main():
    print("=== FAMILYHUB APP REGISTRY DIAGNOSTIC ===\n")
    
    statuses = app_registry.get_all_app_statuses()
    
    for app_key, status in statuses.items():
        print(f"📱 {app_key.upper()}:")
        print(f"  Status: {status['status']}")
        print(f"  Available: {status['available']}")
        print(f"  Mode: {status['mode']}")
        print(f"  Integrated exists: {status['integrated_exists']}")
        print(f"  Standalone exists: {status['standalone_exists']}")
        print(f"  URLs available: {status['urls_available']}")
        print()
    
    print("🔗 Available app URLs:")
    app_urls = app_registry.get_app_urls()
    for pattern, include_path, namespace in app_urls:
        print(f"  {pattern} -> {include_path} (namespace: {namespace})")
    
    print("\n📦 Django app names:")
    django_apps = app_registry.get_django_app_names()
    for app in django_apps:
        print(f"  {app}")

if __name__ == "__main__":
    main()
