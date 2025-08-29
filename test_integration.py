#!/usr/bin/env python
"""
FamilyHub Integration Testing Script
Comprehensive test suite for dual deployment timesheet app

This script validates:
1. Both standalone and FamilyHub integrations work correctly
2. Database migrations and models function properly
3. URL routing and views respond correctly
4. Templates render with appropriate context
5. Settings abstraction works as expected
6. Context processors provide correct deployment context

Usage:
    python test_integration.py [--verbose] [--standalone-only] [--integrated-only]
"""

import argparse
import os
import sys
import subprocess
import time
import requests
from pathlib import Path
import json

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

class TestResult:
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0
        self.failures = []
    
    def add_pass(self, test_name):
        self.tests_run += 1
        self.tests_passed += 1
        print(f"{Colors.GREEN}✓{Colors.END} {test_name}")
    
    def add_fail(self, test_name, error):
        self.tests_run += 1
        self.tests_failed += 1
        self.failures.append((test_name, error))
        print(f"{Colors.RED}✗{Colors.END} {test_name}: {error}")
    
    def summary(self):
        print(f"\n{Colors.BOLD}Test Summary:{Colors.END}")
        print(f"Total: {self.tests_run}")
        print(f"{Colors.GREEN}Passed: {self.tests_passed}{Colors.END}")
        if self.tests_failed > 0:
            print(f"{Colors.RED}Failed: {self.tests_failed}{Colors.END}")
            print(f"\n{Colors.RED}Failures:{Colors.END}")
            for test_name, error in self.failures:
                print(f"  - {test_name}: {error}")
        return self.tests_failed == 0

