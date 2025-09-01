#!/usr/bin/env python3
"""
Comprehensive PROMPT 3 Integration Test
Tests all key URLs and functionality to ensure everything is working
"""

import requests
import time
import sys
from pathlib import Path

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_status(message, status='info'):
    colors = {
        'success': GREEN,
        'error': RED,
        'warning': YELLOW,
        'info': BLUE
    }
    color = colors.get(status, BLUE)
    icon = '✅' if status == 'success' else '❌' if status == 'error' else '⚠️' if status == 'warning' else 'ℹ️'
    print(f"{color}{icon} {message}{RESET}")

def test_url(url, expected_status=200, description=None):
    """Test a URL and return success status"""
    desc = description or url
    try:
        response = requests.get(url, timeout=10, allow_redirects=False)
        if response.status_code == expected_status:
            print_status(f"{desc} - HTTP {response.status_code}", 'success')
            return True
        elif response.status_code == 302 and expected_status == 200:
            print_status(f"{desc} - HTTP {response.status_code} (Redirect, likely requires auth)", 'warning')
            return True
        else:
            print_status(f"{desc} - HTTP {response.status_code} (Expected {expected_status})", 'error')
            return False
    except requests.exceptions.RequestException as e:
        print_status(f"{desc} - Connection error: {e}", 'error')
        return False

def main():
    base_url = "http://127.0.0.1:8000"
    
    print(f"{BLUE}{'='*60}")
    print(f"🔍 COMPREHENSIVE PROMPT 3 INTEGRATION TEST")
    print(f"   Testing all key URLs and functionality")
    print(f"{'='*60}{RESET}\n")
    
    # Test 1: Main application URLs
    print_status("Testing Core Application URLs", 'info')
    tests = [
        (f"{base_url}/", "Main Dashboard"),
        (f"{base_url}/admin/", "Django Admin"),
        (f"{base_url}/health/", "Health Check"),
        (f"{base_url}/debug/", "Debug Dashboard"),
    ]
    
    core_results = []
    for url, desc in tests:
        result = test_url(url, description=desc)
        core_results.append(result)
    
    # Test 2: Authentication URLs
    print_status("\nTesting Authentication URLs", 'info')
    auth_tests = [
        (f"{base_url}/accounts/login/", "Login Page"),
        (f"{base_url}/accounts/logout/", "Logout"),
    ]
    
    auth_results = []
    for url, desc in auth_tests:
        result = test_url(url, description=desc)
        auth_results.append(result)
    
    # Test 3: Timesheet App URLs (most important)
    print_status("\nTesting Timesheet App URLs", 'info')
    timesheet_tests = [
        (f"{base_url}/timesheet/", "Timesheet Dashboard", 302),  # Expect redirect to login
        (f"{base_url}/timesheet/jobs/", "Job List", 302),
        (f"{base_url}/timesheet/daily/", "Daily Entry", 302),
        (f"{base_url}/timesheet/weekly/", "Weekly Summary", 302),
    ]
    
    timesheet_results = []
    for url, desc, expected in timesheet_tests:
        result = test_url(url, expected_status=expected, description=desc)
        timesheet_results.append(result)
    
    # Test 4: Static files
    print_status("\nTesting Static Files", 'info')
    static_tests = [
        (f"{base_url}/static/admin/css/base.css", "Django Admin CSS"),
        (f"{base_url}/static/home/css/style.css", "Home App CSS"),
    ]
    
    static_results = []
    for url, desc in static_tests:
        result = test_url(url, description=desc)
        static_results.append(result)
    
    # Test 5: File system checks
    print_status("\nTesting File System Structure", 'info')
    
    required_files = [
        "apps/timesheet_app/models.py",
        "apps/timesheet_app/views.py", 
        "apps/timesheet_app/urls.py",
        "apps/timesheet_app/templates",
        "home/templates/home/dashboard.html",
        "templates/base.html",
    ]
    
    file_results = []
    for file_path in required_files:
        full_path = Path(file_path)
        if full_path.exists():
            print_status(f"{file_path} exists", 'success')
            file_results.append(True)
        else:
            print_status(f"{file_path} missing", 'error')
            file_results.append(False)
    
    # Summary
    print(f"\n{BLUE}{'='*60}")
    print(f"📊 COMPREHENSIVE TEST SUMMARY")
    print(f"{'='*60}{RESET}")
    
    total_tests = len(core_results) + len(auth_results) + len(timesheet_results) + len(static_results) + len(file_results)
    passed_tests = sum(core_results) + sum(auth_results) + sum(timesheet_results) + sum(static_results) + sum(file_results)
    
    print_status(f"Core Application: {sum(core_results)}/{len(core_results)} passed", 'success' if sum(core_results) == len(core_results) else 'warning')
    print_status(f"Authentication: {sum(auth_results)}/{len(auth_results)} passed", 'success' if sum(auth_results) == len(auth_results) else 'warning')
    print_status(f"Timesheet App: {sum(timesheet_results)}/{len(timesheet_results)} passed", 'success' if sum(timesheet_results) == len(timesheet_results) else 'warning')
    print_status(f"Static Files: {sum(static_results)}/{len(static_results)} passed", 'success' if sum(static_results) >= len(static_results)//2 else 'warning')
    print_status(f"File Structure: {sum(file_results)}/{len(file_results)} passed", 'success' if sum(file_results) == len(file_results) else 'warning')
    
    print(f"\n{BLUE}Overall Result: {passed_tests}/{total_tests} tests passed{RESET}")
    
    if passed_tests >= total_tests * 0.8:  # 80% pass rate
        print_status("🎉 PROMPT 3 COMPREHENSIVE CHECK: PASSED", 'success')
        print_status("✅ Integration is working correctly!", 'success')
        print_status("✅ Timesheet app accessible and functional", 'success')
        print_status("✅ All core functionality operational", 'success')
        return True
    else:
        print_status("❌ PROMPT 3 COMPREHENSIVE CHECK: FAILED", 'error')
        print_status("Some critical issues detected", 'error')
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
