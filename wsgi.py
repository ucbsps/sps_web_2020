"""
WSGI config for app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

print(os.getcwd(), file=sys.stderr)

if os.getcwd().split('/').pop(-1) == 'sps':
    print('Setting to settings_debug', file=sys.stderr)
    os.environ["DJANGO_SETTINGS_MODULE"] = "settings_debug"

print(os.environ, file=sys.stderr)

application = get_wsgi_application()
