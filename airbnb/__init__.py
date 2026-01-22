"""
AirBnB Backend Django Application

Author: Martin Mawien
Copyright (c) 2026 Martin Mawien
GitHub: https://github.com/Martin-Mawien/airbnb-backend
"""

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)
