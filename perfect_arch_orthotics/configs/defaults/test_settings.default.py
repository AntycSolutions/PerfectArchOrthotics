# Test settings

# django settings

from os import path

BASE_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

# SECURITY WARNING: keep the secret key used in production secret!
# Get from file
SECRET_KEY = ''

DEBUG = True

# Get from file
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        # Get from file
        'ENGINE': '',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': ''
    }
}

# Get from file
ADMINS = ()
MANAGERS = ADMINS

EMAIL_SUBJECT_PREFIX = '[Test - Perfect Arch] '
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Get from file
SERVER_EMAIL = ''
# Get from file
DEFAULT_FROM_EMAIL = ''
# For actual emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Get from file
EMAIL_HOST_USER = ''
# Get from file
EMAIL_HOST_PASSWORD = ''
# Get from file
EMAIL_HOST = ''
# Get from file
EMAIL_PORT = ''

# Cache templates
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader',
        ('django.template.loaders.filesystem.Loader',
         'django.template.loaders.app_directories.Loader',)
     ),
)

# local app settings

# Get from file
DM = ''
DS = ''
PRACTITIONERS = ()

# Get from file
MOLL = ''
AROR = ''
PAOI = ''
LABORATORIES = ()

# Get from file
PAOI = ''
BILL_TO = ()
