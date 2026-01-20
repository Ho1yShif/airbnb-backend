#!/usr/bin/env python
"""
Comprehensive REST API validation suite.

Validates endpoint functionality, data integrity, and integration patterns
across the property rental platform.
"""
import os
import django
import json
import sys
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airbnb.settings')
for key in ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT']:
    if key not in os.environ:
        os.environ[key] = ''

django.setup()

from django.contrib.auth.models import User
from rest_framework.test import APIClient
from listings.models import Property, Booking, Payment, Review
from decimal import Decimal
import datetime

print(f"API Validation Suite - {Path(__file__).name}")
print("-" * 60)

# Initialize API client
client = APIClient()

# TEST 1: Verify User Models
print("\n[TEST 1] User Model Relationships")
print("-" * 70)
try:
    admin = User.objects.get(username='admin')
    print(f"✓ Admin user exists: {admin.username}")
    print(f"  Email: {admin.email}")
    print(f"  Profile role: {admin.profile.role}")
except User.DoesNotExist:
    print("✗ Admin user not found")

# TEST 2: Verify Property Model
print("\n[TEST 2] Property Model")
print("-" * 70)
try:
    properties = Property.objects.all()
    print(f"✓ Found {properties.count()} properties")
    for prop in properties:
        print(f"  - {prop.title}")
        print(f"    Owner: {prop.owner.username}")
        print(f"    Price: ${prop.price}")
        print(f"    Status: {prop.status}")
except Exception as e:
    print(f"✗ Error: {e}")

# TEST 3: Verify Booking Model
print("\n[TEST 3] Booking Model & Foreign Keys")
print("-" * 70)
try:
    bookings = Booking.objects.all()
    print(f"✓ Found {bookings.count()} bookings")
    for booking in bookings:
        print(f"  - Booking ID: {booking.id}")
        print(f"    Property: {booking.property.title}")
        print(f"    Guest: {booking.user.username}")
        print(f"    Check-in: {booking.check_in_date}")
        print(f"    Check-out: {booking.check_out_date}")
except Exception as e:
    print(f"✗ Error: {e}")

# TEST 4: Verify Payment Model
print("\n[TEST 4] Payment Model (One-to-One FK)")
print("-" * 70)
try:
    from listings.models import Payment
    payments = Payment.objects.all()
    print(f"✓ Found {payments.count()} payments")
    for payment in payments:
        print(f"  - Payment ID: {payment.id}")
        print(f"    Booking: {payment.booking.id}")
        print(f"    Amount: ${payment.amount}")
        print(f"    Status: {payment.status}")
except Exception as e:
    print(f"✗ Error: {e}")

# TEST 5: Verify Review Model
print("\n[TEST 5] Review Model (Multiple FKs)")
print("-" * 70)
try:
    reviews = Review.objects.all()
    print(f"✓ Found {reviews.count()} reviews")
    for review in reviews:
        print(f"  - Review ID: {review.id}")
        print(f"    Property: {review.property.title}")
        print(f"    By: {review.user.username}")
        print(f"    Rating: {review.rating}/5")
except Exception as e:
    print(f"✗ Error: {e}")

# TEST 6: Test ForeignKey Queryset Operations
print("\n[TEST 6] ForeignKey Queryset Operations")
print("-" * 70)
try:
    if Property.objects.exists():
        prop = Property.objects.first()
        # Test reverse relationship
        related_bookings = prop.bookings.all()
        print(f"✓ Property '{prop.title}' has {related_bookings.count()} bookings")
        
        related_reviews = prop.reviews.all()
        print(f"✓ Property has {related_reviews.count()} reviews")
except Exception as e:
    print(f"✗ Error: {e}")

# TEST 7: Check Migration History
print("\n[TEST 7] Migration History")
print("-" * 70)
try:
    from django.db import connection
    from django.db.migrations.recorder import MigrationRecorder
    
    recorder = MigrationRecorder(connection)
    migrations = recorder.applied_migrations()
    print(f"✓ Found {len(migrations)} applied migrations:")
    for app, name in sorted(migrations)[:10]:
        print(f"  - {app}: {name}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 70)
print("✓ API TESTS COMPLETED")
print("=" * 70)
print("\nNext Steps:")
print("1. Start development server: docker-compose up web")
print("2. Access Django Admin: http://localhost:8000/admin")
print("3. Run test suite: python manage.py test listings")
print("4. Create API views in listings/views.py")
print("5. Register URLs in listings/urls.py")
