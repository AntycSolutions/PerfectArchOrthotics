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
# Get from file
SERVER_EMAIL = ''
# Get from file
DEFAULT_FROM_EMAIL = ''
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

# Get from file
DM = ''
DS = ''
PRACTITIONERS = ()

# Get from file
MOLL = ''
OOLI = ''
AROR = ''
LABORATORIES = ()

# Get from file
PAOI = ''
BILL_TO = ()
SHIP_TO = BILL_TO
