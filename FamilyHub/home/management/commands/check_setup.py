from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Checks FamilyHub setup and configuration'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('=== FamilyHub Setup Check ==='))
        
        # Check settings
        self.stdout.write(f'DEBUG: {settings.DEBUG}')
        self.stdout.write(f'TIME_ZONE: {settings.TIME_ZONE}')
        
        # Check installed apps
        self.stdout.write('\nInstalled Apps:')
        for app in settings.INSTALLED_APPS:
            if 'django.contrib' not in app:
                self.stdout.write(f'  ✓ {app}')
        
        # Check database
        self.stdout.write(f'\nDatabase: {settings.DATABASES["default"]["ENGINE"]}')
        
        # Check directories
        dirs_to_check = [
            ('Templates', settings.BASE_DIR / 'home' / 'templates'),
            ('Static', settings.BASE_DIR / 'static'),
            ('Media', settings.BASE_DIR / 'media'),
        ]
        
        self.stdout.write('\nDirectories:')
        for name, path in dirs_to_check:
            if os.path.exists(path):
                self.stdout.write(self.style.SUCCESS(f'  ✓ {name}: {path}'))
            else:
                self.stdout.write(self.style.WARNING(f'  ✗ {name}: {path} (not found)'))
        
        self.stdout.write(self.style.SUCCESS('\n=== Setup Check Complete ==='))
