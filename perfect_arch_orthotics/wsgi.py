"""
WSGI config for perfect_arch_orthotics project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import sys
from os import path, environ

from django.core.wsgi import get_wsgi_application


BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

# This is required in prod
sys.path.append(BASE_DIR)

environ.setdefault("DJANGO_SETTINGS_MODULE", "perfect_arch_orthotics.settings")

if path.isfile(path.join(BASE_DIR, "../prod")):
    environ['HTTPS'] = "on"


application = get_wsgi_application()
