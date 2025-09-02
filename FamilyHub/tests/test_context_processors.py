#!/usr/bin/env python
"""
Test script to verify context processors are working correctly
for both standalone and integrated modes.
"""

import os
import sys
import django
from django.conf import settings
from django.test import RequestFactory
from django.http import HttpRequest

def test_context_processors():
    print("=" * 60)
    print("TESTING CONTEXT PROCESSORS")
    print("=" * 60)
    
    # Test FamilyHub (Integrated Mode)
    print("\n1. Testing FamilyHub (Integrated Mode)")
    print("-" * 40)
    
    # Set up FamilyHub environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyHub.settings.development')
    django.setup()
    
    from apps.timesheet_app.context_processors import integration_context
    
    # Create a mock request
    factory = RequestFactory()
    request = factory.get('/')
    
    # Test the context processor
    context = integration_context(request)
    print(f"FamilyHub Context: {context}")
    print(f"integrated_mode: {context.get('integrated_mode')}")
    print(f"standalone_mode: {context.get('standalone_mode')}")
    
    # Test Standalone Mode
    print("\n2. Testing Standalone Mode")
    print("-" * 40)
    
    # Clear Django setup
    django.apps.apps.clear_cache()
    
    # Set up standalone environment
    standalone_path = os.path.join(os.path.dirname(__file__), 'standalone-apps', 'timesheet')
    sys.path.insert(0, standalone_path)
    
    os.environ['DJANGO_SETTINGS_MODULE'] = 'timesheet_project.settings'
    
    # Import and test standalone context processor
    try:
        from timesheet_app.context_processors import integration_context as standalone_context
        
        context = standalone_context(request)
        print(f"Standalone Context: {context}")
        print(f"integrated_mode: {context.get('integrated_mode')}")
        print(f"standalone_mode: {context.get('standalone_mode')}")
        
    except Exception as e:
        print(f"Error testing standalone context: {e}")
    
    print("\n" + "=" * 60)
    print("CONTEXT PROCESSOR TESTS COMPLETE")
    print("=" * 60)

if __name__ == '__main__':
    # Change to FamilyHub directory
    familyhub_path = os.path.join(os.path.dirname(__file__), 'FamilyHub')
    os.chdir(familyhub_path)
    
    test_context_processors()
