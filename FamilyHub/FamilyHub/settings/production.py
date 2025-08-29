"""
Production Django settings for FamilyHub project.
"""

from .docker import *
from celery.schedules import crontab

# Production-specific overrides
DEBUG = False

# Stricter security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Additional production security
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'

# Production logging
LOGGING['handlers']['file']['level'] = 'ERROR'
LOGGING['loggers']['django']['level'] = 'WARNING'

# Performance optimizations
CONN_MAX_AGE = 600

# Production cache settings
CACHES['default']['TIMEOUT'] = 3600  # 1 hour default cache

# Session Configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = 86400  # 24 hours

# Celery Configuration for Production
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/1')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379/1')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True

# Celery Beat Schedule
CELERY_BEAT_SCHEDULE = {
    'cleanup-sessions': {
        'task': 'FamilyHub.celery.cleanup_old_sessions',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
    },
    'generate-reports': {
        'task': 'FamilyHub.celery.generate_reports',
        'schedule': crontab(hour=6, minute=0, day_of_week=1),  # Weekly on Monday at 6 AM
    },
    'backup-database': {
        'task': 'FamilyHub.celery.backup_database',
        'schedule': crontab(hour=3, minute=0),  # Daily at 3 AM
    },
    'health-check': {
        'task': 'FamilyHub.celery.health_check',
        'schedule': 300.0,  # Every 5 minutes
    },
}

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
