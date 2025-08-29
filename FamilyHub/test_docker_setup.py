#!/usr/bin/env python
"""
Test script to verify Docker production setup
"""

import os
import sys
import django
import requests

def test_docker_setup():
    """Test Docker production setup"""
    print("🔍 Testing Docker Production Setup")
    print("=" * 60)
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyHub.settings.docker')
    
    try:
        django.setup()
        print("✅ Django setup successful with docker settings")
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False
    
    # Test imports
    try:
        from home.health import HealthCheckView, ReadinessCheckView, LivenessCheckView
        print("✅ Health check views imported successfully")
    except Exception as e:
        print(f"❌ Health check import failed: {e}")
        return False
    
    # Test settings structure
    try:
        from django.conf import settings
        
        checks = [
            ('DATABASE ENGINE', settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql'),
            ('STATIC_ROOT', settings.STATIC_ROOT == '/app/staticfiles'),
            ('MEDIA_ROOT', settings.MEDIA_ROOT == '/app/media'),
            ('REDIS CACHE', 'redis' in settings.CACHES['default']['BACKEND'].lower()),
            ('HEALTH_CHECK', hasattr(settings, 'HEALTH_CHECK')),
            ('FAMILYHUB_SETTINGS', hasattr(settings, 'FAMILYHUB_SETTINGS')),
        ]
        
        print("\nSettings Configuration:")
        for check_name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}")
        
        all_passed = all(passed for _, passed in checks)
        
    except Exception as e:
        print(f"❌ Settings check failed: {e}")
        return False
    
    # Test environment variables
    print("\nEnvironment Variables:")
    env_vars = [
        'POSTGRES_DB',
        'POSTGRES_USER', 
        'POSTGRES_PASSWORD',
        'REDIS_URL',
        'SECRET_KEY',
        'ALLOWED_HOSTS'
    ]
    
    for var in env_vars:
        value = os.environ.get(var, 'NOT_SET')
        masked_value = '***' if 'password' in var.lower() or 'secret' in var.lower() else value
        print(f"   📝 {var}: {masked_value}")
    
    print(f"\n🎯 Docker Production Setup: {'READY' if all_passed else 'NEEDS ATTENTION'}")
    return all_passed

if __name__ == '__main__':
    success = test_docker_setup()
    sys.exit(0 if success else 1)
