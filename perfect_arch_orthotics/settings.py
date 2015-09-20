# perfect_arch_orthotics settings

# django settings

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Application definition
DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)
THIRD_PARTY_APPS = (
    'easy_pdf',
    'bootstrap3_datetime',
    'ajax_select',
)
LOCAL_APPS = (
    'utils',
    'clients',
    'inventory',
)
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# middleware
DJANGO_MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
LOCAL_MIDDLEWARE = (
    'middleware.active_users.ActiveUserMiddleware',
)
MIDDLEWARE_CLASSES = DJANGO_MIDDLEWARE + LOCAL_MIDDLEWARE

ROOT_URLCONF = 'perfect_arch_orthotics.urls'

WSGI_APPLICATION = 'perfect_arch_orthotics.wsgi.application'

# Internationalization
TIME_ZONE = 'America/Edmonton'
USE_I18N = False
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR + '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "assets"),
)

# Media files (user uploaded)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR + '/media/'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# Email
EMAIL_USE_TLS = True

# third party app settings

AJAX_LOOKUP_CHANNELS = {
    'shoe': ('inventory.lookups', 'ShoeLookup'),
}

# import environment aware settings
if os.path.isfile(os.path.join(BASE_DIR, "../prod")):
    from .configs.prod_settings import *
elif os.path.isfile(os.path.join(BASE_DIR, "../test")):
    from .configs.test_settings import *

    INSTALLED_APPS += ('debug_toolbar',)
    MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
    MIDDLEWARE_CLASSES.insert(
        5, 'debug_toolbar.middleware.DebugToolbarMiddleware'
    )
    MIDDLEWARE_CLASSES = tuple(MIDDLEWARE_CLASSES)

    def show_toolbar(request):
        if (hasattr(request, 'user') and not request.is_ajax()
                and request.user.is_staff):
            return True
        return False
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK':
            'perfect_arch_orthotics.settings.show_toolbar',
        'SHOW_COLLAPSED': True,
    }
elif os.path.isfile(os.path.join(BASE_DIR, "../devl")):
    from .configs.devl_settings import *

    INSTALLED_APPS += ('debug_toolbar',)
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_COLLAPSED': True,
    }
else:
    raise Exception("Please create a settings decision file.")
