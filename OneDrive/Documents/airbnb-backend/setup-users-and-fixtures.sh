#!/bin/bash

echo "Initializing administrative user accounts..."
docker-compose exec -T web python manage.py shell << EOF
from django.contrib.auth.models import User

# Provision administrative superuser account
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@airbnb.local',
        password='admin123456'
    )
    print("✓ Administrative account created")
    print("  Credentials: admin / admin123456")
else:
    print("✓ Administrative account already exists")
    
# Display active user accounts
print("\nActive user accounts:")
for user in User.objects.all():
    print(f"  - {user.username} ({user.email})")
EOF

echo -e "\nProvisioning test data fixtures..."
docker-compose exec -T web python manage.py shell << EOF
from django.contrib.auth.models import User
from listings.models import Property, PropertyImage, Booking, Review, UserProfile
from decimal import Decimal
import datetime

# Create host test account
if not User.objects.filter(username='testhost').exists():
    host = User.objects.create_user(
        username='testhost',
        email='host@test.com',
        password='testpass123'
    )
    host.profile.role = 'host'
    host.profile.save()
    
    # Create sample property listing
    prop = Property.objects.create(
        owner=host,
        title='Beautiful Beach House',
        location='Miami, Florida',
        price=Decimal('150.00'),
        description='Stunning beachfront property with ocean views',
        status='available'
    )
    print(f"✓ Host account and property created: {prop.title}")
    
# Create guest test account
if not User.objects.filter(username='testguest').exists():
    guest = User.objects.create_user(
        username='testguest',
        email='guest@test.com',
        password='testpass123'
    )
    guest.profile.role = 'guest'
    guest.profile.save()
    print("✓ Guest account created: testguest")

print("\n✓ Test data provisioning completed")
EOF

echo -e "\nValidating data integrity..."
docker-compose exec -T web python manage.py shell << EOF
from django.contrib.auth.models import User
from listings.models import Property

print("Data inventory:")
print(f"  User accounts: {User.objects.count()}")
print(f"  Property listings: {Property.objects.count()}")

print("\nAccount summary:")
for user in User.objects.all():
    print(f"  - {user.username} ({user.profile.role})")
    
print("\nProperty summary:")
for prop in Property.objects.all():
    print(f"  - {prop.title} (${prop.price}/night)")
EOF

echo -e "\n✓ Provisioning completed - Access admin at http://localhost:8000/admin"
