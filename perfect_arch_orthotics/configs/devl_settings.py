# Devl settings

# django settings

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
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

ADMINS = (('Andrew', 'andrew.charles@antyc.ca'),)
MANAGERS = ADMINS

EMAIL_SUBJECT_PREFIX = '[Perfect Arch Orthotics - Devl] '
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SERVER_EMAIL = 'Perfect Arch <root@localhost>'
DEFAULT_FROM_EMAIL = 'Perfect Arch <no-reply@localhost>'
# For actual emails
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST_USER = 'devlperfectarchorthotics'
# EMAIL_HOST_PASSWORD = 'devldjangosendgrid3'
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_PORT = 587

# local app settings

DM = 'dm'
DS = 'ds'
PRACTITIONERS = (
    (DM, 'D. Mu C.Ped.'),
    (DS, 'Dr. Sefcik D.P.M.'),
)

MOLL = 'moll'
OOLI = 'ooli'
AROR = 'aror'
LABORATORIES = (
    (
        MOLL,
        'MA Orthotics Laboratory Ltd'
        '\n11975 W Sample Rd'
        '\nCoral Springs, FL  331000'
        '\nUSA'
        '\nPhone: (754) 206-6110'
        '\nFax: (754) 206-6109'
        '\nLaboratory Supervisor: M. Asam C.Ped.'
    ),
    (
        OOLI,
        'OOLab Inc.'
        '\n42 Niagara St'
        '\nHamilton, ON  L8L 6A2'
        '\nCanada'
        '\nToll Free: 1-888-873-3316'
        '\nPhone: (905) 521-1230'
        '\nFax: (905) 521-1210'
        '\nEmail: info@oolab.com'
        '\nLaboratory Supervisor: A. Boyle'
    ),
    (
        AROR,
        'Ares Orthotics'
        '\n107 Ave SE'
        '\nCalgary, AB  T2Z 3R7'
        '\nCanada'
        '\nPhone: (403) 398-5629'
        '\nFax: (403) 398-5635'
        '\nEmail: acct@aresorthotics.com'
        '\nLaboratory Supervisor: B. Domosky'
    ),
)

PAOI = 'paoi'
BILL_TO = (
    (
        PAOI,
        'The Perfect Arch Orthotics Inc.'
        '\n10540 - 169 St.'
        '\nEdmonton, AB  T5P 3X6'
        '\nCanada'
        '\nPhone: (587) 400-4588'
        '\nFax: (587) 400-4566'
    ),
)
SHIP_TO = BILL_TO

DANNY_EMAIL = 'danny@perfectarch.ca'
