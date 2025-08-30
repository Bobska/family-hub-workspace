from .base import *

# Debug setting from environment
DEBUG = env.bool('DEBUG', default=False)

# Allowed hosts for Docker deployment
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1', '0.0.0.0'])

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
