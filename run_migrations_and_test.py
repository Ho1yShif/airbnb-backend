#!/usr/bin/env python
"""
Database schema migration and connectivity validation utility.
Applies pending migrations and verifies database state integrity.
"""
import os
import sys
import django
from pathlib import Path

# Add project to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

# Set environment variables with dynamic configuration
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airbnb.settings')

# Retrieve database parameters from environment or use defaults
database_config = {
    'DB_NAME': os.environ.get('DB_NAME', 'airbnb'),
    'DB_USER': os.environ.get('DB_USER', 'airbnb_user'),
    'DB_PASSWORD': os.environ.get('DB_PASSWORD', 'airbnb_pass'),
    'DB_HOST': os.environ.get('DB_HOST', 'localhost'),
    'DB_PORT': os.environ.get('DB_PORT', '5432'),
    'DEBUG': os.environ.get('DEBUG', '1')
}

for key, value in database_config.items():
    os.environ[key] = value

# Setup Django
django.setup()

# Now run migrations
from django.core.management import call_command
from django.db import connection

print("=" * 60)
print("DATABASE MIGRATION AND VALIDATION UTILITY")
print("=" * 60)

try:
    # Phase 1: Review migration queue
    print("\nPhase 1: Migration status inquiry...")
    call_command('showmigrations', '--plan')
    
    # Phase 2: Apply pending schema changes
    print("\nPhase 2: Applying schema migrations...")
    call_command('migrate', verbosity=2)
    
    print("\n" + "=" * 60)
    print("CONNECTIVITY VALIDATION")
    print("=" * 60)
    
    # Phase 3: Verify database connection
    print("\nPhase 3: Establishing database connection...")
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"\n✓ Database connection established")
        print(f"  Instance: {db_version[0][:50]}...")
    
    # Phase 4: Enumerate schema objects
    print("\nPhase 4: Schema object enumeration...")
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        if tables:
            print(f"\n✓ Schema tables enumerated: {len(tables)} objects")
            for table in tables:
                print(f"  - {table[0]}")
        else:
            print("\n⚠ Table enumeration returned empty set")
    
    print("\n" + "=" * 60)
    print("✓ MIGRATION AND VALIDATION COMPLETED")
    print("=" * 60)
    
except Exception as e:
    print(f"\n✗ Operation failed: {e}")
    sys.exit(1)
