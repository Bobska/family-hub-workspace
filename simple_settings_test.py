"""
Simple app settings validation script
"""
import sys
import os
from pathlib import Path

# Add shared apps to path
shared_path = Path(r"c:\Users\Dmitry\OneDrive\Development\myprojects\family-hub-workspace\shared\apps")
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
