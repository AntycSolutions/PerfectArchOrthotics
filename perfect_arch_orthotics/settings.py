# perfect_arch_orthotics settings

import platform
from os import path

# Django settings

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

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
    'session_security',
    'multiselectfield',
    'django_js_reverse',
    'django_twilio',
)
LOCAL_APPS = (
    'clients',
    'inventory',
    'reminders',
)
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

DJANGO_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.template.context_processors.debug',
    'django.template.context_processors.i18n',
    'django.template.context_processors.media',
    'django.template.context_processors.static',
    'django.template.context_processors.tz',
    'django.template.context_processors.request',
    'django.contrib.messages.context_processors.messages',
]
LOCAL_CONTEXT_PROCESSORS = [
    'perfect_arch_orthotics.context_processors.site',
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors':
                DJANGO_CONTEXT_PROCESSORS + LOCAL_CONTEXT_PROCESSORS,
        },
    },
]

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
    path.join(BASE_DIR, "assets"),
)

# Media files (user uploaded)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR + '/media/'

LOGIN_REDIRECT_URL = '/'

# Email
EMAIL_USE_TLS = True

password_validation = 'django.contrib.auth.password_validation.'
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': password_validation + 'UserAttributeSimilarityValidator'},
    {'NAME': password_validation + 'MinimumLengthValidator'},
    {'NAME': password_validation + 'CommonPasswordValidator'},
    {'NAME': password_validation + 'NumericPasswordValidator'},
]

# Third Party

# Django Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Django Ajax Selects
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
PIPELINE = {
    # if there are multiple source_filesnames and DEBUG = True
    #  we need to define debug_keys to keep fallback key unique
    'STYLESHEETS': {
        # templates
        'base': {
            'source_filenames': (
                'css/sticky-footer.css',
                'css/base.css',
                'session_security/style.css',
            ),
            'output_filename': 'css/base_all.css',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'base_all_css',
                'debug_fallback_keys': {
                    STATIC_URL + 'css/sticky-footer.css': 'sticky_footer_css',
                    STATIC_URL + 'css/base.css': 'base_css',
                    STATIC_URL + 'session_security/style.css': 'style_css',
                },
            },
        },
        'index': {
            'source_filenames': (
                'css/index.css',
            ),
            'output_filename': 'css/index_all.css',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'index_all_css',
            },
        },
        # clients
        'biomechanical_foot': {
            'source_filenames': (
                'clients/css/biomechanical_foot.css',
            ),
            'output_filename': 'css/biomechanical_foot_all.css',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
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
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'biomechanical_gait_all_css',
                'debug_fallback_keys': {
                    STATIC_URL + 'clients/css/biomechanical_gait.css':
                        'biomechanical_gait_css',
                    STATIC_URL + 'utils/css/typeahead.css': 'typeahead_css',
                },
            },
        },
        'insurance': {
            'source_filenames': (
                'clients/css/insurance.css',
            ),
            'output_filename': 'css/insurance_all.css',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'insurance_all_css',
            },
        },
        'client': {
            'source_filenames': (
                'clients/css/client.css',
                'clients/css/form-static.css',
                'clients/css/anchor.css',
            ),
            'output_filename': 'css/client_all.css',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'client_all_css',
                'debug_fallback_keys': {
                    STATIC_URL + 'clients/css/client.css': 'client_css',
                    STATIC_URL + 'clients/css/form-static.css':
                        'form_static_css',
                    STATIC_URL + 'clients/css/anchor.css': 'anchor_css',
                },
            },
        },
        'claim': {
            'source_filenames': (
                'clients/css/form-static.css',
            ),
            'output_filename': 'css/claim_all.css',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'claim_all_css',
            },
        },
        # reminders
        'reminders': {
            'source_filenames': (
                'utils/css/typeahead.css',
            ),
            'output_filename': 'css/reminders_all.css',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'reminders_all_css',
            },
        },
    },
    'JAVASCRIPT': {
        'base': {
            'source_filenames': (
                'session_security/script.js',
            ),
            'output_filename': 'js/base_all.js',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'base_all_js',
            },
        },
        # clients
        'insurance': {
            'source_filenames': (
                'clients/js/insurance.js',
            ),
            'output_filename': 'js/insurance_all.js',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'insurance_all_js',
            },
        },
        'claims': {
            'source_filenames': (
                'utils/jquery_utils/ajax.js',
            ),
            'output_filename': 'js/claims_all.js',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'claims_all_js',
            },
        },
        # inventory
        'coverage_order': {
            'source_filenames': (
                'inventory/js/coverage_order.js',
            ),
            'output_filename': 'js/coverage_order_all.js',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'coverage_order_all_js',
            },
        },
        # reminders
        'reminders': {
            'source_filenames': (
                'utils/jquery_utils/ajax.js',
            ),
            'output_filename': 'js/reminders_all.js',
            'template_name': 'utils/snippets/pipeline_fallback_css_js.html',
            'extra_context': {
                'fallback_key': 'reminders_all_js',
            },
        },
    },
}
system = platform.system()
if system == 'Windows':
    yuglify = 'yuglify.cmd'
elif system == 'Linux':
    yuglify = 'yuglify'
else:
    raise Exception('Unknown platform.system')
PIPELINE['YUGLIFY_BINARY'] = (
    path.normpath(
        path.join(BASE_DIR, '../node_modules/.bin/' + yuglify)
    )
)

# Project

PROFILING = False

VERSIONS = {
    'bootswatch_cerulean_css': '3.3.6',
    'typeahead_js': '0.11.1',
}

# import environment aware settings
if path.isfile(path.join(BASE_DIR, "../prod")):
    from .configs.prod_settings import *
    ENV = 'prod'
elif path.isfile(path.join(BASE_DIR, "../test")):
    from .configs.test_settings import *
    ENV = 'test'
elif path.isfile(path.join(BASE_DIR, "../devl")):
    from .configs.devl_settings import *
    ENV = 'devl'
else:
    raise Exception("Please create a settings decision file.")

if DEBUG:
    # Django Debug Toolbar
    INSTALLED_APPS += ('debug_toolbar',)

    MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
    MIDDLEWARE_CLASSES.insert(
        5, 'debug_toolbar.middleware.DebugToolbarMiddleware'
    )
    MIDDLEWARE_CLASSES = tuple(MIDDLEWARE_CLASSES)

    if ENV != 'devl':
        def show_toolbar(request):
            return (
                hasattr(request, 'user') and
                not request.is_ajax() and
                request.user.is_staff
            )
        DEBUG_TOOLBAR_CONFIG.update({
            'SHOW_TOOLBAR_CALLBACK':
                'perfect_arch_orthotics.settings.show_toolbar',
        })
    else:
        INTERNAL_IPS = ['127.0.0.1']

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

if ENV != 'devl':
    # Django Session Security
    MIDDLEWARE_CLASSES += (
        'session_security.middleware.SessionSecurityMiddleware',
    )
