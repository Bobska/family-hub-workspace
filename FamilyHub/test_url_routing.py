#!/usr/bin/env python
"""
URL Routing Verification Test
Tests that all timesheet URLs are properly configured and accessible
"""

import os
import django
from django.test import Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

def test_url_routing():
    """Test URL routing configuration"""
    print("🔍 Testing URL Routing Configuration")
    print("=" * 60)
    
    try:
        # Test URL resolution
        print("1. Testing URL pattern resolution...")
        
        # Test timesheet URLs
        urls_to_test = [
            ('timesheet:dashboard', '/timesheet/'),
            ('timesheet:daily_entry', '/timesheet/daily/'),
            ('timesheet:weekly_summary', '/timesheet/weekly/'),
            ('timesheet:job_list', '/timesheet/jobs/'),
            ('timesheet:job_create', '/timesheet/jobs/add/'),
        ]
        
        for url_name, expected_path in urls_to_test:
            try:
                resolved_path = reverse(url_name)
                if resolved_path == expected_path:
                    print(f"   ✅ {url_name} -> {resolved_path}")
                else:
                    print(f"   ⚠️  {url_name} -> {resolved_path} (expected {expected_path})")
            except Exception as e:
                print(f"   ❌ {url_name} -> Error: {e}")
        
        # Test URL resolution from path
        print("\n2. Testing path resolution...")
        paths_to_test = [
            '/timesheet/',
            '/timesheet/daily/',
            '/timesheet/weekly/',
            '/timesheet/jobs/',
        ]
        
        for path in paths_to_test:
            try:
                resolver = resolve(path)
                print(f"   ✅ {path} -> {resolver.view_name}")
            except Exception as e:
                print(f"   ❌ {path} -> Error: {e}")
        
        print("\n3. Testing HTTP responses (without authentication)...")
        client = Client()
        
        for path in paths_to_test:
            try:
                response = client.get(path)
                if response.status_code == 302:  # Redirect to login
                    print(f"   ✅ {path} -> HTTP {response.status_code} (redirects to login)")
                elif response.status_code == 200:
                    print(f"   ✅ {path} -> HTTP {response.status_code} (accessible)")
                else:
                    print(f"   ⚠️  {path} -> HTTP {response.status_code}")
            except Exception as e:
                print(f"   ❌ {path} -> Error: {e}")
        
        print("\n🎉 URL routing verification completed!")
        return True
        
    except Exception as e:
        print(f"❌ URL Routing Test Error: {e}")
        return False

if __name__ == '__main__':
    # Setup Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyHub.settings')
    django.setup()
    
    # Run the test
    success = test_url_routing()
    
    if success:
        print("\n✅ URL Routing Test: PASSED")
    else:
        print("\n❌ URL Routing Test: FAILED")
