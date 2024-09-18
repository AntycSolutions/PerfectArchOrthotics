# Devl settings

from os import path

from ..settings import *

# Django settings

BASE_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

# SECURITY WARNING: keep the secret key used in production secret!
# Get from file
SECRET_KEY = ''

DEBUG = True

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

EMAIL_SUBJECT_PREFIX = '[Devl - Perfect Arch] '
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

# third party settings

# Django Session Security
SESSION_SECURITY_INSECURE = True

# local app settings

DM = 'dm'
DS = 'ds'
# Get from file
PRACTITIONERS = ()

MOLL = 'moll'
AROR = 'aror'
PAOI = 'paoi'
# Get from file
LABORATORIES = ()

PAOI = 'paoi'
# Get from file
BILL_TO = ()

# Get from file
DANNY_EMAIL = ''
