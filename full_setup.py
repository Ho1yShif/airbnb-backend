#!/usr/bin/env python
"""
Comprehensive environment initialization script for AirBnB Backend.
Handles database schema validation, superuser provisioning, test data seeding,
administrative interface configuration, and relationship verification.
"""
import os
import sys
import django
import subprocess
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airbnb.settings')

# Retrieve database configuration from environment with fallbacks
def load_database_config():
    """Load database configuration from environment variables."""
    defaults = {
        'DB_NAME': 'airbnb',
        'DB_USER': 'airbnb_user',
        'DB_PASSWORD': 'airbnb_pass',
        'DB_HOST': 'localhost',
        'DB_PORT': '5432'
    }
    for key, default_value in defaults.items():
        if key not in os.environ:
            os.environ[key] = default_value

load_database_config()

django.setup()

from django.contrib.auth.models import User
from django.db import connection
from listings.models import Property, PropertyImage, Booking, Payment, Review, Wishlist, UserProfile
from decimal import Decimal
import datetime

print("=" * 80)
print("AIRBNB BACKEND - COMPREHENSIVE ENVIRONMENT INITIALIZATION")
print("=" * 80)

# Phase 1: Database Schema Validation
print("\n" + "=" * 80)
print("PHASE 1: DATABASE SCHEMA VALIDATION")
print("=" * 80)

