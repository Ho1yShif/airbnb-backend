#!/usr/bin/env python
"""
Professional Backend Validation Script
Checks all critical components of the AirBnB backend
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airbnb.settings')
sys.path.insert(0, str(Path(__file__).parent))

django.setup()

from django.core.management import call_command
from django.db import connections
from django.apps import apps
from django.core.checks import run_checks

print("=" * 80)
print("AIRBNB BACKEND VALIDATION REPORT")
print("=" * 80)

# 1. System Checks
print("\n[1] Running Django System Checks...")
issues = run_checks()
if issues:
    for issue in issues:
        if issue.is_serious():
            print(f"  ❌ {issue.level}: {issue.msg}")
        else:
            print(f"  ⚠️  {issue.level}: {issue.msg}")
else:
    print("  ✅ All system checks passed")

# 2. Database Connection
print("\n[2] Checking Database Connection...")
try:
    connection = connections['default']
    cursor = connection.cursor()
    cursor.execute("SELECT 1")
    print("  ✅ Database connection successful")
except Exception as e:
    print(f"  ❌ Database connection failed: {e}")

# 3. Installed Apps
print("\n[3] Checking Installed Apps...")
apps_config = apps.get_app_configs()
for app in apps_config:
    status = "✅" if app.ready else "⚠️ "
    print(f"  {status} {app.name}")

# 4. Models
print("\n[4] Checking Models...")
for app in apps_config:
    models = apps.get_models(app)
    if models:
        print(f"  {app.name}:")
        for model in models:
            fields = [f.name for f in model._meta.fields]
            print(f"    ✅ {model.__name__} ({len(fields)} fields)")

# 5. Migrations
print("\n[5] Checking Migration Status...")
try:
    from django.db.migrations.executor import MigrationExecutor
    executor = MigrationExecutor(connections['default'])
    
    # Get all migrations
    plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
    
    if plan:
        print(f"  ⚠️  {len(plan)} migration(s) pending:")
        for migration, backwards in plan:
            print(f"    - {migration}")
    else:
        print("  ✅ All migrations applied")
except Exception as e:
    print(f"  ⚠️  Could not check migrations: {e}")

# 6. Settings Verification
print("\n[6] Verifying Critical Settings...")

settings_checks = {
    'DEBUG': os.environ.get('DEBUG', '0') == '1',
    'SECRET_KEY': bool(os.environ.get('DJANGO_SECRET_KEY') or os.environ.get('SECRET_KEY')),
    'DATABASES': bool(os.environ.get('DB_HOST')),
    'REDIS': bool(os.environ.get('REDIS_URL')),
    'SENTRY': bool(os.environ.get('SENTRY_DSN')),
}

for setting, is_set in settings_checks.items():
    status = "✅" if is_set else "⚠️ "
    print(f"  {status} {setting}: {is_set}")

# 7. Authentication
print("\n[7] Checking Authentication Setup...")
auth_checks = {
    'JWT': 'rest_framework_simplejwt' in str(apps_config),
    'Token Auth': 'rest_framework.authtoken' in str(apps_config),
}

for auth_type, enabled in auth_checks.items():
    status = "✅" if enabled else "❌"
    print(f"  {status} {auth_type}: {enabled}")

# 8. Cache Backend
print("\n[8] Checking Cache Configuration...")
from django.core.cache import cache
try:
    cache.set('test_key', 'test_value', 60)
    value = cache.get('test_key')
    if value == 'test_value':
        cache.delete('test_key')
        print("  ✅ Cache backend operational")
    else:
        print("  ❌ Cache backend not working correctly")
except Exception as e:
    print(f"  ⚠️  Cache backend check failed: {e}")

# 9. Critical Features
print("\n[9] Checking Critical Features...")

features = {
    'Rate Limiting': 'listings.rate_limiting' in [app.name for app in apps_config],
    'Caching': 'listings.caching' in [app.name for app in apps_config],
    'Auth Views': os.path.exists('listings/auth_views.py'),
}

for feature, available in features.items():
    status = "✅" if available else "⚠️ "
    print(f"  {status} {feature}: {available}")

# 10. Summary
print("\n" + "=" * 80)
print("VALIDATION SUMMARY")
print("=" * 80)

print("""
✅ = Ready for production
⚠️  = Configuration needed
❌ = Critical issue

NEXT STEPS:
1. Ensure all environment variables are set:
   - DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
   - REDIS_URL (if caching enabled)
   - SENTRY_DSN (optional, for error tracking)
   
2. Apply pending migrations:
   python manage.py migrate

3. Create superuser (if not exists):
   python manage.py createsuperuser

4. Start development server:
   python manage.py runserver
   
5. Access API documentation:
   - Swagger: http://localhost:8000/swagger/
   - ReDoc: http://localhost:8000/redoc/
""")

print("=" * 80)
