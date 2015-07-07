# Prod settings

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
# Get from file
SECRET_KEY = ''

DEBUG = False
TEMPLATE_DEBUG = DEBUG

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

# # Get from file
EMAIL_HOST_USER = ''
# # Get from file
EMAIL_HOST_PASSWORD = ''

EMAIL_SUBJECT_PREFIX = '[Perfect Arch Orthotics] '

# Cache templates
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader',
        ('django.template.loaders.filesystem.Loader',
         'django.template.loaders.app_directories.Loader',)
     ),
)

# HTTPS/SSL
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
os.environ['wsgi.url_scheme'] = 'https'
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 15768000
