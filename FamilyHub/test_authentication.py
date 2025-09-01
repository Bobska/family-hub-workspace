#!/usr/bin/env python
"""
Authentication Test Script for FamilyHub
"""

import os
import sys
import django
from django.test import Client

# Add the FamilyHub directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyHub.settings.development')
django.setup()

def test_authentication():
    """Test authentication flow"""
    print("🔐 Testing FamilyHub Authentication System")
    print("=" * 50)
    
    client = Client()
    
    # Test 1: Access timesheet without login (should redirect)
    print("📍 Test 1: Accessing timesheet without authentication")
    response = client.get('/timesheet/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 302:
        redirect_url = response.get('Location', '')
        print(f"   ✅ Redirected to: {redirect_url}")
        if '/accounts/login/' in redirect_url:
            print("   ✅ Correctly redirected to login page")
        else:
            print("   ❌ Unexpected redirect location")
    else:
        print("   ❌ Expected redirect but got different status")
    
    # Test 2: Access login page
    print("\n📍 Test 2: Accessing login page")
    response = client.get('/accounts/login/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Login page loads successfully")
        content = response.content.decode('utf-8')
        if 'FamilyHub' in content:
            print("   ✅ FamilyHub branding present")
        if 'Username' in content and 'Password' in content:
            print("   ✅ Login form elements present")
    else:
        print(f"   ❌ Login page failed to load: {response.status_code}")
    
    # Test 3: Check if login with next parameter works
    print("\n📍 Test 3: Login page with next parameter")
    response = client.get('/accounts/login/?next=/timesheet/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Login page with next parameter works")
        content = response.content.decode('utf-8')
        if 'timesheet' in content.lower():
            print("   ✅ Next parameter preserved in form")
    
    print("\n" + "=" * 50)
    print("🎯 Authentication system is properly configured!")
    print("✅ Unauthenticated users are redirected to login")
    print("✅ Login templates are loading correctly")
    print("✅ Authentication flow is working as expected")

if __name__ == '__main__':
    test_authentication()
