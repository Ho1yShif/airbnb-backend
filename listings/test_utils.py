"""
Test utilities, fixtures, and helper functions for API tests.
"""

import json
from datetime import date, timedelta
from decimal import Decimal
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from listings.models import Property, Booking, Review, Wishlist


class TestDataFactory:
    """Factory class for creating test data"""

    @staticmethod
    def create_host_user(username='testhost', email='host@example.com', password='testpass123'):
        """Create and return a host user"""
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name='Test',
            last_name='Host'
        )
        # Profile is auto-created by signal, but ensure it's set correctly
        user.profile.user_role = 'host'
        user.profile.save()
        return user

    @staticmethod
    def create_guest_user(username='testguest', email='guest@example.com', password='testpass123'):
        """Create and return a guest user"""
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name='Test',
            last_name='Guest'
        )
        # Profile is auto-created by signal, but ensure it's set correctly
        user.profile.user_role = 'guest'
        user.profile.save()
        return user

    @staticmethod
    def create_property(owner, listing_title='Test Property', 
                       nightly_rate=Decimal('100.00'), **kwargs):
        """Create and return a property"""
        defaults = {
            'property_location': 'Test Location',
            'nightly_rate': nightly_rate,
            'property_description': 'Test description',
            'listing_status': 'available'
        }
        defaults.update(kwargs)
        
        return Property.objects.create(
            property_owner=owner,
            listing_title=listing_title,
            **defaults
        )

    @staticmethod
    def create_booking(guest, property, arrival_days=5, duration=5, **kwargs):
        """Create and return a booking"""
        arrival_date = date.today() + timedelta(days=arrival_days)
        departure_date = arrival_date + timedelta(days=duration)
        
        defaults = {
            'reservation_state': 'awaiting_approval',
            'guest_feedback': '',
        }
        defaults.update(kwargs)
        
        return Booking.objects.create(
            guest=guest,
            reserved_property=property,
            arrival_date=arrival_date,
            departure_date=departure_date,
            **defaults
        )

    @staticmethod
    def create_review(reviewer, property, rating=5, comment='Great!', **kwargs):
        """Create and return a review"""
        defaults = {'rating': rating, 'comment': comment}
        defaults.update(kwargs)
        
        return Review.objects.create(
            reviewer=reviewer,
            reviewed_property=property,
            **defaults
        )

    @staticmethod
    def create_wishlist(user, property):
        """Create and return a wishlist entry"""
        return Wishlist.objects.create(user=user, property=property)

    @staticmethod
    def get_auth_token(user):
        """Get or create auth token for user"""
        token, created = Token.objects.get_or_create(user=user)
        return token


class APITestMixin:
    """Mixin for common API test functionality"""

    def authenticate(self, user):
        """Authenticate client with user's token"""
        token = TestDataFactory.get_auth_token(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def assert_valid_json(self, response):
        """Assert response contains valid JSON"""
        try:
            json.loads(response.content)
        except json.JSONDecodeError:
            self.fail('Response is not valid JSON')

    def assert_property_fields(self, response_data, expected_fields):
        """Assert response contains expected property fields"""
        for field in expected_fields:
            self.assertIn(field, response_data)

    def assert_error_response(self, response, status_code, error_field=None):
        """Assert response is an error with expected status and optionally field"""
        self.assertEqual(response.status_code, status_code)
        if error_field:
            self.assertIn(error_field, response.data)


class MockEmailBackend:
    """Mock email backend for testing"""

    def __init__(self):
        self.sent_emails = []

    def send_mail(self, subject, message, from_email, recipient_list, **kwargs):
        """Mock send_mail implementation"""
        self.sent_emails.append({
            'subject': subject,
            'message': message,
            'from_email': from_email,
            'recipient_list': recipient_list,
        })
        return len(recipient_list)

    def clear(self):
        """Clear sent emails"""
        self.sent_emails = []


class CeleryTestMixin:
    """Mixin for testing Celery tasks"""

    def setup_celery_test(self):
        """Setup Celery for synchronous testing"""
        # In test settings, CELERY_TASK_ALWAYS_EAGER should be True
        # This makes all tasks execute synchronously
        pass

    def assert_task_executed(self, task_name, *args, **kwargs):
        """Assert a task was executed (requires task tracking)"""
        # Can be extended with task backend inspection
        pass


# Test Data Constants
TEST_EMAIL_VALID = 'test@example.com'
TEST_EMAIL_INVALID = 'invalid-email'
TEST_USER_PASSWORD = 'testpass123'
TEST_BOOKING_DURATION = 5
TEST_PROPERTY_RATE = Decimal('100.00')

# Expected fields in API responses
PROPERTY_RESPONSE_FIELDS = [
    'id', 'listing_title', 'property_location', 'nightly_rate',
    'property_description', 'listing_status', 'property_owner'
]

BOOKING_RESPONSE_FIELDS = [
    'id', 'guest', 'reserved_property', 'arrival_date', 
    'departure_date', 'reservation_state'
]

REVIEW_RESPONSE_FIELDS = [
    'id', 'reviewer', 'reviewed_property', 'rating', 'comment'
]

WISHLIST_RESPONSE_FIELDS = [
    'id', 'user', 'property', 'added_date'
]
