#!/usr/bin/env python3
"""
PROMPT 2 Implementation Verification Script
Verifies that structure cleanup and duplicate removal was successful
"""

import os
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

def main():
    print(f"{BLUE}{'='*60}")
    print(f"🧹 PROMPT 2 IMPLEMENTATION VERIFICATION")
    print(f"   Remove Duplicates and Fix Structure")
    print(f"{'='*60}{RESET}\n")
    
    # Check FamilyHub/apps directory structure
    apps_dir = Path("apps")
    if apps_dir.exists():
        print_status("Checking FamilyHub/apps directory structure...", 'info')
        
        app_dirs = [d for d in apps_dir.iterdir() if d.is_dir() and not d.name.startswith('__')]
        
        if len(app_dirs) == 1 and app_dirs[0].name == 'timesheet_app':
            print_status("✅ Apps directory properly cleaned - only timesheet_app remains", 'success')
        else:
            print_status(f"❌ Unexpected apps found: {[d.name for d in app_dirs]}", 'error')
            
        # Check for empty directories
        empty_dirs = []
        for app_dir in app_dirs:
            if app_dir.is_dir():
                contents = list(app_dir.iterdir())
                if not contents:
                    empty_dirs.append(app_dir.name)
                    
        if not empty_dirs:
            print_status("✅ No empty stub directories found", 'success')
        else:
            print_status(f"❌ Empty directories still exist: {empty_dirs}", 'error')
    else:
        print_status("❌ FamilyHub/apps directory not found", 'error')
    
    # Check timesheet_app content
    timesheet_dir = Path("apps/timesheet_app")
    if timesheet_dir.exists():
        print_status("Checking timesheet_app implementation...", 'info')
        
        # Check key files exist
        key_files = ['models.py', 'views.py', 'urls.py', 'apps.py']
        missing_files = []
        
        for file in key_files:
            if not (timesheet_dir / file).exists():
                missing_files.append(file)
                
        if not missing_files:
            print_status("✅ All key timesheet_app files present", 'success')
        else:
            print_status(f"❌ Missing timesheet_app files: {missing_files}", 'error')
            
        # Check models.py has content
        models_file = timesheet_dir / 'models.py'
        if models_file.exists():
            content = models_file.read_text(encoding='utf-8')
            if len(content.strip()) > 100:  # Has substantial content
                print_status("✅ timesheet_app models.py has implementation", 'success')
            else:
                print_status("❌ timesheet_app models.py appears to be stub", 'error')
    else:
        print_status("❌ timesheet_app directory not found", 'error')
    
    # Check dashboard template
    template_file = Path("home/templates/home/dashboard.html")
    if template_file.exists():
        print_status("Checking dashboard template...", 'info')
        
        content = template_file.read_text(encoding='utf-8')
        if '{% for app in apps %}' in content:
            print_status("✅ Dashboard template uses correct variable name 'apps'", 'success')
        else:
            print_status("❌ Dashboard template variable issue", 'error')
            
        if 'app.available' in content:
            print_status("✅ Dashboard template filters by availability", 'success')
        else:
            print_status("❌ Dashboard template doesn't filter by availability", 'error')
    else:
        print_status("❌ Dashboard template not found", 'error')
    
    # Check app registry
    registry_file = Path("home/app_registry.py")
    if registry_file.exists():
        print_status("Checking app registry...", 'info')
        
        content = registry_file.read_text(encoding='utf-8')
        if 'get_available_apps' in content:
            print_status("✅ App registry has dynamic discovery", 'success')
        else:
            print_status("❌ App registry missing dynamic discovery", 'error')
    else:
        print_status("❌ App registry not found", 'error')
    
    # Check for duplicate files
    print_status("Checking for potential duplicates...", 'info')
    
    # Look for common duplicate patterns
    duplicate_patterns = [
        'timesheet',  # Should only be in apps/timesheet_app/
    ]
    
    found_duplicates = False
    for pattern in duplicate_patterns:
        # Search for files containing this pattern
        for root, dirs, files in os.walk('.'):
            # Skip __pycache__ and other system directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            
            for file in files:
                if pattern in file.lower() and not file.endswith('.pyc'):
                    file_path = Path(root) / file
                    if 'apps/timesheet_app' not in str(file_path):
                        print_status(f"⚠️ Potential duplicate: {file_path}", 'warning')
                        found_duplicates = True
    
    if not found_duplicates:
        print_status("✅ No obvious duplicates found", 'success')
    
    print(f"\n{BLUE}{'='*60}")
    print(f"📊 PROMPT 2 VERIFICATION COMPLETE")
    print(f"{'='*60}{RESET}")

if __name__ == '__main__':
    main()
