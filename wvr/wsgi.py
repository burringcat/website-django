"""
WSGI config for wvr project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from utils.utils.env import load_env

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wvr.settings')
load_env()
application = get_wsgi_application()
