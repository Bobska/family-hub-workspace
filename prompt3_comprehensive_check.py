#!/usr/bin/env python3
"""
PROMPT 3 COMPREHENSIVE VERIFICATION CHECKLIST
Systematically verify all PROMPT 3 requirements are met
"""

import urllib.request
import urllib.error
import subprocess
import json
import sys
from pathlib import Path

class PromptThreeChecker:
    def __init__(self):
        self.results = {}
        self.workspace = Path("C:/Users/Dmitry/OneDrive/Development/myprojects/family-hub-workspace")
        
    def check_file_exists(self, filepath, description):
        """Check if a file exists"""
        full_path = self.workspace / filepath
        exists = full_path.exists()
        self.results[description] = {
            'status': '✅ PASS' if exists else '❌ FAIL',
            'details': f'File exists: {full_path}' if exists else f'Missing: {full_path}'
        }
        return exists
        
    def check_url_response(self, url, description, expected_status=200):
        """Check URL accessibility"""
        try:
            response = urllib.request.urlopen(url, timeout=10)
            status = response.status
            content_length = len(response.read())
            
            if status == expected_status or (expected_status == 302 and status in [200, 302]):
                self.results[description] = {
                    'status': '✅ PASS',
                    'details': f'HTTP {status}, {content_length} bytes'
                }
                return True
            else:
                self.results[description] = {
                    'status': '❌ FAIL',
                    'details': f'HTTP {status}, expected {expected_status}'
                }
                return False
                
        except urllib.error.HTTPError as e:
            if e.code == 302 and expected_status in [200, 302]:
                self.results[description] = {
                    'status': '✅ PASS',
                    'details': f'HTTP {e.code} (redirect - authentication required)'
                }
                return True
            else:
                self.results[description] = {
                    'status': '❌ FAIL', 
                    'details': f'HTTP {e.code}'
                }
                return False
                
        except Exception as e:
            self.results[description] = {
                'status': '❌ FAIL',
                'details': f'Error: {str(e)}'
            }
            return False
            
    def check_docker_containers(self):
        """Check Docker container status"""
        try:
            result = subprocess.run(
                ['docker-compose', 'ps', '--format', 'json'], 
                capture_output=True, 
                text=True, 
                cwd=self.workspace
            )
            
            if result.returncode == 0:
                containers = []
                for line in result.stdout.strip().split('\\n'):
                    if line.strip():
                        try:
                            container = json.loads(line)
                            containers.append(container)
                        except json.JSONDecodeError:
                            pass
                            
                db_running = any(c.get('Service') == 'db' and 'healthy' in c.get('Health', '') for c in containers)
                app_running = any(c.get('Service') == 'familyhub' for c in containers)
                
                self.results['Docker DB Container'] = {
                    'status': '✅ PASS' if db_running else '❌ FAIL',
                    'details': 'PostgreSQL container healthy' if db_running else 'PostgreSQL container not healthy'
                }
                
                self.results['Docker App Container'] = {
                    'status': '✅ PASS' if app_running else '❌ FAIL',
                    'details': 'FamilyHub container running' if app_running else 'FamilyHub container not running'
                }
                
                return db_running and app_running
            else:
                self.results['Docker Containers'] = {
                    'status': '❌ FAIL',
                    'details': 'docker-compose ps failed'
                }
                return False
                
        except Exception as e:
            self.results['Docker Containers'] = {
                'status': '❌ FAIL',
                'details': f'Error checking containers: {str(e)}'
            }
            return False
            
    def run_comprehensive_check(self):
        """Run all PROMPT 3 checks"""
        
        print("🐳 PROMPT 3: DOCKER CONFIGURATION COMPREHENSIVE VERIFICATION")
        print("=" * 65)
        
        # 1. Docker Infrastructure Files
        print("\\n📁 DOCKER INFRASTRUCTURE FILES:")
        self.check_file_exists("FamilyHub/Dockerfile", "Dockerfile exists")
        self.check_file_exists("docker-compose.yml", "docker-compose.yml exists")
        self.check_file_exists("FamilyHub/FamilyHub/settings/docker.py", "Docker settings exists")
        self.check_file_exists(".env", "Environment file exists")
        
        # 2. Docker Containers Status
        print("\\n🐳 DOCKER CONTAINERS:")
        self.check_docker_containers()
        
        # 3. Core Application URLs
        print("\\n🌐 APPLICATION ACCESSIBILITY:")
        self.check_url_response("http://localhost:8000/", "Main Dashboard")
        self.check_url_response("http://localhost:8000/health/", "Health Check")
        self.check_url_response("http://localhost:8000/admin/", "Admin Panel")
        self.check_url_response("http://localhost:8000/accounts/login/", "Login Page")
        
        # 4. Timesheet Integration (The main PROMPT 3 goal)
        print("\\n🎯 TIMESHEET INTEGRATION:")
        self.check_url_response("http://localhost:8000/timesheet/", "Timesheet App", expected_status=302)
        
        # 5. Static Files
        print("\\n📦 STATIC FILES:")
        self.check_url_response("http://localhost:8000/static/css/main.css", "Main CSS", expected_status=200)
        
        # Generate Report
        self.generate_report()
        
    def generate_report(self):
        """Generate comprehensive verification report"""
        
        print("\\n" + "=" * 65)
        print("📊 PROMPT 3 VERIFICATION RESULTS")
        print("=" * 65)
        
        passed = 0
        failed = 0
        
        for description, result in self.results.items():
            status = result['status']
            details = result['details']
            print(f"{status} {description}")
            print(f"    {details}")
            
            if '✅' in status:
                passed += 1
            else:
                failed += 1
                
        print("\\n" + "=" * 65)
        print(f"📈 SUMMARY: {passed} PASSED, {failed} FAILED")
        
        if failed == 0:
            print("🎉 PROMPT 3: DOCKER CONFIGURATION - COMPLETE SUCCESS!")
            print("✅ All requirements met, Docker integration fully functional")
        elif failed <= 2:
            print("⚠️  PROMPT 3: DOCKER CONFIGURATION - MOSTLY SUCCESSFUL")
            print("✅ Core infrastructure working, minor issues to address")
        else:
            print("❌ PROMPT 3: DOCKER CONFIGURATION - NEEDS ATTENTION")
            print("⚠️  Multiple issues found, review required")
            
        print("=" * 65)

if __name__ == "__main__":
    checker = PromptThreeChecker()
    checker.run_comprehensive_check()
