"""
FamilyHub App Registry - Dynamic App Discovery and Management System

This module provides intelligent app discovery that can handle both integrated
apps (in FamilyHub/apps/) and standalone apps (in standalone-apps/).

Key Features:
- Dynamic INSTALLED_APPS generation
- Automatic Python path management
- App availability checking
- Sync status tracking
- Support for both symbolic links and file copying
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from django.conf import settings


class AppRegistry:
    """Central registry for managing FamilyHub apps across different modes."""
    
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.apps_dir = self.base_dir / 'apps'
        self.standalone_dir = self.base_dir.parent / 'standalone-apps'
        self.known_apps = {
            'timesheet': {
                'name': 'Timesheet',
                'description': 'Time tracking and job management',
                'icon': 'fas fa-clock',
                'color': 'primary',
                'app_module': 'timesheet_app',
                'standalone_project': 'timesheet_app',
                'priority': 1,
            },
            'daycare_invoice': {
                'name': 'Daycare Invoice Tracker',
                'description': 'Track and manage daycare invoices',
                'icon': 'fas fa-baby',
                'color': 'success',
                'app_module': 'daycare_invoice_app',
                'standalone_project': 'daycare_invoice_app',
                'priority': 2,
            },
            'employment_history': {
                'name': 'Employment History',
                'description': 'Manage employment records',
                'icon': 'fas fa-briefcase',
                'color': 'info',
                'app_module': 'employment_history_app',
                'standalone_project': 'employment_history_app',
                'priority': 3,
            },
            'upcoming_payments': {
                'name': 'Upcoming Payments',
                'description': 'Track upcoming bills and payments',
                'icon': 'fas fa-calendar-alt',
                'color': 'warning',
                'app_module': 'upcoming_payments_app',
                'standalone_project': 'upcoming_payments_app',
                'priority': 4,
            },
            'credit_card_mgmt': {
                'name': 'Credit Card Management',
                'description': 'Manage credit card accounts',
                'icon': 'fas fa-credit-card',
                'color': 'danger',
                'app_module': 'credit_card_mgmt_app',
                'standalone_project': 'credit_card_mgmt_app',
                'priority': 5,
            },
            'household_budget': {
                'name': 'Household Budget',
                'description': 'Family budget management',
                'icon': 'fas fa-calculator',
                'color': 'secondary',
                'app_module': 'household_budget_app',
                'standalone_project': 'household_budget_app',
                'priority': 6,
            },
        }
    
    def get_app_status(self, app_key: str) -> Dict:
        """Get comprehensive status of an app."""
        if app_key not in self.known_apps:
            return {'status': 'unknown', 'available': False}
        
        app_config = self.known_apps[app_key]
        integrated_path = self.apps_dir / app_config['app_module']
        standalone_path = self.standalone_dir / app_key / app_config['standalone_project']
        
        status = {
            'key': app_key,
            'config': app_config,
            'integrated_exists': integrated_path.exists(),
            'standalone_exists': standalone_path.exists(),
            'integrated_path': integrated_path,
            'standalone_path': standalone_path,
            'is_symlink': integrated_path.is_symlink() if integrated_path.exists() else False,
            'available': False,
            'status': 'not_available',
            'mode': None,
            'urls_available': False,
        }
        
        # Check if app has actual implementation
        if status['integrated_exists']:
            # Check if it's a proper implementation (has models.py with content)
            models_file = integrated_path / 'models.py'
            if models_file.exists() and models_file.stat().st_size > 100:  # Basic content check
                status['available'] = True
                status['status'] = 'integrated'
                status['mode'] = 'symlink' if status['is_symlink'] else 'copied'
                
                # Check for URL configuration
                urls_file = integrated_path / 'urls.py'
                if urls_file.exists():
                    status['urls_available'] = True
        
        elif status['standalone_exists']:
            # Standalone exists but not integrated
            status['status'] = 'standalone_only'
            status['mode'] = 'standalone'
            
            # Check if standalone has proper implementation
            models_file = standalone_path / 'models.py'
            if models_file.exists() and models_file.stat().st_size > 100:
                status['available'] = True
                
                # Check for URL configuration
                urls_file = standalone_path / 'urls.py'
                if urls_file.exists():
                    status['urls_available'] = True
        
        return status
    
    def get_all_app_statuses(self) -> Dict[str, Dict]:
        """Get status of all known apps."""
        return {app_key: self.get_app_status(app_key) for app_key in self.known_apps.keys()}
    
    def get_available_apps(self) -> List[str]:
        """Get list of apps that are available for use."""
        available = []
        for app_key in self.known_apps.keys():
            status = self.get_app_status(app_key)
            if status['available']:
                available.append(app_key)
        return available
    
    def get_django_app_names(self) -> List[str]:
        """Get list of Django app names for INSTALLED_APPS."""
        django_apps = []
        for app_key in self.known_apps.keys():
            status = self.get_app_status(app_key)
            if status['available'] and status['status'] == 'integrated':
                # Use just the app module name since apps/ is in Python path
                app_module = self.known_apps[app_key]['app_module']
                django_apps.append(app_module)  # Just 'timesheet_app', not 'apps.timesheet_app'
        return django_apps
    
    def setup_python_paths(self):
        """Setup Python paths for app discovery."""
        # Add apps directory to Python path
        apps_path = str(self.apps_dir)
        if apps_path not in sys.path:
            sys.path.insert(0, apps_path)
        
        # Add standalone apps to path if needed
        standalone_path = str(self.standalone_dir)
        if standalone_path not in sys.path:
            sys.path.insert(0, standalone_path)
    
    def get_app_urls(self) -> List[Tuple[str, str, str]]:
        """Get URL patterns for available apps."""
        url_patterns = []
        for app_key in self.known_apps.keys():
            status = self.get_app_status(app_key)
            if status['available'] and status['urls_available']:
                app_module = self.known_apps[app_key]['app_module']
                url_patterns.append((
                    f'{app_key}/',
                    f'{app_module}.urls',  # Just 'timesheet_app.urls', not 'apps.timesheet_app.urls'
                    app_key
                ))
        return url_patterns
    
    def sync_app(self, app_key: str, method: str = 'symlink') -> bool:
        """Sync an app from standalone to integrated."""
        if app_key not in self.known_apps:
            return False
        
        status = self.get_app_status(app_key)
        if not status['standalone_exists']:
            return False
        
        app_config = self.known_apps[app_key]
        source_path = status['standalone_path']
        target_path = status['integrated_path']
        
        # Remove existing target if it exists
        if target_path.exists():
            if target_path.is_symlink():
                target_path.unlink()
            else:
                import shutil
                shutil.rmtree(target_path)
        
        try:
            if method == 'symlink':
                # Create symbolic link
                target_path.symlink_to(source_path, target_is_directory=True)
            elif method == 'copy':
                # Copy files
                import shutil
                shutil.copytree(source_path, target_path)
            else:
                return False
            
            return True
        except Exception as e:
            print(f"Failed to sync {app_key}: {e}")
            return False
    
    def get_dashboard_data(self) -> List[Dict]:
        """Get data for dashboard app cards."""
        dashboard_apps = []
        statuses = self.get_all_app_statuses()
        
        for app_key, status in statuses.items():
            config = status['config']
            app_data = {
                'key': app_key,
                'name': config['name'],
                'description': config['description'],
                'icon': config['icon'],
                'color': config['color'],
                'available': status['available'],
                'status': status['status'],
                'mode': status['mode'],
                'url': f'/{app_key}/' if status['available'] and status['urls_available'] else None,
                'priority': config['priority'],
            }
            dashboard_apps.append(app_data)
        
        # Sort by priority
        dashboard_apps.sort(key=lambda x: x['priority'])
        return dashboard_apps


# Global registry instance
app_registry = AppRegistry()


def get_dynamic_installed_apps() -> List[str]:
    """Get dynamically generated INSTALLED_APPS list."""
    # Core Django apps
    django_apps = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]
    
    # FamilyHub core apps
    familyhub_apps = [
        'home',
    ]
    
    # Third-party apps
    third_party_apps = [
        # Add third-party apps here
    ]
    
    # Setup Python paths
    app_registry.setup_python_paths()
    
    # Get available integrated apps
    integrated_apps = app_registry.get_django_app_names()
    
    return django_apps + familyhub_apps + third_party_apps + integrated_apps


def get_dynamic_url_patterns():
    """Get dynamically generated URL patterns for apps."""
    return app_registry.get_app_urls()