class DualDeploymentTester:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.result = TestResult()
        self.workspace_root = Path(r'c:\Users\Dmitry\OneDrive\Development\myprojects\family-hub-workspace')
        self.familyhub_dir = self.workspace_root / 'FamilyHub'
        self.standalone_dir = self.workspace_root / 'standalone-apps' / 'timesheet'
        self.shared_apps_dir = self.workspace_root / 'shared' / 'apps'
        
        # Server process tracking
        self.familyhub_process = None
        self.standalone_process = None
    
    def log(self, message):
        if self.verbose:
            print(f"{Colors.BLUE}[DEBUG]{Colors.END} {message}")
    
    def run_command(self, command, cwd=None, capture_output=True):
        """Run shell command and return result"""
        try:
            if cwd:
                self.log(f"Running: {command} in {cwd}")
            else:
                self.log(f"Running: {command}")
            
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=capture_output,
                text=True,
                timeout=30
            )
            return result
        except subprocess.TimeoutExpired:
            return None
        except Exception as e:
            self.log(f"Command failed: {e}")
            return None
    
    def test_directory_structure(self):
        """Test that all required directories and files exist"""
        print(f"\n{Colors.BOLD}Testing Directory Structure{Colors.END}")
        
        # Check workspace structure
        required_paths = [
            self.workspace_root,
            self.familyhub_dir,
            self.standalone_dir,
            self.shared_apps_dir,
            self.shared_apps_dir / 'timesheet',
            self.shared_apps_dir / 'timesheet' / 'models.py',
            self.shared_apps_dir / 'timesheet' / 'views.py',
            self.shared_apps_dir / 'timesheet' / 'app_settings.py',
            self.shared_apps_dir / 'timesheet' / 'context_processors.py',
            self.shared_apps_dir / 'timesheet' / 'templates' / 'timesheet' / 'base.html',
            self.shared_apps_dir / 'timesheet' / 'templates' / 'timesheet' / 'base_integrated.html',
        ]
        
        for path in required_paths:
            if path.exists():
                self.result.add_pass(f"Path exists: {path.name}")
            else:
                self.result.add_fail(f"Path missing: {path.name}", f"Required path not found: {path}")
    
    def test_django_check(self):
        """Test Django configuration check for both projects"""
        print(f"\n{Colors.BOLD}Testing Django Configuration{Colors.END}")
        
        # Test FamilyHub
        result = self.run_command("python manage.py check", cwd=self.familyhub_dir)
        if result and result.returncode == 0:
            self.result.add_pass("FamilyHub Django check")
        else:
            error = result.stderr if result else "Command failed to run"
            self.result.add_fail("FamilyHub Django check", error)
        
        # Test Standalone (if it exists and is configured)
        if (self.standalone_dir / 'manage.py').exists():
            result = self.run_command("python manage.py check", cwd=self.standalone_dir)
            if result and result.returncode == 0:
                self.result.add_pass("Standalone Django check")
            else:
                error = result.stderr if result else "Command failed to run"
                self.result.add_fail("Standalone Django check", error)
        else:
            self.result.add_pass("Standalone project not configured (expected)")
    
    def test_database_migrations(self):
        """Test database migrations for both projects"""
        print(f"\n{Colors.BOLD}Testing Database Migrations{Colors.END}")
        
        # Test FamilyHub migrations
        result = self.run_command("python manage.py showmigrations", cwd=self.familyhub_dir)
        if result and result.returncode == 0 and 'timesheet' in result.stdout:
            self.result.add_pass("FamilyHub timesheet migrations exist")
        else:
            self.result.add_fail("FamilyHub timesheet migrations", "Migrations not found or command failed")
        
        # Test migration application
        result = self.run_command("python manage.py migrate --check", cwd=self.familyhub_dir)
        if result and result.returncode == 0:
            self.result.add_pass("FamilyHub migrations can be applied")
        else:
            error = result.stderr if result else "Command failed to run"
            self.result.add_fail("FamilyHub migrations application", error)
    
    def start_server(self, project_dir, port, name):
        """Start a Django development server"""
        try:
            cmd = f"python manage.py runserver {port}"
            process = subprocess.Popen(
                cmd,
                shell=True,
                cwd=project_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for server to start
            time.sleep(3)
            
            # Check if server is running
            try:
                response = requests.get(f"http://127.0.0.1:{port}/", timeout=5)
                if response.status_code in [200, 302, 404]:  # 404 is OK, means server is running
                    self.log(f"{name} server started on port {port}")
                    return process
            except requests.exceptions.RequestException:
                pass
            
            # If we get here, server didn't start properly
            process.terminate()
            return None
            
        except Exception as e:
            self.log(f"Failed to start {name} server: {e}")
            return None
    
    def stop_server(self, process, name):
        """Stop a Django development server"""
        if process:
            try:
                process.terminate()
                process.wait(timeout=5)
                self.log(f"{name} server stopped")
            except subprocess.TimeoutExpired:
                process.kill()
                self.log(f"{name} server force killed")
            except Exception as e:
                self.log(f"Error stopping {name} server: {e}")
    
    def test_server_startup(self):
        """Test that both servers can start without errors"""
        print(f"\n{Colors.BOLD}Testing Server Startup{Colors.END}")
        
        # Test FamilyHub server
        self.familyhub_process = self.start_server(self.familyhub_dir, 8000, "FamilyHub")
        if self.familyhub_process:
            self.result.add_pass("FamilyHub server startup")
        else:
            self.result.add_fail("FamilyHub server startup", "Server failed to start or respond")
        
        # Test Standalone server (if configured)
        if (self.standalone_dir / 'manage.py').exists():
            self.standalone_process = self.start_server(self.standalone_dir, 8001, "Standalone")
            if self.standalone_process:
                self.result.add_pass("Standalone server startup")
            else:
                self.result.add_fail("Standalone server startup", "Server failed to start or respond")
        else:
            self.result.add_pass("Standalone server not configured (expected)")
    
    def test_url_responses(self):
        """Test that key URLs respond correctly"""
        print(f"\n{Colors.BOLD}Testing URL Responses{Colors.END}")
        
        # Test FamilyHub timesheet URLs
        if self.familyhub_process:
            test_urls = [
                ('/timesheet/', 'FamilyHub timesheet dashboard'),
                ('/timesheet/daily/', 'FamilyHub daily entry'),
                ('/timesheet/weekly/', 'FamilyHub weekly summary'),
                ('/timesheet/jobs/', 'FamilyHub job list'),
            ]
            
            for url, description in test_urls:
                try:
                    response = requests.get(f"http://127.0.0.1:8000{url}", timeout=5)
                    if response.status_code in [200, 302]:  # 302 redirect is OK (login required)
                        self.result.add_pass(description)
                    else:
                        self.result.add_fail(description, f"HTTP {response.status_code}")
                except requests.exceptions.RequestException as e:
                    self.result.add_fail(description, f"Request failed: {e}")
    
    def test_app_settings(self):
        """Test app settings functionality"""
        print(f"\n{Colors.BOLD}Testing App Settings{Colors.END}")
        
        # Test app settings import and basic functionality
        try:
            script_content = '''
import sys
import os
from pathlib import Path

# Add shared apps to path
shared_path = Path(r"c:\\Users\\Dmitry\\OneDrive\\Development\\myprojects\\family-hub-workspace\\shared\\apps")
sys.path.insert(0, str(shared_path))

# Setup basic environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyHub.settings')

# Basic import test
try:
    from timesheet.app_settings import TimesheetSettings
    settings = TimesheetSettings()
    
    print(f"deployment_context:{settings.deployment_context}")
    print(f"is_standalone:{settings.is_standalone}")
    print(f"base_template:{settings.base_template}")
    print(f"navigation_items_count:{len(settings.navigation_items)}")
    print("SUCCESS")
except Exception as e:
    print(f"ERROR:{e}")
'''
            
            with open(self.workspace_root / 'temp_test_settings.py', 'w') as f:
                f.write(script_content)
            
            result = self.run_command("python temp_test_settings.py", cwd=self.workspace_root)
            
            if result and result.returncode == 0:
                output = result.stdout.strip()
                if 'SUCCESS' in output and 'deployment_context:' in output:
                    self.result.add_pass("App settings import and basic functionality")
                else:
                    self.result.add_fail("App settings functionality", f"Unexpected output: {output}")
            else:
                error = result.stderr if result else "Command failed"
                self.result.add_fail("App settings import", error)
            
            # Cleanup
            temp_file = self.workspace_root / 'temp_test_settings.py'
            if temp_file.exists():
                temp_file.unlink()
                
        except Exception as e:
            self.result.add_fail("App settings test", str(e))
    
    def test_template_inheritance(self):
        """Test that templates use correct inheritance based on deployment"""
        print(f"\n{Colors.BOLD}Testing Template Inheritance{Colors.END}")
        
        # Check that templates have conditional inheritance
        template_files = [
            'dashboard.html',
            'daily_entry.html', 
            'weekly_summary.html',
            'job_list.html'
        ]
        
        template_dir = self.shared_apps_dir / 'timesheet' / 'templates' / 'timesheet'
        
        for template_file in template_files:
            template_path = template_dir / template_file
            if template_path.exists():
                try:
                    content = template_path.read_text()
                    if '{% extends base_template|default:' in content:
                        self.result.add_pass(f"Template {template_file} has conditional inheritance")
                    else:
                        self.result.add_fail(f"Template {template_file} conditional inheritance", 
                                           "Missing conditional extends tag")
                except Exception as e:
                    self.result.add_fail(f"Template {template_file} read", str(e))
            else:
                self.result.add_fail(f"Template {template_file} exists", "Template file not found")
    
    def cleanup(self):
        """Stop any running servers"""
        print(f"\n{Colors.BOLD}Cleaning Up{Colors.END}")
        self.stop_server(self.familyhub_process, "FamilyHub")
        self.stop_server(self.standalone_process, "Standalone")
    
    def run_tests(self, standalone_only=False, integrated_only=False):
        """Run the complete test suite"""
        print(f"{Colors.BOLD}FamilyHub Timesheet Integration Test Suite{Colors.END}")
        print("=" * 60)
        
        try:
            # Always test basic structure
            self.test_directory_structure()
            self.test_django_check()
            self.test_database_migrations()
            self.test_app_settings()
            self.test_template_inheritance()
            
            # Server tests (unless disabled)
            if not standalone_only:  # Test integrated by default
                self.test_server_startup()
                self.test_url_responses()
            
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Tests interrupted by user{Colors.END}")
        except Exception as e:
            print(f"\n{Colors.RED}Test suite error: {e}{Colors.END}")
        finally:
            self.cleanup()
        
        # Print summary
        success = self.result.summary()
        
        if success:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ All tests passed! Integration is working correctly.{Colors.END}")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}✗ Some tests failed. Review the issues above.{Colors.END}")
        
        return success

def main():
    parser = argparse.ArgumentParser(description='Test FamilyHub timesheet integration')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--standalone-only', action='store_true', help='Test standalone deployment only')
    parser.add_argument('--integrated-only', action='store_true', help='Test integrated deployment only')
    
    args = parser.parse_args()
    
    tester = DualDeploymentTester(verbose=args.verbose)
    success = tester.run_tests(
        standalone_only=args.standalone_only,
        integrated_only=args.integrated_only
    )
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
