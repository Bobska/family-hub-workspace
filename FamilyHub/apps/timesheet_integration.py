"""
Timesheet App Integration Module for FamilyHub.

This module handles the proper integration of the standalone timesheet app
into the FamilyHub project, managing imports, context processors, and
template overrides for seamless integration.
"""

import os
import sys
from pathlib import Path
from django.conf import settings


def setup_timesheet_integration():
    """
    Set up the timesheet app integration for FamilyHub.
    
    This function ensures that the standalone timesheet app is properly
    accessible within the FamilyHub Django project.
    """
    # Get the base directory for FamilyHub
    base_dir = Path(settings.BASE_DIR)
    
    # Path to standalone timesheet app
    standalone_timesheet_path = base_dir.parent / 'standalone-apps' / 'timesheet' / 'timesheet_app'
    
    # Add standalone timesheet app to Python path if not already there
    standalone_timesheet_str = str(standalone_timesheet_path)
    if standalone_timesheet_str not in sys.path:
        sys.path.insert(0, standalone_timesheet_str)
        print(f"Added timesheet app to Python path: {standalone_timesheet_str}")
    
    return standalone_timesheet_path


def create_symbolic_link_or_proxy():
    """
    Create symbolic link or proxy for timesheet app integration.
    
    Attempts to create a symbolic link on systems that support it,
    falls back to creating a proxy module on Windows.
    """
    apps_dir = Path(settings.BASE_DIR) / 'apps'
    apps_dir.mkdir(exist_ok=True)
    
    timesheet_link = apps_dir / 'timesheet_app'
    standalone_path = setup_timesheet_integration()
    
    if not timesheet_link.exists():
        try:
            # Try to create symbolic link (works on Linux, Mac, and Windows with proper permissions)
            if os.name == 'nt':  # Windows
                # On Windows, try creating junction point
                import subprocess
                cmd = f'mklink /J "{timesheet_link}" "{standalone_path}"'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"Created junction point: {timesheet_link} -> {standalone_path}")
                    return True
                else:
                    print("Junction point creation failed, falling back to proxy module")
                    return create_proxy_module(timesheet_link, standalone_path)
            else:
                # Unix-like systems
                timesheet_link.symlink_to(standalone_path)
                print(f"Created symbolic link: {timesheet_link} -> {standalone_path}")
                return True
                
        except (OSError, PermissionError) as e:
            print(f"Symbolic link creation failed: {e}")
            return create_proxy_module(timesheet_link, standalone_path)
    
    return True


def create_proxy_module(link_path, standalone_path):
    """
    Create a proxy module that imports from the standalone timesheet app.
    
    This is a fallback when symbolic links cannot be created.
    """
    link_path.mkdir(exist_ok=True)
    
    # Create __init__.py that imports everything from standalone app
    init_content = f'''"""
Proxy module for timesheet app integration.

This module imports all components from the standalone timesheet app
to make them available within the FamilyHub project structure.
"""

import sys
from pathlib import Path

# Add standalone timesheet app to path
standalone_path = Path("{standalone_path}")
if str(standalone_path) not in sys.path:
    sys.path.insert(0, str(standalone_path))

# Import all components from standalone timesheet app
try:
    from timesheet_app.models import *
    from timesheet_app.views import *
    from timesheet_app.forms import *
    from timesheet_app.admin import *
    from timesheet_app import urls
    from timesheet_app import apps
except ImportError as e:
    print(f"Warning: Could not import from timesheet_app: {{e}}")
'''
    
    init_file = link_path / '__init__.py'
    with open(init_file, 'w') as f:
        f.write(init_content)
    
    print(f"Created proxy module at: {link_path}")
    return True


def timesheet_context_processor(request):
    """
    Context processor for timesheet app integration.
    
    Adds integration flags and FamilyHub-specific context when
    the timesheet app is running within FamilyHub.
    """
    return {
        'IS_INTEGRATED': True,
        'IS_FAMILYHUB': True,
        'TIMESHEET_NAMESPACE': 'timesheet',
        'FAMILYHUB_BASE_URL': '/',
        'INTEGRATION_MODE': 'familyhub'
    }


# Auto-setup when module is imported
try:
    setup_timesheet_integration()
    create_symbolic_link_or_proxy()
except Exception as e:
    print(f"Warning: Timesheet integration setup failed: {e}")
