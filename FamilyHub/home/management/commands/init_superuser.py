"""
Django management command to initialize superuser for FamilyHub.

This command checks if any superuser exists and creates one using
environment variables if none exist. It handles IntegrityError
gracefully and provides clear feedback.
"""

import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Initialize superuser for FamilyHub using environment variables'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force creation even if superusers exist',
        )

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Get superuser credentials from environment
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@familyhub.local')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
        
        # Check if any superuser exists
        superuser_exists = User.objects.filter(is_superuser=True).exists()
        
        if superuser_exists and not options['force']:
            existing_superusers = User.objects.filter(is_superuser=True).values_list('username', flat=True)
            self.stdout.write(
                self.style.WARNING(
                    f'Superuser(s) already exist: {", ".join(existing_superusers)}. '
                    'Skipping superuser creation. Use --force to create anyway.'
                )
            )
            return
        
        # Check if the specific username already exists
        if User.objects.filter(username=username).exists():
            existing_user = User.objects.get(username=username)
            if existing_user.is_superuser:
                self.stdout.write(
                    self.style.WARNING(
                        f'Superuser "{username}" already exists. Skipping creation.'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'User "{username}" exists but is not a superuser. '
                        'Cannot create superuser with same username.'
                    )
                )
            return
        
        # Validate required fields
        if not username or not email or not password:
            raise CommandError(
                'Missing required environment variables: '
                'DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD'
            )
        
        try:
            # Create the superuser
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Superuser "{username}" created successfully!'
                )
            )
            
            # Log details for debugging (without password)
            self.stdout.write(f'  Username: {username}')
            self.stdout.write(f'  Email: {email}')
            self.stdout.write(f'  Superuser status: {user.is_superuser}')
            self.stdout.write(f'  Staff status: {user.is_staff}')
            
        except IntegrityError as e:
            self.stdout.write(
                self.style.WARNING(
                    f'Superuser "{username}" already exists (IntegrityError handled gracefully)'
                )
            )
            
        except Exception as e:
            raise CommandError(f'Error creating superuser: {str(e)}')
