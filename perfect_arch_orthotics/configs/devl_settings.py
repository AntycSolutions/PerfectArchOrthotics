# Devl settings

# django settings

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
# Get from file
SECRET_KEY = ''

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Get from file
ADMINS = ()
MANAGERS = ADMINS

EMAIL_SUBJECT_PREFIX = '[Perfect Arch Orthotics - Devl] '
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SERVER_EMAIL = 'Perfect Arch <root@localhost>'
DEFAULT_FROM_EMAIL = 'Perfect Arch <no-reply@localhost>'
# For actual emails
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Get from file
# EMAIL_HOST_USER = ''
# Get from file
# EMAIL_HOST_PASSWORD = ''
# Get from file
# EMAIL_HOST = ''
# Get from file
# EMAIL_PORT = ''

# local app settings

DM = 'dm'
DS = 'ds'
# Get from file
PRACTITIONERS = ()

MOLL = 'moll'
OOLI = 'ooli'
AROR = 'aror'
PAOI = 'paoi'
# Get from file
LABORATORIES = ()

PAOI = 'paoi'
# Get from file
BILL_TO = ()
SHIP_TO = BILL_TO

# Get from file
DANNY_EMAIL = ''
