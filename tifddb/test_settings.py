"""
test_settings.py — overrides for running the test suite without MySQL.

Usage:
    python manage.py test camp --settings=tifddb.test_settings
"""
from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Speed up password hashing in tests
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']

# Suppress logging noise during tests
LOGGING = {}

# Paypal test mode
PAYPAL_TEST = True
PAYPAL_RECEIVER_EMAIL = 'payments@tifd.org'
