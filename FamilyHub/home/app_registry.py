"""
FamilyHub App Configuration Management
Centralized configuration for all family hub applications
"""
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from django.urls import reverse_lazy


@dataclass
class AppConfig:
    """Configuration for a single FamilyHub application"""
    name: str
    slug: str
    icon: str
    description: str
    color: str
    url_name: Optional[str] = None
    url_path: Optional[str] = None
    is_active: bool = True
    is_integrated: bool = False
    standalone_port: Optional[int] = None
    
    @property
    def url(self) -> str:
        """Get the URL for this app"""
        if self.url_name:
            try:
                return str(reverse_lazy(self.url_name))
            except:
                pass
        return self.url_path or f'/{self.slug}/'
    
    @property
    def standalone_url(self) -> Optional[str]:
        """Get standalone app URL if available"""
        if self.standalone_port:
            return f"http://127.0.0.1:{self.standalone_port}"
        return None


class FamilyHubAppsRegistry:
    """Registry for all FamilyHub applications"""
    
    def __init__(self):
        self._apps = {}
        self._initialize_default_apps()
    
    def _initialize_default_apps(self):
        """Initialize the default FamilyHub applications"""
        default_apps = [
            AppConfig(
                name="Timesheet",
                slug="timesheet", 
                icon="⏰",
                description="Track your work hours and projects",
                color="primary",
                url_path="/timesheet/",
                standalone_port=8001
            ),
            AppConfig(
                name="Household Budget",
                slug="budget",
                icon="💰", 
                description="Manage family finances and budgets",
                color="success",
                url_path="/budget/",
                standalone_port=8006
            ),
            AppConfig(
                name="Daycare Invoices",
                slug="daycare",
                icon="🧒",
                description="Track daycare bills and payments", 
                color="info",
                url_path="/daycare/",
                standalone_port=8002
            ),
            AppConfig(
                name="Employment History",
                slug="employment",
                icon="💼",
                description="Your career journey and records",
                color="warning", 
                url_path="/employment/",
                standalone_port=8003
            ),
            AppConfig(
                name="Upcoming Payments",
                slug="payments",
                icon="📅",
                description="Never miss a payment deadline",
                color="danger",
                url_path="/payments/", 
                standalone_port=8004
            ),
            AppConfig(
                name="Credit Cards",
                slug="creditcards",
                icon="💳",
                description="Manage credit cards and limits",
                color="secondary",
                url_path="/creditcards/",
                standalone_port=8005
            ),
        ]
        
        for app in default_apps:
            self._apps[app.slug] = app
    
    def get_all_apps(self) -> List[AppConfig]:
        """Get all registered applications"""
        return list(self._apps.values())
    
    def get_active_apps(self) -> List[AppConfig]:
        """Get only active applications"""
        return [app for app in self._apps.values() if app.is_active]
    
    def get_integrated_apps(self) -> List[AppConfig]:
        """Get applications that are integrated into FamilyHub"""
        return [app for app in self._apps.values() if app.is_integrated]
    
    def get_available_apps(self) -> List[AppConfig]:
        """Get applications that are actually available (have implementation)"""
        import os
        from pathlib import Path
        
        available_apps = []
        
        for app in self.get_active_apps():
            # Check if app has actual implementation
            # Try multiple possible paths for Docker/local compatibility
            possible_paths = [
                Path(f"apps/{app.slug}_app"),  # Local development
                Path(f"/app/apps/{app.slug}_app"),  # Docker absolute path
                Path(f"/standalone-apps/{app.slug}/{app.slug}_app"),  # Docker standalone path
            ]
            
            app_found = False
            for app_path in possible_paths:
                # An app is considered available if it has models.py with content
                models_file = app_path / "models.py"
                if models_file.exists():
                    try:
                        content = models_file.read_text(encoding='utf-8')
                        # Check if models.py has substantial content (not just imports/comments)
                        lines = [line.strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]
                        if len(lines) > 5:  # Has more than just basic imports
                            # Mark as available and integrated if it has real content
                            app.is_integrated = True
                            available_apps.append(app)
                            app_found = True
                            break
                    except:
                        continue
            
            if app_found:
                break
                    
        return available_apps

    def get_dashboard_data(self) -> List[Dict[str, Any]]:
        """Get dashboard data showing only available apps"""
        available_apps = self.get_available_apps()
        
        return [
            {
                'name': app.name,
                'slug': app.slug,
                'icon': app.icon,
                'description': app.description,
                'url': app.url,
                'color': app.color,
                'is_active': app.is_active,
                'is_integrated': app.is_integrated,
                'available': True,  # Only available apps are returned
                'standalone_url': app.standalone_url,
            }
            for app in available_apps
        ]

    def get_all_app_statuses(self) -> List[Dict[str, Any]]:
        """Get status of all apps for debugging"""
        return [
            {
                'name': app.name,
                'slug': app.slug,
                'available': app in self.get_available_apps(),
                'is_active': app.is_active,
                'is_integrated': app.is_integrated,
            }
            for app in self.get_all_apps()
        ]
    
    def get_app(self, slug: str) -> Optional[AppConfig]:
        """Get a specific application by slug"""
        return self._apps.get(slug)
    
    def register_app(self, app: AppConfig):
        """Register a new application"""
        self._apps[app.slug] = app
    
    def to_dict_list(self) -> List[Dict[str, Any]]:
        """Convert apps to dictionary list for template compatibility"""
        return [
            {
                'name': app.name,
                'slug': app.slug,
                'icon': app.icon,
                'description': app.description,
                'url': app.url,
                'color': app.color,
                'is_active': app.is_active,
                'is_integrated': app.is_integrated,
                'standalone_url': app.standalone_url,
            }
            for app in self.get_active_apps()
        ]


# Global registry instance
apps_registry = FamilyHubAppsRegistry()
