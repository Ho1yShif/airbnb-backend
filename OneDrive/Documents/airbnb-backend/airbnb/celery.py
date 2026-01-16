"""
Celery configuration for AirBnB Backend project.

Author: Martin Mawien
Copyright (c) 2026 Martin Mawien
GitHub: https://github.com/Martin-Mawien/airbnb-backend
"""
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airbnb.settings')

app = Celery('airbnb')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
