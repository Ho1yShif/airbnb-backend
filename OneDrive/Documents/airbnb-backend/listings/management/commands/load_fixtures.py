"""
Django management command to load sample data for development and testing.

Creates:
- Sample users with profiles (hosts and guests)
- Properties with descriptions and availability
- Bookings with various statuses
- Reviews and ratings
- Payment records

Usage:
    python manage.py load_fixtures
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal

from listings.models import (
    UserProfile, Property, Booking, Payment, Review, Wishlist, Address, CustomerPreferences
)


class Command(BaseCommand):
    help = 'Load sample data for development and testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before loading fixtures',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.clear_data()
            self.stdout.write(self.style.WARNING('Cleared existing data'))

        # Create hosts (property owners)
        hosts = self.create_hosts()
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(hosts)} host accounts'))

        # Create guests
        guests = self.create_guests()
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(guests)} guest accounts'))

        # Create properties
        properties = self.create_properties(hosts)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(properties)} properties'))

        # Create bookings
        bookings = self.create_bookings(guests, properties)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(bookings)} bookings'))

        # Create payments
        payments = self.create_payments(bookings)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(payments)} payment records'))

        # Create reviews
        reviews = self.create_reviews(guests, properties)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(reviews)} reviews'))

        # Create wishlists
        wishlists = self.create_wishlists(guests, properties)
        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(wishlists)} wishlist items'))

        self.stdout.write(self.style.SUCCESS('\n✓ All fixtures loaded successfully!'))
        self.print_sample_credentials(hosts, guests)

    def clear_data(self):
        """Clear all sample data"""
        models_to_clear = [
            Review, Payment, Booking, Wishlist, Property, UserProfile, User
        ]
        for model in models_to_clear:
            model.objects.all().delete()

    def create_hosts(self):
        """Create sample host accounts"""
        hosts_data = [
            {
                'username': 'alice_host',
                'email': 'alice@example.com',
                'first_name': 'Alice',
                'last_name': 'Johnson',
                'bio': 'Passionate property owner with 5+ years of hosting experience',
            },
            {
                'username': 'bob_host',
                'email': 'bob@example.com',
                'first_name': 'Bob',
                'last_name': 'Smith',
                'bio': 'Luxury apartment specialist in downtown areas',
            },
            {
                'username': 'carol_host',
                'email': 'carol@example.com',
                'first_name': 'Carol',
                'last_name': 'Davis',
                'bio': 'Cozy cottage owner near nature reserves',
            },
        ]

        hosts = []
        for data in hosts_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                }
            )
            if created:
                user.set_password('password123')
                user.save()

            profile = user.profile
            profile.user_role = 'host'
            profile.biography = data['bio']
            profile.phone_number = f'+1{60000 + len(hosts)}123456'
            profile.save()

            hosts.append(user)

        return hosts

    def create_guests(self):
        """Create sample guest accounts"""
        guests_data = [
            {
                'username': 'john_guest',
                'email': 'john@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
            },
            {
                'username': 'jane_guest',
                'email': 'jane@example.com',
                'first_name': 'Jane',
                'last_name': 'Wilson',
            },
            {
                'username': 'mike_guest',
                'email': 'mike@example.com',
                'first_name': 'Mike',
                'last_name': 'Brown',
            },
            {
                'username': 'sarah_guest',
                'email': 'sarah@example.com',
                'first_name': 'Sarah',
                'last_name': 'Taylor',
            },
        ]

        guests = []
        for data in guests_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                }
            )
            if created:
                user.set_password('password123')
                user.save()

            profile = user.profile
            profile.user_role = 'guest'
            profile.phone_number = f'+1{70000 + len(guests)}654321'
            profile.save()

            guests.append(user)

        return guests

    def create_properties(self, hosts):
        """Create sample properties"""
        properties_data = [
            {
                'owner': hosts[0],
                'title': 'Modern Downtown Apartment',
                'location': '123 Main St, New York, NY 10001',
                'rate': Decimal('150.00'),
                'description': 'Spacious 2-bedroom apartment in the heart of downtown with city views, fully equipped kitchen, and modern amenities.',
                'status': 'available',
            },
            {
                'owner': hosts[0],
                'title': 'Cozy Studio Loft',
                'location': '456 Park Ave, New York, NY 10002',
                'rate': Decimal('95.00'),
                'description': 'Charming studio with exposed brick, large windows, and artistic vibes. Perfect for solo travelers.',
                'status': 'available',
            },
            {
                'owner': hosts[1],
                'title': 'Luxury Penthouse Suite',
                'location': '789 Fifth Ave, New York, NY 10003',
                'rate': Decimal('350.00'),
                'description': 'Exclusive penthouse with rooftop terrace, panoramic views, concierge service, and premium furnishings.',
                'status': 'available',
            },
            {
                'owner': hosts[1],
                'title': 'Beachfront Beach House',
                'location': '321 Ocean Blvd, Miami, FL 33101',
                'rate': Decimal('250.00'),
                'description': 'Beautiful beach house with direct ocean access, private pool, and sunset views. Ideal for families.',
                'status': 'available',
            },
            {
                'owner': hosts[2],
                'title': 'Mountain Cabin Retreat',
                'location': '555 Forest Road, Aspen, CO 81611',
                'rate': Decimal('180.00'),
                'description': 'Peaceful mountain cabin surrounded by nature, fireplace, hot tub, and hiking trails nearby.',
                'status': 'available',
            },
            {
                'owner': hosts[2],
                'title': 'Historic Victorian Home',
                'location': '888 Heritage Lane, Boston, MA 02101',
                'rate': Decimal('200.00'),
                'description': 'Restored Victorian mansion with period features, elegant decor, and central location near attractions.',
                'status': 'available',
            },
        ]

        properties = []
        for data in properties_data:
            prop, created = Property.objects.get_or_create(
                property_owner=data['owner'],
                listing_title=data['title'],
                defaults={
                    'property_location': data['location'],
                    'nightly_rate': data['rate'],
                    'property_description': data['description'],
                    'listing_status': data['status'],
                }
            )
            properties.append(prop)

        return properties

    def create_bookings(self, guests, properties):
        """Create sample bookings with various statuses"""
        bookings = []
        today = date.today()

        booking_data = [
            {
                'guest': guests[0],
                'property': properties[0],
                'arrival': today + timedelta(days=5),
                'departure': today + timedelta(days=10),
                'status': 'approved',
            },
            {
                'guest': guests[1],
                'property': properties[1],
                'arrival': today + timedelta(days=2),
                'departure': today + timedelta(days=6),
                'status': 'awaiting_approval',
            },
            {
                'guest': guests[2],
                'property': properties[2],
                'arrival': today + timedelta(days=15),
                'departure': today + timedelta(days=22),
                'status': 'approved',
            },
            {
                'guest': guests[3],
                'property': properties[3],
                'arrival': today - timedelta(days=30),
                'departure': today - timedelta(days=25),
                'status': 'completed',
            },
            {
                'guest': guests[0],
                'property': properties[4],
                'arrival': today + timedelta(days=20),
                'departure': today + timedelta(days=25),
                'status': 'approved',
            },
        ]

        for data in booking_data:
            booking, created = Booking.objects.get_or_create(
                guest=data['guest'],
                reserved_property=data['property'],
                arrival_date=data['arrival'],
                defaults={
                    'departure_date': data['departure'],
                    'reservation_state': data['status'],
                }
            )
            bookings.append(booking)

        return bookings

    def create_payments(self, bookings):
        """Create payment records for bookings"""
        payments = []
        for booking in bookings[:3]:  # Create payments for first 3 bookings
            payment, created = Payment.objects.get_or_create(
                reservation=booking,
                defaults={
                    'transaction_amount': booking.computed_total_cost,
                    'transaction_state': 'successful',
                    'transaction_id': f'TXN-{booking.id}-001',
                    'payment_date': timezone.now(),
                }
            )
            payments.append(payment)

        return payments

    def create_reviews(self, guests, properties):
        """Create sample reviews"""
        reviews = []
        review_data = [
            {
                'reviewer': guests[0],
                'property': properties[0],
                'rating': 5,
                'comment': 'Amazing apartment! The host was very responsive and the location is perfect.',
            },
            {
                'reviewer': guests[1],
                'property': properties[1],
                'rating': 4,
                'comment': 'Nice cozy space, though a bit smaller than expected. Would stay again.',
            },
            {
                'reviewer': guests[3],
                'property': properties[3],
                'rating': 5,
                'comment': 'Wonderful beachfront property. Perfect for a family vacation!',
            },
        ]

        for data in review_data:
            review, created = Review.objects.get_or_create(
                reviewer=data['reviewer'],
                reviewed_property=data['property'],
                defaults={
                    'rating': data['rating'],
                    'comment': data['comment'],
                }
            )
            reviews.append(review)

        return reviews

    def create_wishlists(self, guests, properties):
        """Create wishlist items"""
        wishlists = []
        wishlist_data = [
            (guests[0], properties[2]),
            (guests[0], properties[4]),
            (guests[1], properties[3]),
            (guests[2], properties[0]),
            (guests[3], properties[5]),
        ]

        for guest, prop in wishlist_data:
            wishlist, created = Wishlist.objects.get_or_create(
                user=guest,
                property=prop,
            )
            wishlists.append(wishlist)

        return wishlists

    def print_sample_credentials(self, hosts, guests):
        """Print sample credentials for testing"""
        self.stdout.write('\n' + self.style.WARNING('=' * 60))
        self.stdout.write(self.style.WARNING('SAMPLE CREDENTIALS FOR TESTING'))
        self.stdout.write(self.style.WARNING('=' * 60))

        self.stdout.write(self.style.SUCCESS('\n🏠 HOSTS:'))
        for host in hosts:
            self.stdout.write(f'  Username: {host.username}')
            self.stdout.write(f'  Email: {host.email}')
            self.stdout.write(f'  Password: password123\n')

        self.stdout.write(self.style.SUCCESS('👤 GUESTS:'))
        for guest in guests:
            self.stdout.write(f'  Username: {guest.username}')
            self.stdout.write(f'  Email: {guest.email}')
            self.stdout.write(f'  Password: password123\n')

        self.stdout.write(self.style.WARNING('=' * 60))
        self.stdout.write('Use these credentials to test the API locally.\n')
