from .base import *

# Use the INSTALLED_APPS from base.py (includes integrated apps)
# No override needed - let base.py handle app discovery

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Deployment context flag for dual deployment strategy
IS_STANDALONE = False
