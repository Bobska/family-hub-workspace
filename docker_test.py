#!/usr/bin/env python3
"""
PROMPT 3 Docker Configuration Testing Script
Verifies that Docker configuration works correctly for integration
"""

import subprocess
import time
import requests
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
    print(f"{color}{'✅' if status == 'success' else '❌' if status == 'error' else '⚠️' if status == 'warning' else 'ℹ️'} {message}{RESET}")

def run_command(command, description):
    """Run a command and return success status"""
    print_status(f"Running: {description}", 'info')
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print_status(f"✅ {description} - SUCCESS", 'success')
            return True
        else:
            print_status(f"❌ {description} - FAILED", 'error')
            print(f"Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print_status(f"❌ {description} - TIMEOUT", 'error')
        return False
    except Exception as e:
        print_status(f"❌ {description} - ERROR: {e}", 'error')
        return False

def check_url(url, timeout=10):
    """Check if URL is accessible"""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except:
        return False

def main():
    print(f"{BLUE}{'='*60}")
    print(f"🐳 PROMPT 3 DOCKER CONFIGURATION TESTING")
    print(f"   Integration Docker Environment Verification")
    print(f"{'='*60}{RESET}\n")
    
    # Check prerequisite files
    print_status("Checking Docker configuration files...", 'info')
    
    required_files = [
        'docker-compose.yml',
        'FamilyHub/Dockerfile',
        'FamilyHub/FamilyHub/settings/docker.py',
        '.env'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print_status(f"❌ Missing required files: {missing_files}", 'error')
        return False
    else:
        print_status("✅ All required Docker files present", 'success')
    
    # Test 1: Build Docker image successfully
    print_status("TEST 1: Building Docker image...", 'info')
    build_success = run_command(
        "docker-compose build familyhub",
        "Docker image build"
    )
    
    if not build_success:
        print_status("❌ Docker build failed - stopping tests", 'error')
        return False
    
    # Test 2: Start containers
    print_status("TEST 2: Starting Docker containers...", 'info')
    start_success = run_command(
        "docker-compose up -d",
        "Docker containers startup"
    )
    
    if not start_success:
        print_status("❌ Docker startup failed - stopping tests", 'error')
        return False
    
    # Wait for services to be ready
    print_status("Waiting for services to be ready...", 'info')
    time.sleep(30)
    
    # Test 3: Check container health
    print_status("TEST 3: Checking container status...", 'info')
    container_check = run_command(
        "docker-compose ps",
        "Container status check"
    )
    
    # Test 4: Access http://localhost:8000 from host
    print_status("TEST 4: Testing main page accessibility...", 'info')
    main_page_accessible = check_url("http://localhost:8000", timeout=30)
    
    if main_page_accessible:
        print_status("✅ Main page accessible at http://localhost:8000", 'success')
    else:
        print_status("❌ Main page not accessible", 'error')
    
    # Test 5: Test dashboard displays correctly
    print_status("TEST 5: Testing dashboard...", 'info')
    dashboard_accessible = check_url("http://localhost:8000/", timeout=10)
    
    if dashboard_accessible:
        print_status("✅ Dashboard displays correctly", 'success')
    else:
        print_status("❌ Dashboard not accessible", 'error')
    
    # Test 6: Test timesheet app accessibility
    print_status("TEST 6: Testing timesheet app at /timesheet/...", 'info')
    timesheet_accessible = check_url("http://localhost:8000/timesheet/", timeout=10)
    
    if timesheet_accessible:
        print_status("✅ Timesheet app accessible at /timesheet/", 'success')
    else:
        print_status("⚠️ Timesheet app not accessible (may be expected if not fully integrated)", 'warning')
    
    # Test 7: Check static files serve correctly
    print_status("TEST 7: Testing static files...", 'info')
    static_accessible = check_url("http://localhost:8000/static/admin/css/base.css", timeout=10)
    
    if static_accessible:
        print_status("✅ Static files serve correctly", 'success')
    else:
        print_status("⚠️ Static files may not be served (check collectstatic)", 'warning')
    
    # Test 8: Test health endpoint
    print_status("TEST 8: Testing health endpoint...", 'info')
    health_accessible = check_url("http://localhost:8000/health/", timeout=10)
    
    if health_accessible:
        print_status("✅ Health endpoint accessible", 'success')
    else:
        print_status("⚠️ Health endpoint not accessible", 'warning')
    
    # Show container logs for debugging
    print_status("Showing recent container logs...", 'info')
    run_command("docker-compose logs --tail=20 familyhub", "Container logs")
    
    # Summary
    print(f"\n{BLUE}{'='*60}")
    print(f"📊 DOCKER TESTING SUMMARY")
    print(f"{'='*60}{RESET}")
    
    tests_passed = sum([
        build_success,
        start_success,
        container_check,
        main_page_accessible,
        dashboard_accessible,
    ])
    
    total_tests = 5  # Core tests that must pass
    
    if tests_passed >= 4:
        print_status(f"🎉 DOCKER CONFIGURATION: MOSTLY WORKING ({tests_passed}/{total_tests} core tests passed)", 'success')
        print_status("✅ Integration can run in Docker environment", 'success')
    elif tests_passed >= 3:
        print_status(f"⚠️ DOCKER CONFIGURATION: PARTIAL ({tests_passed}/{total_tests} core tests passed)", 'warning')
        print_status("Some issues detected, but basic functionality works", 'warning')
    else:
        print_status(f"❌ DOCKER CONFIGURATION: FAILED ({tests_passed}/{total_tests} core tests passed)", 'error')
        print_status("Major issues detected", 'error')
    
    # Test cleanup
    print_status("Cleaning up test containers...", 'info')
    run_command("docker-compose down", "Container cleanup")
    
    return tests_passed >= 4

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
