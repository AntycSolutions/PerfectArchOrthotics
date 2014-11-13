"""
WSGI config for perfect_arch_orthotics project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
base_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_dir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "perfect_arch_orthotics.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
