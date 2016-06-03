# perfect_arch_orthotics settings

# Django

import os
import platform

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

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
    'crispy_forms',
    'auditlog',
    'utils',
    'accounts',
    'pipeline',
)
LOCAL_APPS = (
    'clients',
    'inventory',
)
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

DJANGO_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.template.context_processors.debug",
    "django.template.context_processors.i18n",
    "django.template.context_processors.media",
    "django.template.context_processors.static",
    "django.template.context_processors.tz",
    "django.template.context_processors.request",
    "django.contrib.messages.context_processors.messages",
]
LOCAL_CONTEXT_PROCESSORS = [
    "perfect_arch_orthotics.context_processors.site",
]
TEMPLATE_CONTEXT_PROCESSORS = (
    DJANGO_CONTEXT_PROCESSORS + LOCAL_CONTEXT_PROCESSORS
)

DJANGO_MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
THIRD_PARTY_MIDDLEWARE = (
    'auditlog.middleware.AuditlogMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',
)
LOCAL_MIDDLEWARE = (
    'middleware.active_users.ActiveUserMiddleware',
    'utils.middleware.exception.ExceptionUserInfoMiddleware',
)
MIDDLEWARE_CLASSES = (
    DJANGO_MIDDLEWARE + THIRD_PARTY_MIDDLEWARE + LOCAL_MIDDLEWARE
)

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

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# Email
EMAIL_USE_TLS = True

# Third Party

# Django Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Django Ajax  Selects
AJAX_LOOKUP_CHANNELS = {
    'shoe': ('inventory.lookups', 'ShoeLookup'),
}

# Django Utils
UTILS = {
    'fallback': True,
    'bootstrap3': True,
    'font_awesome': True,
    'jquery_ui': True,
    'pipeline': True,
}

# Django Debug Toolbar
DEBUG_TOOLBAR_PANELS = [
    # defaults
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    # 'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_COLLAPSED': True,
}

# Django Pipeline
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
# STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#     'pipeline.finders.CachedFileFinder',
#     'pipeline.finders.PipelineFinder',
# )
PIPELINE = {
    'STYLESHEETS': {
        'base': {
            'source_filenames': (
                'css/sticky-footer.css',
                'css/base.css',
            ),
            'output_filename': 'css/base_all.css',
            'template_name': 'pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'base_all_css',
            },
        },
        'index': {
            'source_filenames': (
                'css/index.css',
            ),
            'output_filename': 'css/index_all.css',
            'template_name': 'pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'index_all_css',
            },
        },
        'biomechanical_foot': {
            'source_filenames': (
                'clients/css/biomechanical_foot.css',
            ),
            'output_filename': 'css/biomechanical_foot_all.css',
            'template_name': 'pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'biomechanical_foot_all_css',
            },
        },
        'biomechanical_gait': {
            'source_filenames': (
                'clients/css/biomechanical_gait.css',
                'utils/css/typeahead.css',
            ),
            'output_filename': 'css/biomechanical_gait_all.css',
            'template_name': 'pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'biomechanical_gait_all_css',
            },
        },
        'insurance': {
            'source_filenames': (
                'clients/css/insurance.css',
            ),
            'output_filename': 'css/insurance_all.css',
            'template_name': 'pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'insurance_all_css',
            },
        },
    },
    'JAVASCRIPT': {
        'insurance': {
            'source_filenames': (
                'clients/js/insurance.js',
            ),
            'output_filename': 'js/insurance_all.js',
            'template_name': 'pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'insurance_all_js',
            },
        },
    },
}
system = platform.system()
if system == 'Windows':
    PIPELINE['YUGLIFY_BINARY'] = (
        os.path.normpath(
            os.path.join(BASE_DIR, '../node_modules/.bin/yuglify.cmd')
        )
    )
elif system == 'Linux':
    PIPELINE['YUGLIFY_BINARY'] = (
        os.path.normpath(
            os.path.join(BASE_DIR, '../node_modules/.bin/yuglify')
        )
    )
else:
    raise Exception('Unknown platform.system')

# Project

PROFILING = False

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
        if (
            hasattr(request, 'user') and not request.is_ajax() and
                request.user.is_staff):
            return True
        return False
    DEBUG_TOOLBAR_CONFIG.update({
        'SHOW_TOOLBAR_CALLBACK':
            'perfect_arch_orthotics.settings.show_toolbar',
    })
elif os.path.isfile(os.path.join(BASE_DIR, "../devl")):
    from .configs.devl_settings import *

    INSTALLED_APPS += ('debug_toolbar',)
else:
    raise Exception("Please create a settings decision file.")

if PROFILING:
    INSTALLED_APPS += (
        'template_profiler_panel',
        'template_timings_panel',
    )

    DEBUG_TOOLBAR_PANELS += [
        # built in
        'debug_toolbar.panels.profiling.ProfilingPanel',
        # third party
        'template_profiler_panel.panels.template.TemplateProfilerPanel',
        'template_timings_panel.panels.TemplateTimings.TemplateTimings',
    ]
