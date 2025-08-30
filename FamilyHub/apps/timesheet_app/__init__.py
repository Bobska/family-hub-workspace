"""
Timesheet App Proxy Module for FamilyHub Integration.

This module acts as a bridge to the standalone timesheet app,
making it accessible within the FamilyHub Django project.
"""

import sys
import os
from pathlib import Path

# Get the standalone timesheet app path
current_dir = Path(__file__).parent.parent.parent.parent
standalone_timesheet_path = current_dir / 'standalone-apps' / 'timesheet' / 'timesheet_app'

# Add to Python path if not already there
standalone_timesheet_str = str(standalone_timesheet_path)
if standalone_timesheet_str not in sys.path:
    sys.path.insert(0, standalone_timesheet_str)

# Verify the path exists
if not standalone_timesheet_path.exists():
    raise ImportError(f"Standalone timesheet app not found at: {standalone_timesheet_path}")

# Set the module path for Django to find the timesheet app files
__path__ = [str(standalone_timesheet_path)]

# Django app configuration
default_app_config = 'timesheet_app.apps.TimesheetAppConfig'
