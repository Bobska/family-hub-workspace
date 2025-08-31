"""
Django management command to check status of all FamilyHub apps.

Usage:
    python manage.py app_status
    python manage.py app_status --detailed
    python manage.py app_status --app timesheet
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from FamilyHub.app_registry import app_registry
import sys
from pathlib import Path


class Command(BaseCommand):
    help = 'Check status of FamilyHub apps'

    def add_arguments(self, parser):
        parser.add_argument(
            '--app',
            type=str,
            help='Show status for specific app only'
        )
        parser.add_argument(
            '--detailed',
            action='store_true',
            help='Show detailed information'
        )
        parser.add_argument(
            '--urls',
            action='store_true',
            help='Show URL configuration'
        )

    def handle(self, *args, **options):
        app_name = options.get('app')
        detailed = options['detailed']
        show_urls = options['urls']

        self.stdout.write(self.style.SUCCESS('FamilyHub App Status'))
        self.stdout.write('=' * 50)

        if app_name:
            self.show_single_app(app_name, detailed)
        else:
            self.show_all_apps(detailed)
            
        if show_urls:
            self.show_url_configuration()

    def show_all_apps(self, detailed):
        """Show status of all apps."""
        statuses = app_registry.get_all_app_statuses()
        
        # Summary table
        self.stdout.write("\nApp Summary:")
        self.stdout.write("-" * 80)
        self.stdout.write(f"{'App Name':<20} {'Status':<15} {'Mode':<10} {'Available':<10} {'URLs':<5}")
        self.stdout.write("-" * 80)
        
        for app_key, status in statuses.items():
            config = app_registry.known_apps[app_key]
            name = config['name'][:19]  # Truncate if too long
            status_str = status['status'][:14]
            mode = status.get('mode', 'N/A')[:9] if status.get('mode') else 'N/A'
            available = '✅' if status['available'] else '❌'
            urls = '✅' if status['urls_available'] else '❌'
            
            self.stdout.write(f"{name:<20} {status_str:<15} {mode:<10} {available:<10} {urls:<5}")
        
        # Statistics
        total_apps = len(statuses)
        available_apps = sum(1 for s in statuses.values() if s['available'])
        integrated_apps = sum(1 for s in statuses.values() if s['status'] == 'integrated')
        standalone_only = sum(1 for s in statuses.values() if s['status'] == 'standalone_only')
        
        self.stdout.write("-" * 80)
        self.stdout.write(f"Total Apps: {total_apps}")
        self.stdout.write(f"Available: {available_apps}")
        self.stdout.write(f"Integrated: {integrated_apps}")
        self.stdout.write(f"Standalone Only: {standalone_only}")
        
        if detailed:
            self.stdout.write("\nDetailed Information:")
            self.stdout.write("=" * 50)
            for app_key in statuses.keys():
                self.show_single_app(app_key, True, brief_header=True)

    def show_single_app(self, app_name, detailed, brief_header=False):
        """Show status of a single app."""
        if app_name not in app_registry.known_apps:
            self.stdout.write(self.style.ERROR(f"Unknown app: {app_name}"))
            return

        status = app_registry.get_app_status(app_name)
        config = app_registry.known_apps[app_name]
        
        if brief_header:
            self.stdout.write(f"\n--- {config['name']} ({app_name}) ---")
        else:
            self.stdout.write(f"\nApp: {config['name']}")
            self.stdout.write(f"Key: {app_name}")
            self.stdout.write(f"Description: {config['description']}")
        
        # Status indicators
        status_color = self.style.SUCCESS if status['available'] else self.style.ERROR
        self.stdout.write(f"Status: {status_color(status['status'])}")
        
        if status['available']:
            self.stdout.write(self.style.SUCCESS("✅ Available"))
        else:
            self.stdout.write(self.style.ERROR("❌ Not Available"))
        
        if detailed:
            self.stdout.write(f"Django Module: {config['app_module']}")
            self.stdout.write(f"Standalone Project: {config['standalone_project']}")
            self.stdout.write(f"Priority: {config['priority']}")
            
            # Paths
            self.stdout.write(f"Standalone Path: {status['standalone_path']}")
            self.stdout.write(f"Standalone Exists: {'✅' if status['standalone_exists'] else '❌'}")
            self.stdout.write(f"Integrated Path: {status['integrated_path']}")
            self.stdout.write(f"Integrated Exists: {'✅' if status['integrated_exists'] else '❌'}")
            
            if status['integrated_exists']:
                link_type = "Symbolic Link" if status['is_symlink'] else "Regular Directory"
                self.stdout.write(f"Link Type: {link_type}")
            
            # URL availability
            if status['urls_available']:
                self.stdout.write(self.style.SUCCESS("✅ URLs Available"))
                if status['available']:
                    self.stdout.write(f"URL: /{app_name}/")
            else:
                self.stdout.write(self.style.WARNING("⚠️ No URLs Available"))
            
            # Show file structure if available
            if status['integrated_exists'] and brief_header:
                self.show_app_structure(status['integrated_path'])

    def show_app_structure(self, app_path):
        """Show the structure of an app directory."""
        try:
            files = list(app_path.iterdir())
            python_files = [f for f in files if f.suffix == '.py']
            
            if python_files:
                self.stdout.write("Python Files:")
                for file in sorted(python_files):
                    size = file.stat().st_size
                    size_indicator = "📄" if size > 100 else "📋"  # Empty vs has content
                    self.stdout.write(f"  {size_indicator} {file.name} ({size} bytes)")
            
            # Check for important directories
            important_dirs = ['templates', 'static', 'migrations']
            for dirname in important_dirs:
                dir_path = app_path / dirname
                if dir_path.exists() and dir_path.is_dir():
                    self.stdout.write(f"📁 {dirname}/ (exists)")
                    
        except Exception as e:
            self.stdout.write(f"Could not read app structure: {e}")

    def show_url_configuration(self):
        """Show current URL configuration."""
        self.stdout.write("\nURL Configuration:")
        self.stdout.write("=" * 30)
        
        url_patterns = app_registry.get_app_urls()
        
        if url_patterns:
            for url_pattern, include_path, namespace in url_patterns:
                self.stdout.write(f"/{url_pattern} -> {include_path} (namespace: {namespace})")
        else:
            self.stdout.write("No app URLs currently configured")
        
        # Show Django admin and other core URLs
        self.stdout.write("\nCore URLs:")
        self.stdout.write("/admin/ -> Django Admin")
        self.stdout.write("/ -> Home Dashboard")
        self.stdout.write("/accounts/ -> Authentication")

    def show_django_settings_info(self):
        """Show relevant Django settings information."""
        self.stdout.write("\nDjango Settings Info:")
        self.stdout.write("=" * 30)
        
        installed_apps = getattr(settings, 'INSTALLED_APPS', [])
        app_related = [app for app in installed_apps if 'app' in app.lower() or app.startswith('apps.')]
        
        self.stdout.write("Relevant INSTALLED_APPS:")
        for app in app_related:
            self.stdout.write(f"  - {app}")
        
        # Show Python path
        self.stdout.write(f"\nPython Path (first 5 entries):")
        for i, path in enumerate(sys.path[:5]):
            self.stdout.write(f"  {i+1}. {path}")
        
        if len(sys.path) > 5:
            self.stdout.write(f"  ... and {len(sys.path) - 5} more entries")
