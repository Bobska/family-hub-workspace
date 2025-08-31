#!/usr/bin/env python
"""
Script to integrate standalone apps into FamilyHub
Usage: python integrate_app.py <app_name>
"""

import os
import sys
import shutil
from pathlib import Path

def integrate_app(app_name):
    """Integrate a standalone app into FamilyHub"""
    
    base_dir = Path(__file__).parent
    standalone_dir = base_dir.parent / 'standalone-apps' / app_name
    target_dir = base_dir / 'apps' / f'{app_name}_app'
    
    if not standalone_dir.exists():
        print(f"Error: Standalone app '{app_name}' not found at {standalone_dir}")
        return False
    
    # Find the actual app directory within the standalone project
    # For timesheet: standalone-apps/timesheet/timesheet_app/
    app_dirs = [d for d in standalone_dir.iterdir() 
                if d.is_dir() and d.name.endswith('_app')]
    
    if not app_dirs:
        print(f"Error: No app directory found in {standalone_dir}")
        print("Looking for directories ending with '_app'")
        print("Available directories:")
        for d in standalone_dir.iterdir():
            if d.is_dir():
                print(f"  - {d.name}")
        return False
    
    source_app_dir = app_dirs[0]
    
    print(f"Integrating {source_app_dir} -> {target_dir}")
    
    # Windows - copy instead of symbolic links (more reliable)
    if target_dir.exists():
        print(f"Removing existing {target_dir}")
        shutil.rmtree(target_dir)
    
    print(f"Copying app: {source_app_dir} -> {target_dir}")
    shutil.copytree(source_app_dir, target_dir)
    
    # Update settings.py to include the app
    settings_file = base_dir / 'FamilyHub' / 'settings' / 'base.py'
    app_name_in_settings = f"'{app_name}_app'"
    
    with open(settings_file, 'r') as f:
        content = f.read()
    
    if app_name_in_settings not in content:
        # Add to INSTALLED_APPS
        if "# Shared integrated apps" in content:
            content = content.replace(
                "'timesheet_app',  # Timesheet app from standalone integration",
                f"'timesheet_app',  # Timesheet app from standalone integration\n    '{app_name}_app',  # {app_name.title()} app from standalone integration"
            )
        else:
            # Fallback: add after 'home'
            content = content.replace(
                "# Core FamilyHub apps\n    'home',",
                f"# Core FamilyHub apps\n    'home',\n    \n    # Integrated apps\n    '{app_name}_app',"
            )
        
        with open(settings_file, 'w') as f:
            f.write(content)
        print(f"Added {app_name_in_settings} to INSTALLED_APPS in base.py")
    
    return True

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python integrate_app.py <app_name>")
        print("Available apps: timesheet, daycare_invoice, employment_history, upcoming_payments, credit_card_mgmt, household_budget")
        sys.exit(1)
    
    app_name = sys.argv[1]
    if integrate_app(app_name):
        print(f"\nSuccess! Now run:")
        print(f"  python manage.py makemigrations")
        print(f"  python manage.py migrate")
        print(f"  python manage.py runserver")
        print(f"\nTo use integrated mode:")
        print(f"  $env:DJANGO_SETTINGS_MODULE='FamilyHub.settings.development_full'")
    else:
        print(f"\nFailed to integrate {app_name}")
