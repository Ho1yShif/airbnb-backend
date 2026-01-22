import os
import sys
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airbnb.settings')
for env_key in ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT']:
    if env_key not in os.environ:
        os.environ[env_key] = ''

import django
django.setup()

from django.core.management import call_command
from django.db import connection

print(f"Database Integration Verification - {Path(__file__).name}")
print("-" * 60)

try:
    print("\nInitiating database schema validation...")
    call_command('migrate', verbosity=0)
    
    print("\nVerifying database connectivity...")
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
    print(f"Connected to PostgreSQL instance")
    
    print("\nValidating database schema objects...")
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        "