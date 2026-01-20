"""
Production WSGI application entry point.

Configures the application for deployment via WSGI-compatible servers.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airbnb.settings')

application = get_wsgi_application()
