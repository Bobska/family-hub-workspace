from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection
from django.conf import settings
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
import os

class Command(BaseCommand):
    help = 'Performs comprehensive health check of FamilyHub system'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('=== FamilyHub Health Check ===\n'))
        
        # Initialize counters
        passed_checks = 0
        total_checks = 5
        
        # 1. Check database connectivity
        self.stdout.write('1. Database Connectivity:')
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result:
                    self.stdout.write(self.style.SUCCESS('   ✓ Database connection successful'))
                    passed_checks += 1
                else:
                    self.stdout.write(self.style.ERROR('   ✗ Database query failed'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ✗ Database connection failed: {e}'))
        
        # 2. Count users in the system
        self.stdout.write('\n2. User Management:')
        try:
            user_count = User.objects.count()
            admin_count = User.objects.filter(is_superuser=True).count()
            active_count = User.objects.filter(is_active=True).count()
            
            self.stdout.write(self.style.SUCCESS(f'   ✓ Total users: {user_count}'))
            self.stdout.write(self.style.SUCCESS(f'   ✓ Admin users: {admin_count}'))
            self.stdout.write(self.style.SUCCESS(f'   ✓ Active users: {active_count}'))
            passed_checks += 1
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ✗ User query failed: {e}'))
        
        # 3. Verify static files directory exists
        self.stdout.write('\n3. Static Files Directory:')
        try:
            static_dirs = [
                (settings.BASE_DIR / 'static', 'Global static'),
                (settings.BASE_DIR / 'home' / 'static', 'Home app static'),
            ]
            
            all_static_exist = True
            for static_path, description in static_dirs:
                if os.path.exists(static_path):
                    self.stdout.write(self.style.SUCCESS(f'   ✓ {description}: {static_path}'))
                else:
                    self.stdout.write(self.style.ERROR(f'   ✗ {description}: {static_path} (missing)'))
                    all_static_exist = False
            
            if all_static_exist:
                passed_checks += 1
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ✗ Static files check failed: {e}'))
        
        # 4. Check if templates are loading correctly
        self.stdout.write('\n4. Template Loading:')
        try:
            templates_to_check = [
                'home/dashboard.html',
                'admin/base.html',  # Django admin template
            ]
            
            templates_loaded = True
            for template_name in templates_to_check:
                try:
                    template = get_template(template_name)
                    self.stdout.write(self.style.SUCCESS(f'   ✓ Template loaded: {template_name}'))
                except TemplateDoesNotExist:
                    self.stdout.write(self.style.ERROR(f'   ✗ Template missing: {template_name}'))
                    templates_loaded = False
            
            if templates_loaded:
                passed_checks += 1
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ✗ Template loading check failed: {e}'))
        
        # 5. Check media directory and settings
        self.stdout.write('\n5. Media Files Configuration:')
        try:
            media_root = getattr(settings, 'MEDIA_ROOT', settings.BASE_DIR / 'media')
            media_url = getattr(settings, 'MEDIA_URL', '/media/')
            
            if os.path.exists(media_root):
                self.stdout.write(self.style.SUCCESS(f'   ✓ Media root exists: {media_root}'))
                self.stdout.write(self.style.SUCCESS(f'   ✓ Media URL configured: {media_url}'))
                passed_checks += 1
            else:
                self.stdout.write(self.style.ERROR(f'   ✗ Media root missing: {media_root}'))
                self.stdout.write(self.style.WARNING(f'   ! Media URL: {media_url}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ✗ Media configuration check failed: {e}'))
        
        # Summary report
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('HEALTH CHECK SUMMARY:'))
        self.stdout.write(f'Checks passed: {passed_checks}/{total_checks}')
        
        if passed_checks == total_checks:
            self.stdout.write(self.style.SUCCESS('🎉 All systems operational! FamilyHub is healthy.'))
        elif passed_checks >= total_checks * 0.8:  # 80% or more
            self.stdout.write(self.style.WARNING('⚠️  Most systems operational. Minor issues detected.'))
        else:
            self.stdout.write(self.style.ERROR('🚨 Critical issues detected. System needs attention.'))
        
        self.stdout.write('='*50)
        
        # Return appropriate exit code
        if passed_checks < total_checks * 0.8:
            exit(1)  # Exit with error if too many checks failed
