"""
Django management command to sync standalone apps with FamilyHub integration.

Usage:
    python manage.py sync_app timesheet --method symlink
    python manage.py sync_app timesheet --method copy
    python manage.py sync_app all --method symlink
"""

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from FamilyHub.app_registry import app_registry
import sys
from pathlib import Path


class Command(BaseCommand):
    help = 'Sync standalone apps with FamilyHub integration'

    def add_arguments(self, parser):
        parser.add_argument(
            'app_name',
            type=str,
            help='Name of the app to sync (or "all" for all apps)'
        )
        parser.add_argument(
            '--method',
            type=str,
            choices=['symlink', 'copy'],
            default='symlink',
            help='Sync method: symlink (default) or copy'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force sync even if target already exists'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without actually doing it'
        )

    def handle(self, *args, **options):
        app_name = options['app_name']
        method = options['method']
        force = options['force']
        dry_run = options['dry_run']

        self.stdout.write(self.style.SUCCESS('FamilyHub App Sync Tool'))
        self.stdout.write('=' * 50)

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - No changes will be made'))

        # Check if Windows and method is symlink
        if sys.platform == 'win32' and method == 'symlink':
            self.stdout.write(
                self.style.WARNING(
                    'Warning: Symbolic links on Windows may require admin privileges.\n'
                    'If this fails, try running as administrator or use --method copy'
                )
            )

        if app_name == 'all':
            self.sync_all_apps(method, force, dry_run)
        else:
            self.sync_single_app(app_name, method, force, dry_run)

    def sync_all_apps(self, method, force, dry_run):
        """Sync all available standalone apps."""
        statuses = app_registry.get_all_app_statuses()
        
        for app_key, status in statuses.items():
            if status['standalone_exists']:
                self.stdout.write(f"\n--- Syncing {app_key} ---")
                self.sync_single_app(app_key, method, force, dry_run)
            else:
                self.stdout.write(
                    self.style.WARNING(f"Skipping {app_key}: No standalone version found")
                )

    def sync_single_app(self, app_name, method, force, dry_run):
        """Sync a single app."""
        if app_name not in app_registry.known_apps:
            raise CommandError(f"Unknown app: {app_name}")

        status = app_registry.get_app_status(app_name)
        
        self.stdout.write(f"App: {app_name}")
        self.stdout.write(f"Method: {method}")
        
        # Show current status
        self.stdout.write(f"Current status: {status['status']}")
        self.stdout.write(f"Standalone exists: {status['standalone_exists']}")
        self.stdout.write(f"Integrated exists: {status['integrated_exists']}")
        
        if status['integrated_exists']:
            self.stdout.write(f"Is symlink: {status['is_symlink']}")

        # Check if we can proceed
        if not status['standalone_exists']:
            self.stdout.write(
                self.style.ERROR(f"Cannot sync {app_name}: Standalone version not found")
            )
            return

        if status['integrated_exists'] and not force:
            self.stdout.write(
                self.style.WARNING(
                    f"Integrated version already exists. Use --force to overwrite."
                )
            )
            return

        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Would sync {app_name} using {method} method"
                )
            )
            return

        # Perform the sync
        self.stdout.write(f"Syncing {app_name}...")
        
        try:
            success = app_registry.sync_app(app_name, method)
            
            if success:
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Successfully synced {app_name}")
                )
                
                # Verify the sync
                new_status = app_registry.get_app_status(app_name)
                if new_status['available']:
                    self.stdout.write(
                        self.style.SUCCESS(f"✅ App is now available for integration")
                    )
                    
                    # Show next steps
                    self.stdout.write("\nNext steps:")
                    self.stdout.write("1. Run migrations if needed:")
                    self.stdout.write(f"   python manage.py makemigrations {app_registry.known_apps[app_name]['app_module']}")
                    self.stdout.write("   python manage.py migrate")
                    self.stdout.write("2. Restart the Django server")
                    self.stdout.write(f"3. Visit /{app_name}/ to test the integration")
                else:
                    self.stdout.write(
                        self.style.WARNING(f"⚠️  Sync completed but app may not be fully functional")
                    )
            else:
                self.stdout.write(
                    self.style.ERROR(f"❌ Failed to sync {app_name}")
                )
        
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Error syncing {app_name}: {str(e)}")
            )
            
            # Provide troubleshooting tips
            if sys.platform == 'win32' and method == 'symlink':
                self.stdout.write(
                    self.style.WARNING(
                        "\nTroubleshooting tips for Windows:\n"
                        "1. Run PowerShell/Command Prompt as Administrator\n"
                        "2. Or try using --method copy instead\n"
                        "3. Or enable Developer Mode in Windows Settings"
                    )
                )

    def show_app_info(self, app_name):
        """Show detailed information about an app."""
        status = app_registry.get_app_status(app_name)
        config = app_registry.known_apps[app_name]
        
        self.stdout.write(f"\n--- {config['name']} ---")
        self.stdout.write(f"Description: {config['description']}")
        self.stdout.write(f"Django Module: {config['app_module']}")
        self.stdout.write(f"Standalone Path: {status['standalone_path']}")
        self.stdout.write(f"Integrated Path: {status['integrated_path']}")
        self.stdout.write(f"Status: {status['status']}")
        self.stdout.write(f"Available: {status['available']}")
        self.stdout.write(f"URLs Available: {status['urls_available']}")
