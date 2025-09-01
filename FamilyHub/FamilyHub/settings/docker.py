from .base import *
import sys
from pathlib import Path

# Debug setting from environment
DEBUG = env.bool('DEBUG', default=False)

# Allowed hosts for Docker deployment
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1', '0.0.0.0'])

# Docker-compatible path resolution for standalone apps
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Add standalone apps to Python path for Docker environment
STANDALONE_APPS_DIR = Path('/app/standalone-apps')
if not STANDALONE_APPS_DIR.exists():
    # Fallback for local development
    STANDALONE_APPS_DIR = BASE_DIR.parent / 'standalone-apps'

if STANDALONE_APPS_DIR.exists():
    # Add timesheet app to Python path
    timesheet_path = STANDALONE_APPS_DIR / 'timesheet'
    if timesheet_path.exists() and str(timesheet_path) not in sys.path:
        sys.path.insert(0, str(timesheet_path))

# Database configuration for PostgreSQL 17
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB', default='familyhub_db'),
        'USER': env('POSTGRES_USER', default='familyhub_user'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST', default='db'),
        'PORT': env('POSTGRES_PORT', default='5432'),
        'CONN_MAX_AGE': 60,
        'OPTIONS': {
            'connect_timeout': 10,
        }
    }
}

# Deployment context flag for dual deployment strategy
IS_STANDALONE = False
