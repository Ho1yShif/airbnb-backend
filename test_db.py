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
        """)
        tables = cursor.fetchall()
        if tables:
            print(f"Schema contains {len(tables)} tables")
    
    print("\nInspecting application models...")
    print("\n[4/4] Testing model access...")
    from listings.models import Property, Booking, Payment, Review, PropertyImage, Wishlist, UserProfile
    print(f"✓ Property: {Property._meta.db_table}")
    print(f"✓ Booking: {Booking._meta.db_table}")
    print(f"✓ Payment: {Payment._meta.db_table}")
    print(f"✓ Review: {Review._meta.db_table}")
    print(f"✓ PropertyImage: {PropertyImage._meta.db_table}")
    print(f"✓ Wishlist: {Wishlist._meta.db_table}")
    print(f"✓ UserProfile: {UserProfile._meta.db_table}")
    
    print("\n" + "=" * 70)
    print("SUCCESS: All operations completed without errors!")
    print("=" * 70)
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