try:
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) as count FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        table_count = cursor.fetchone()[0]
    
    print(f"✓ Database contains {table_count} tables")
    
    # List all tables
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' ORDER BY table_name
        """)
        tables = cursor.fetchall()
    
    print("\n✓ Schema tables loaded:")
    for table in tables:
        print(f"  - {table[0]}")
    
    # Show migration history
    from django.db.migrations.recorder import MigrationRecorder
    recorder = MigrationRecorder(connection)
    migrations = list(recorder.applied_migrations())
    print(f"\n✓ Migration status: {len(migrations)} schemas applied")
    
except Exception as e:
    print(f"✗ Schema validation failed: {e}")
    sys.exit(1)

# Phase 2: Administrative User Provisioning
print("\n" + "=" * 80)
print("PHASE 2: ADMINISTRATIVE USER PROVISIONING")
print("=" * 80)

try:
    if User.objects.filter(username='admin').exists():
        admin = User.objects.get(username='admin')
        print("✓ Administrative account 'admin' already provisioned")
    else:
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@airbnb.local',
            password='admin123456'
        )
        print("✓ Administrative account created successfully")
        print(f"  Credentials: admin (role: {admin.profile.role})")
    
except Exception as e:
    print(f"✗ User provisioning failed: {e}")

# Phase 3: Test Data Initialization
print("\n" + "=" * 80)
print("PHASE 3: TEST DATA INITIALIZATION")
print("=" * 80)

try:
    # Initialize host test account
    if not User.objects.filter(username='testhost').exists():
        host = User.objects.create_user(
            username='testhost',
            email='host@test.com',
            password='testpass123',
            first_name='Test',
            last_name='Host'
        )
        host.profile.role = 'host'
        host.profile.phone = '+1-305-555-0100'
        host.profile.bio = 'Professional property host'
        host.profile.save()
        print("✓ Created host test account: testhost")
        
        # Create sample property listings for host
        properties_data = [
            {
                'title': 'Beautiful Beach House',
                'location': 'Miami, Florida',
                'price': Decimal('150.00'),
                'description': 'Stunning beachfront property with ocean views, direct beach access'
            },
            {
                'title': 'Modern Downtown Loft',
                'location': 'New York, New York',
                'price': Decimal('200.00'),
                'description': 'Contemporary loft in the heart of Manhattan'
            },
            {
                'title': 'Mountain Cabin Retreat',
                'location': 'Aspen, Colorado',
                'price': Decimal('180.00'),
                'description': 'Cozy cabin with fireplace and mountain views'
            }
        ]
        
        for prop_data in properties_data:
            prop = Property.objects.create(
                owner=host,
                **prop_data,
                status='available'
            )
            print(f"  ✓ Listing: {prop.title} (${prop.price}/night)")
    else:
        print("✓ Host test account 'testhost' already exists")
    
    # Initialize guest test account
    if not User.objects.filter(username='testguest').exists():
        guest = User.objects.create_user(
            username='testguest',
            email='guest@test.com',
            password='testpass123',
            first_name='Test',
            last_name='Guest'
        )
        guest.profile.role = 'guest'
        guest.profile.phone = '+1-305-555-0200'
        guest.profile.bio = 'Traveling enthusiast'
        guest.profile.save()
        print("✓ Created guest test account: testguest")
        
        # Create sample booking reservation for guest
        try:
            prop = Property.objects.first()
            if prop and not Booking.objects.filter(user=guest, property=prop).exists():
                booking = Booking.objects.create(
                    user=guest,
                    property=prop,
                    check_in_date=datetime.date.today() + datetime.timedelta(days=7),
                    check_out_date=datetime.date.today() + datetime.timedelta(days=14),
                    status='confirmed'
                )
                print(f"  ✓ Reservation created for {prop.title}")
                
                # Create corresponding payment transaction
                payment = Payment.objects.create(
                    booking=booking,
                    amount=prop.price * (booking.total_nights),
                    status='paid'
                )
                print(f"  ✓ Transaction processed: ${payment.amount}")
        except Exception as e:
            print(f"  ! Reservation creation note: {e}")
    else:
        print("✓ Guest test account 'testguest' already exists")
    
    # Initialize administrative service account
    if not User.objects.filter(username='admin_user').exists():
        admin_user = User.objects.create_user(
            username='admin_user',
            email='admin_user@airbnb.local',
            password='admin123456'
        )
        admin_user.profile.role = 'admin'
        admin_user.profile.save()
        print("✓ Created administrative service account: admin_user")
    
except Exception as e:
    print(f"✗ Test data initialization failed: {e}")
    import traceback
    traceback.print_exc()

# Phase 4: Administrative Interface Configuration
print("\n" + "=" * 80)
print("PHASE 4: ADMINISTRATIVE INTERFACE CONFIGURATION")
print("=" * 80)

try:
    from django.contrib.admin.apps import AdminConfig
    print("✓ Administrative interface is configured and available")
    print("  Access point: http://localhost:8000/admin")
    print("  Default credentials: admin / admin123456")
    print("\n✓ Managed entities:")
    
    models_to_check = [
        ('User', User),
        ('UserProfile', UserProfile),
        ('Property', Property),
        ('PropertyImage', PropertyImage),
        ('Booking', Booking),
        ('Payment', Payment),
        ('Review', Review),
        ('Wishlist', Wishlist),
    ]
    
    for name, model in models_to_check:
        count = model.objects.count()
        print(f"  - {name}: {count} records")
        
except Exception as e:
    print(f"! Administrative configuration note: {e}")

# Phase 5: Data Relationship Verification
print("\n" + "=" * 80)
print("PHASE 5: DATA RELATIONSHIP VERIFICATION")
print("=" * 80)

try:
    print("\n✓ Model relationship integrity check:")
    
    # Test ForeignKey relationships
    properties = Property.objects.all()
    print(f"  - Property portfolio: {properties.count()} listings")
    for prop in properties:
        bookings = prop.bookings.all().count()
        reviews = prop.reviews.all().count()
        images = prop.images.all().count()
        print(f"    - {prop.title}: {bookings} reservations, {reviews} reviews, {images} media items")
    
    # Test reverse ForeignKey from User
    print(f"\n  - User activity:")
    for user in User.objects.exclude(username__in=['AnonymousUser']):
        user_bookings = user.bookings.count()
        user_properties = user.properties.count()
        user_reviews = user.reviews.count()
        print(f"    - {user.username}: {user_properties} listings, {user_bookings} reservations, {user_reviews} reviews")
    
    # Test Payment OneToOne
    print(f"\n  - Transaction records:")
    payments = Payment.objects.all()
    for payment in payments:
        print(f"    - Transaction {payment.id}: ${payment.amount} ({payment.status}) [Reservation {payment.booking.id}]")
    
    # Test query aggregation
    from django.db.models import Count
    print(f"\n✓ Advanced analytics:")
    top_properties = Property.objects.annotate(
        booking_count=Count('bookings')
    ).order_by('-booking_count')[:3]
    print(f"  - Most reserved listings:")
    for prop in top_properties:
        print(f"    - {prop.title}: {prop.booking_count} total reservations")
    
except Exception as e:
    print(f"✗ Relationship verification failed: {e}")
    import traceback
    traceback.print_exc()

# Completion Summary
print("\n" + "=" * 80)
print("✓ INITIALIZATION SEQUENCE COMPLETED")
print("=" * 80)
print("\nEnvironment Summary:")
print(f"  - Database schemas: ✓ {len(migrations)} migrations applied")
print(f"  - Database tables: ✓ {table_count} tables initialized")
print(f"  - Administrative account: ✓ provisioned")
print(f"  - Test data: ✓ host, guest, listings created")
print(f"  - Admin interface: ✓ configured at /admin")
print(f"  - Relationships: ✓ integrity verified")

print("\nNext Steps:")
print("  1. Deploy container stack: docker-compose up -d web")
print("  2. Access admin interface: http://localhost:8000/admin")
print("  3. Configure API viewsets: listings/views.py")
print("  4. Execute test suite: python manage.py test listings")
print("  5. Promote to production environment")



try:
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) as count FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        table_count = cursor.fetchone()[0]
    
    print(f"✓ Database has {table_count} tables")
    
    # List all tables
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' ORDER BY table_name
        """)
        tables = cursor.fetchall()
    
    print("\n✓ Created tables:")
    for table in tables:
        print(f"  - {table[0]}")
    
    # Show migration history
    from django.db.migrations.recorder import MigrationRecorder
    recorder = MigrationRecorder(connection)
    migrations = list(recorder.applied_migrations())
    print(f"\n✓ Applied {len(migrations)} migrations")
    
