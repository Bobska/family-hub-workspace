"""
Timesheet App Settings
Handles deployment-specific configuration and behavior
"""
import os
import sys
from django.conf import settings
from django.urls import reverse_lazy


class TimesheetSettings:
    """
    Centralized configuration for timesheet app behavior
    Adapts to standalone vs integrated deployment contexts
    """
    
    def __init__(self):
        self._deployment_context = self._detect_deployment_context()
    
    def _detect_deployment_context(self):
        """
        Detect whether running in standalone or integrated mode
        """
        # Check if running as standalone project
        if 'timesheet_project' in sys.modules or 'timesheet_project' in [
            mod.split('.')[0] for mod in sys.modules.keys()
        ]:
            return 'standalone'
        
        # Check for FamilyHub context
        if 'FamilyHub' in sys.modules or 'home' in getattr(settings, 'INSTALLED_APPS', []):
            return 'integrated'
        
        # Fallback: check project root
        project_root = getattr(settings, 'BASE_DIR', '')
        if 'standalone-apps' in str(project_root):
            return 'standalone'
        elif 'FamilyHub' in str(project_root):
            return 'integrated'
        
        return 'standalone'  # Default fallback
    
    @property
    def is_standalone(self):
        """True if running in standalone deployment"""
        return self._deployment_context == 'standalone'
    
    @property
    def is_integrated(self):
        """True if running in FamilyHub integration"""
        return self._deployment_context == 'integrated'
    
    @property
    def deployment_context(self):
        """Current deployment context: 'standalone' or 'integrated'"""
        return self._deployment_context
    
    @property
    def app_name(self):
        """App name for URLs and navigation"""
        return 'timesheet'
    
    @property
    def app_title(self):
        """Human-readable app title"""
        return 'Timesheet Tracker'
    
    @property
    def app_description(self):
        """App description for dashboard cards"""
        if self.is_integrated:
            return 'Track work hours, manage jobs, and generate timesheet reports'
        return 'Professional timesheet tracking and management system'
    
    @property
    def base_template(self):
        """Base template to use based on deployment context"""
        if self.is_integrated:
            return 'timesheet/base_integrated.html'
        return 'timesheet/base.html'
    
    @property
    def success_url_dashboard(self):
        """Dashboard URL for redirects"""
        if self.is_integrated:
            return reverse_lazy('timesheet:dashboard')
        return reverse_lazy('timesheet:dashboard')
    
    @property
    def breadcrumb_home(self):
        """Home breadcrumb configuration"""
        if self.is_integrated:
            return {
                'name': 'FamilyHub',
                'url': reverse_lazy('home:dashboard') if 'home' in getattr(settings, 'INSTALLED_APPS', []) else '/'
            }
        return {
            'name': 'Home',
            'url': reverse_lazy('timesheet:dashboard')
        }
    
    @property
    def navigation_items(self):
        """Navigation menu items based on deployment context"""
        base_items = [
            {'name': 'Dashboard', 'url': 'timesheet:dashboard', 'icon': 'fas fa-tachometer-alt'},
            {'name': 'Daily Entry', 'url': 'timesheet:daily_entry', 'icon': 'fas fa-plus-circle'},
            {'name': 'Weekly Summary', 'url': 'timesheet:weekly_summary', 'icon': 'fas fa-calendar-week'},
            {'name': 'Manage Jobs', 'url': 'timesheet:job_list', 'icon': 'fas fa-briefcase'},
        ]
        
        if self.is_integrated:
            # Add integration-specific navigation
            base_items.append({
                'name': 'Back to FamilyHub', 
                'url': 'home:dashboard', 
                'icon': 'fas fa-home',
                'css_class': 'btn-outline-light'
            })
        
        return base_items
    
    @property
    def pagination_per_page(self):
        """Items per page for list views"""
        if self.is_integrated:
            return 10  # Smaller pages in integrated view
        return 25  # Larger pages in standalone
    
    @property
    def date_format(self):
        """Date format for forms and displays"""
        return '%Y-%m-%d'
    
    @property
    def time_format(self):
        """Time format for forms and displays"""
        return '%H:%M'
    
    @property
    def datetime_format(self):
        """DateTime format for displays"""
        return '%Y-%m-%d %H:%M'
    
    @property
    def timezone(self):
        """Timezone setting"""
        return getattr(settings, 'TIME_ZONE', 'Pacific/Auckland')
    
    @property
    def dashboard_widgets(self):
        """Dashboard widget configuration based on deployment"""
        base_widgets = [
            'today_summary',
            'week_summary', 
            'recent_entries',
            'active_jobs'
        ]
        
        if self.is_integrated:
            # Simplified widgets for integrated view
            return ['today_summary', 'recent_entries']
        
        return base_widgets
    
    @property
    def form_css_classes(self):
        """CSS classes for form styling"""
        return {
            'form': 'needs-validation',
            'field': 'form-control',
            'select': 'form-select',
            'checkbox': 'form-check-input',
            'submit': 'btn btn-primary',
            'cancel': 'btn btn-secondary'
        }
    
    @property
    def alert_classes(self):
        """Bootstrap alert classes for messages"""
        return {
            'error': 'alert-danger',
            'warning': 'alert-warning', 
            'success': 'alert-success',
            'info': 'alert-info'
        }
    
    def get_context_data(self, **kwargs):
        """
        Get context data for templates
        """
        context = {
            'timesheet_settings': self,
            'is_standalone': self.is_standalone,
            'is_integrated': self.is_integrated,
            'deployment_context': self.deployment_context,
            'base_template': self.base_template,
            'app_name': self.app_name,
            'app_title': self.app_title,
            'app_description': self.app_description,
            'navigation_items': self.navigation_items,
            'breadcrumb_home': self.breadcrumb_home,
        }
        context.update(kwargs)
        return context


# Global instance
timesheet_settings = TimesheetSettings()


def get_timesheet_settings():
    """
    Get the global timesheet settings instance
    """
    return timesheet_settings


def get_app_context(request=None, **kwargs):
    """
    Get app-specific context for views and templates
    """
    return timesheet_settings.get_context_data(**kwargs)
