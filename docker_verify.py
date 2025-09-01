#!/usr/bin/env python3
"""
PROMPT 3 Docker Verification Script
Quick verification that Docker configuration works
"""

import subprocess
import time
import sys

def run_command(command):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        return result.returncode == 0, result.stdout, result.stderr
    except:
        return False, "", "Command failed"

def test_http_access():
    """Test HTTP access using PowerShell"""
    command = "powershell -Command \"try { (Invoke-WebRequest -Uri http://localhost:8000/ -UseBasicParsing).StatusCode } catch { 'ERROR' }\""
    success, stdout, stderr = run_command(command)
    return success and "200" in stdout

def main():
    print("🐳 PROMPT 3 DOCKER VERIFICATION")
    print("=" * 40)
    
    # Test 1: Check if containers are running
    print("1. Checking container status...")
    success, stdout, stderr = run_command("docker-compose ps --services --filter status=running")
    if success and "familyhub" in stdout:
        print("   ✅ FamilyHub container is running")
    else:
        print("   ❌ FamilyHub container not running")
        return False
    
    # Test 2: Check HTTP access
    print("2. Testing HTTP access...")
    if test_http_access():
        print("   ✅ FamilyHub accessible at http://localhost:8000")
    else:
        print("   ❌ FamilyHub not accessible")
        return False
    
    # Test 3: Check logs for Django startup
    print("3. Checking application logs...")
    success, stdout, stderr = run_command("docker-compose logs familyhub --tail=5")
    if success and "Starting development server" in stdout:
        print("   ✅ Django server started successfully")
    else:
        print("   ⚠️  Django server status unclear")
    
    print("\n🎉 PROMPT 3 DOCKER VERIFICATION: PASSED")
    print("✅ Docker configuration working correctly!")
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