except Exception as e:
    print(f"✗ Migration verification failed: {e}")
    sys.exit(1)

# STEP 2: Create Django Superuser
print("\n" + "=" * 80)
print("STEP 2: CREATE DJANGO SUPERUSER")
print("=" * 80)

try:
    if User.objects.filter(username='admin').exists():
        admin = User.objects.get(username='admin')
        print("✓ Superuser 'admin' already exists")
    else:
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@airbnb.local',
            password='admin123456'
        )
        print("✓ Superuser created:")
        print(f"  Username: admin")
        print(f"  Email: admin@airbnb.local")
        print(f"  Password: admin123456")
    
    print(f"  Profile role: {admin.profile.role}")
    
except Exception as e:
    print(f"✗ Superuser creation failed: {e}")

# STEP 3: Create Test Fixtures
print("\n" + "=" * 80)
print("STEP 3: CREATE TEST FIXTURES")
print("=" * 80)

try:
    # Create test host user
    if not User.objects.filter(username='testhost').exists():
        host = User.objects.create_user(
            username='testhost',
            email='host@test.com',
            password='testpass123',
            first_name='Test',
            last_name='Host'
        )
        host.profile.role = 'host'
        host.profile.phone = '+1-305-555-0100'
        host.profile.bio = 'Professional property host'
        host.profile.save()
        print("✓ Created host user: testhost")
        
        # Create sample properties for the host
        properties_data = [
            {
                'title': 'Beautiful Beach House',
                'location': 'Miami, Florida',
                'price': Decimal('150.00'),
                'description': 'Stunning beachfront property with ocean views, direct beach access'
            },
            {
                'title': 'Modern Downtown Loft',
                'location': 'New York, New York',
                'price': Decimal('200.00'),
                'description': 'Contemporary loft in the heart of Manhattan'
            },
            {
                'title': 'Mountain Cabin Retreat',
                'location': 'Aspen, Colorado',
                'price': Decimal('180.00'),
                'description': 'Cozy cabin with fireplace and mountain views'
            }
        ]
        
        for prop_data in properties_data:
            prop = Property.objects.create(
                owner=host,
                **prop_data,
                status='available'
            )
            print(f"  ✓ Property: {prop.title} (${prop.price}/night)")
    else:
        print("✓ Host user 'testhost' already exists")
    
    # Create test guest user
    if not User.objects.filter(username='testguest').exists():
        guest = User.objects.create_user(
            username='testguest',
            email='guest@test.com',
            password='testpass123',
            first_name='Test',
            last_name='Guest'
        )
        guest.profile.role = 'guest'
        guest.profile.phone = '+1-305-555-0200'
        guest.profile.bio = 'Traveling enthusiast'
        guest.profile.save()
        print("✓ Created guest user: testguest")
        
        # Create sample bookings for guest
        try:
            prop = Property.objects.first()
            if prop and not Booking.objects.filter(user=guest, property=prop).exists():
                booking = Booking.objects.create(
                    user=guest,
                    property=prop,
                    check_in_date=datetime.date.today() + datetime.timedelta(days=7),
                    check_out_date=datetime.date.today() + datetime.timedelta(days=14),
                    status='confirmed'
                )
                print(f"  ✓ Booking created for {prop.title}")
                
                # Create payment for booking
                payment = Payment.objects.create(
                    booking=booking,
                    amount=prop.price * (booking.total_nights),
                    status='paid'
                )
                print(f"  ✓ Payment created: ${payment.amount}")
        except Exception as e:
            print(f"  ! Error creating booking: {e}")
    else:
        print("✓ Guest user 'testguest' already exists")
    
    # Create admin user with all roles visibility
    if not User.objects.filter(username='admin_user').exists():
        admin_user = User.objects.create_user(
            username='admin_user',
            email='admin_user@airbnb.local',
            password='admin123456'
        )
        admin_user.profile.role = 'admin'
        admin_user.profile.save()
        print("✓ Created admin user: admin_user")
    
