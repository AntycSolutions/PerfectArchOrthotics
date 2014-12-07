# Devl settings

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
# Get from file
SECRET_KEY = 'e#v=c7*5@x1qnp*tfke!f#+nd_amito34d%blwm)!8&@4u7=+y'

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

# Get from file
PRACTITIONERS = ()

# Get from file
LABORATORIES = ()

# Get from file
BILL_TO = ()

SHIP_TO = BILL_TO

# Get from file
# EMAIL_HOST_USER = ''
# Get from file
# EMAIL_HOST_PASSWORD = ''

# EMAIL_SUBJECT_PREFIX = '[Perfect Arch Orthotics - Devl]'
