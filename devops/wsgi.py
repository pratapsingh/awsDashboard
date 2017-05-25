"""
WSGI config for devops project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os, sys
sys.path.append('/app/devops')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "devops.settings")

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "devops.settings")

application = get_wsgi_application()