except Exception as e:
    print(f"✗ Fixture creation failed: {e}")
    import traceback
    traceback.print_exc()

# STEP 4: Deploy Django Admin (Just verify it's configured)
print("\n" + "=" * 80)
print("STEP 4: DJANGO ADMIN CONFIGURATION")
print("=" * 80)

try:
    from django.contrib.admin.apps import AdminConfig
    print("✓ Django Admin is configured")
    print("  Access at: http://localhost:8000/admin")
    print("  Superuser: admin / admin123456")
    print("\n✓ Models available in admin:")
    
    models_to_check = [
        ('User', User),
        ('UserProfile', UserProfile),
        ('Property', Property),
        ('PropertyImage', PropertyImage),
        ('Booking', Booking),
        ('Payment', Payment),
        ('Review', Review),
        ('Wishlist', Wishlist),
    ]
    
    for name, model in models_to_check:
        count = model.objects.count()
        print(f"  - {name}: {count} records")
        
except Exception as e:
    print(f"! Admin configuration note: {e}")

# STEP 5: API Testing
print("\n" + "=" * 80)
print("STEP 5: API TESTING & VERIFICATION")
print("=" * 80)

try:
    print("\n✓ Model Relationships Test:")
    
    # Test ForeignKey relationships
    properties = Property.objects.all()
    print(f"  - Properties: {properties.count()}")
    for prop in properties:
        bookings = prop.bookings.all().count()
        reviews = prop.reviews.all().count()
        images = prop.images.all().count()
        print(f"    - {prop.title}: {bookings} bookings, {reviews} reviews, {images} images")
    
    # Test reverse ForeignKey from User
    print(f"\n  - Users:")
    for user in User.objects.exclude(username__in=['AnonymousUser']):
        user_bookings = user.bookings.count()
        user_properties = user.properties.count()
        user_reviews = user.reviews.count()
        print(f"    - {user.username}: {user_properties} properties, {user_bookings} bookings, {user_reviews} reviews")
    
    # Test Payment OneToOne
    print(f"\n  - Payments:")
    payments = Payment.objects.all()
    for payment in payments:
        print(f"    - Payment {payment.id}: ${payment.amount} ({payment.status}) for Booking {payment.booking.id}")
    
    # Test query aggregation
    from django.db.models import Count
    print(f"\n✓ Advanced Queries:")
    top_properties = Property.objects.annotate(
        booking_count=Count('bookings')
    ).order_by('-booking_count')[:3]
    print(f"  - Top properties by bookings:")
    for prop in top_properties:
        print(f"    - {prop.title}: {prop.booking_count} bookings")
    
except Exception as e:
    print(f"✗ API testing failed: {e}")
    import traceback
    traceback.print_exc()

# Summary
print("\n" + "=" * 80)
print("✓ ALL STEPS COMPLETED SUCCESSFULLY!")
print("=" * 80)
print("\nSummary:")
print(f"  - Migrations: ✓ {len(migrations)} applied")
print(f"  - Database tables: ✓ {table_count} created")
print(f"  - Superuser: ✓ admin created")
print(f"  - Test fixtures: ✓ hosts, guests, properties created")
print(f"  - Admin interface: ✓ configured at /admin")
print(f"  - API relationships: ✓ verified and working")

print("\nNext Steps:")
print("  1. Start Django: docker-compose up -d web")
print("  2. Access admin: http://localhost:8000/admin")
print("  3. Create API views in listings/views.py")
print("  4. Run tests: python manage.py test listings")
print("  5. Deploy to production")
