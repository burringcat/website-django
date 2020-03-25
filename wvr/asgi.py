"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os
import django
from channels.routing import get_default_application
from utils.utils.env import load_env
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wvr.settings")
load_env()
django.setup()
application = get_default_application()

