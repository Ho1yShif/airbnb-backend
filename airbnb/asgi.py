"""
Asynchronous WSGI application entry point.

Configures the application for deployment via ASGI-compatible servers.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airbnb.settings')

application = get_asgi_application()
