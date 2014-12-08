# Prod settings

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
# Get from file
SECRET_KEY = ''

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['perfectarch.ca']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # Get from file
        'NAME': '',
        # Get from file
        'USER': '',
        # Get from file
        'PASSWORD': '',
        'HOST': 'localhost'
    }
}

# Get from file
ADMINS = ()

# Get from file
DM = ''
PRACTITIONERS = ()

# Get from file
MOLL = ''
LABORATORIES = ()

# Get from file
PAOI = ''
BILL_TO = ()

SHIP_TO = BILL_TO

# # Get from file
# EMAIL_HOST_USER = ''
# # Get from file
# EMAIL_HOST_PASSWORD = ''

# EMAIL_SUBJECT_PREFIX = '[Perfect Arch Orthotics]'
