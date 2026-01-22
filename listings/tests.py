"""
Comprehensive test suite for API endpoints, Celery tasks, and email functionality.

Tests:
- Email notification endpoint
- CRUD operations for all resources
- Celery task execution
- Email sending with mocking
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core import mail
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from unittest.mock import patch, MagicMock
from datetime import date, timedelta
from decimal import Decimal

from listings.models import (
    UserProfile, Property, Booking, Review, Wishlist
)
from listings.serializers import EmailNotificationSerializer
from listings.tasks import send_notification_email


class EmailNotificationSerializerTest(TestCase):
    """Tests for EmailNotificationSerializer validation"""

    def test_valid_email_notification(self):
        """Test serializer with valid data"""
        data = {
            'subject': 'Test Subject',
            'message': 'Test message content',
            'recipient': 'test@example.com'
        }
        serializer = EmailNotificationSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_email_format(self):
        """Test serializer rejects invalid email"""
        data = {
            'subject': 'Test Subject',
            'message': 'Test message',
            'recipient': 'invalid-email'
        }
        serializer = EmailNotificationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('recipient', serializer.errors)

    def test_missing_required_fields(self):
        """Test serializer requires all fields"""
        data = {
            'subject': 'Test Subject',
            # Missing message and recipient
        }
        serializer = EmailNotificationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('message', serializer.errors)
        self.assertIn('recipient', serializer.errors)

    def test_empty_subject(self):
        """Test serializer rejects empty subject"""
        data = {
            'subject': '',
            'message': 'Test message',
            'recipient': 'test@example.com'
        }
        serializer = EmailNotificationSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_long_subject(self):
        """Test serializer enforces max length"""
        data = {
            'subject': 'x' * 300,  # Exceeds 255 max
            'message': 'Test message',
            'recipient': 'test@example.com'
        }
        serializer = EmailNotificationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('subject', serializer.errors)


class EmailNotificationEndpointTest(APITestCase):
    """Tests for email notification API endpoint"""

    def setUp(self):
        """Set up test client and data"""
        self.client = APIClient()
        # Ensure email URL exists in routing
        try:
            self.email_url = reverse('send-email')
        except Exception:
            self.email_url = '/api/send-email/'

    def test_send_email_success(self):
        """Test successful email notification"""
        data = {
            'subject': 'Welcome',
            'message': 'Welcome to AirBnB!',
            'recipient': 'user@example.com'
        }
        
        with patch('listings.tasks.send_notification_email.delay') as mock_task:
            mock_task.return_value.id = 'task-123'
            
            response = self.client.post(self.email_url, data, format='json')
            
            self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
            self.assertEqual(response.data['status'], 'success')
            self.assertEqual(response.data['task_id'], 'task-123')
            mock_task.assert_called_once()

    def test_send_email_invalid_data(self):
        """Test endpoint rejects invalid data"""
        data = {
            'subject': 'Test',
            'message': 'Test',
            # Missing recipient
        }
        
        response = self.client.post(self.email_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertIn('recipient', response.data['errors'])

    def test_send_email_invalid_email(self):
        """Test endpoint rejects invalid email address"""
        data = {
            'subject': 'Test',
            'message': 'Test message',
            'recipient': 'not-an-email'
        }
        
        response = self.client.post(self.email_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_send_email_task_error(self):
        """Test endpoint handles Celery task errors"""
        data = {
            'subject': 'Test',
            'message': 'Test message',
            'recipient': 'test@example.com'
        }
        
        with patch('listings.tasks.send_notification_email.delay') as mock_task:
            mock_task.side_effect = Exception('Connection error')
            
            response = self.client.post(self.email_url, data, format='json')
            
            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
            self.assertEqual(response.data['status'], 'error')

    def test_send_email_get_not_allowed(self):
        """Test GET method not allowed"""
        response = self.client.get(self.email_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class CeleryEmailTaskTest(TestCase):
    """Tests for Celery email task execution"""

    def test_send_notification_email_task(self):
        """Test email task sends email successfully"""
        subject = 'Test Subject'
        message = 'Test message content'
        recipient = 'test@example.com'
        
        # Clear mail outbox
        mail.outbox = []
        
        # Execute task synchronously (CELERY_TASK_ALWAYS_EAGER=True in tests)
        result = send_notification_email(subject, message, recipient)
        
        self.assertIn('success', result.lower())
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [recipient])
        self.assertEqual(mail.outbox[0].subject, subject)
        self.assertEqual(mail.outbox[0].body, message)

    def test_send_notification_email_multiple(self):
        """Test sending multiple emails"""
        emails = [
            ('Subject 1', 'Message 1', 'user1@example.com'),
            ('Subject 2', 'Message 2', 'user2@example.com'),
            ('Subject 3', 'Message 3', 'user3@example.com'),
        ]
        
        mail.outbox = []
        
        for subject, message, recipient in emails:
            send_notification_email(subject, message, recipient)
        
        self.assertEqual(len(mail.outbox), 3)
        
        for i, (subject, message, recipient) in enumerate(emails):
            self.assertEqual(mail.outbox[i].to, [recipient])
            self.assertEqual(mail.outbox[i].subject, subject)

    @patch('django.core.mail.send_mail')
    def test_send_notification_email_failure(self, mock_send):
        """Test email task handles send failure"""
        mock_send.side_effect = Exception('SMTP connection failed')
        
        with self.assertRaises(Exception):
            send_notification_email(
                'Subject',
                'Message',
                'test@example.com'
            )
        
        mock_send.assert_called_once()


class PropertyCRUDTest(APITestCase):
    """Tests for Property CRUD operations"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.host_user = User.objects.create_user(
            username='host',
            email='host@example.com',
            password='testpass123'
        )
        self.host_user.profile.user_role = 'host'
        self.host_user.profile.save()
        
        self.token = Token.objects.create(user=self.host_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        self.property_url = reverse('property-list')

    def test_create_property(self):
        """Test creating a new property"""
        data = {
            'listing_title': 'Modern Apartment',
            'property_location': '123 Main St',
            'nightly_rate': '150.00',
            'property_description': 'Beautiful modern apartment',
            'listing_status': 'available'
        }
        
        response = self.client.post(self.property_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['listing_title'], data['listing_title'])
        self.assertTrue(Property.objects.filter(listing_title=data['listing_title']).exists())

    def test_list_properties(self):
        """Test listing all properties"""
        # Create test properties
        Property.objects.create(
            property_owner=self.host_user,
            listing_title='Property 1',
            property_location='Location 1',
            nightly_rate=Decimal('100.00')
        )
        Property.objects.create(
            property_owner=self.host_user,
            listing_title='Property 2',
            property_location='Location 2',
            nightly_rate=Decimal('150.00')
        )
        
        response = self.client.get(self.property_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_retrieve_property(self):
        """Test retrieving a single property"""
        prop = Property.objects.create(
            property_owner=self.host_user,
            listing_title='Test Property',
            property_location='Test Location',
            nightly_rate=Decimal('100.00'),
            property_description='Test description'
        )
        
        url = reverse('property-detail', kwargs={'pk': prop.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['listing_title'], 'Test Property')

    def test_update_property(self):
        """Test updating a property"""
        prop = Property.objects.create(
            property_owner=self.host_user,
            listing_title='Original Title',
            property_location='Original Location',
            nightly_rate=Decimal('100.00')
        )
        
        url = reverse('property-detail', kwargs={'pk': prop.id})
        data = {
            'listing_title': 'Updated Title',
            'property_location': 'Original Location',
            'nightly_rate': '100.00',
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['listing_title'], 'Updated Title')

    def test_delete_property(self):
        """Test deleting a property"""
        prop = Property.objects.create(
            property_owner=self.host_user,
            listing_title='Property to Delete',
            property_location='Location',
            nightly_rate=Decimal('100.00')
        )
        
        url = reverse('property-detail', kwargs={'pk': prop.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Property.objects.filter(id=prop.id).exists())

    def test_create_property_invalid_rate(self):
        """Test property creation with invalid rate"""
        data = {
            'listing_title': 'Property',
            'property_location': 'Location',
            'nightly_rate': '-50.00',  # Negative rate
            'listing_status': 'available'
        }
        
        response = self.client.post(self.property_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BookingCRUDTest(APITestCase):
    """Tests for Booking CRUD operations"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create host and property
        self.host_user = User.objects.create_user(
            username='host',
            email='host@example.com',
            password='testpass123'
        )
        self.host_user.profile.user_role = 'host'
        self.host_user.profile.save()
        
        # Create guest
        self.guest_user = User.objects.create_user(
            username='guest',
            email='guest@example.com',
            password='testpass123'
        )
        self.guest_user.profile.user_role = 'guest'
        self.guest_user.profile.save()
        
        # Create property
        self.property = Property.objects.create(
            property_owner=self.host_user,
            listing_title='Test Property',
            property_location='Test Location',
            nightly_rate=Decimal('100.00')
        )
        
        self.token = Token.objects.create(user=self.guest_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        self.booking_url = reverse('booking-list')

    def test_create_booking(self):
        """Test creating a booking"""
        data = {
            'reserved_property': self.property.id,
            'arrival_date': (date.today() + timedelta(days=5)).isoformat(),
            'departure_date': (date.today() + timedelta(days=10)).isoformat(),
        }
        
        response = self.client.post(self.booking_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Booking.objects.filter(
            guest=self.guest_user,
            reserved_property=self.property
        ).exists())

    def test_create_booking_invalid_dates(self):
        """Test booking with departure before arrival"""
        data = {
            'reserved_property': self.property.id,
            'arrival_date': (date.today() + timedelta(days=10)).isoformat(),
            'departure_date': (date.today() + timedelta(days=5)).isoformat(),
        }
        
        response = self.client.post(self.booking_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_booking_past_date(self):
        """Test booking with past dates"""
        data = {
            'reserved_property': self.property.id,
            'arrival_date': (date.today() - timedelta(days=5)).isoformat(),
            'departure_date': (date.today() - timedelta(days=1)).isoformat(),
        }
        
        response = self.client.post(self.booking_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_bookings(self):
        """Test listing bookings for authenticated user"""
        Booking.objects.create(
            guest=self.guest_user,
            reserved_property=self.property,
            arrival_date=date.today() + timedelta(days=5),
            departure_date=date.today() + timedelta(days=10)
        )
        
        response = self.client.get(self.booking_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_update_booking_status(self):
        """Test updating booking status"""
        booking = Booking.objects.create(
            guest=self.guest_user,
            reserved_property=self.property,
            arrival_date=date.today() + timedelta(days=5),
            departure_date=date.today() + timedelta(days=10),
            reservation_state='awaiting_approval'
        )
        
        url = reverse('booking-detail', kwargs={'pk': booking.id})
        data = {
            'reservation_state': 'approved',
        }
        
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        booking.refresh_from_db()
        self.assertEqual(booking.reservation_state, 'approved')


class ReviewCRUDTest(APITestCase):
    """Tests for Review CRUD operations"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create users
        self.guest_user = User.objects.create_user(
            username='guest',
            email='guest@example.com',
            password='testpass123'
        )
        self.host_user = User.objects.create_user(
            username='host',
            email='host@example.com',
            password='testpass123'
        )
        
        # Create property
        self.property = Property.objects.create(
            property_owner=self.host_user,
            listing_title='Test Property',
            property_location='Test Location',
            nightly_rate=Decimal('100.00')
        )
        
        self.token = Token.objects.create(user=self.guest_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        self.review_url = reverse('review-list')

    def test_create_review(self):
        """Test creating a review"""
        data = {
            'reviewed_property': self.property.id,
            'rating': 5,
            'comment': 'Excellent property!'
        }
        
        response = self.client.post(self.review_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Review.objects.filter(
            reviewer=self.guest_user,
            reviewed_property=self.property
        ).exists())

    def test_create_review_invalid_rating(self):
        """Test review with invalid rating"""
        data = {
            'reviewed_property': self.property.id,
            'rating': 10,  # Max is 5
            'comment': 'Great'
        }
        
        response = self.client.post(self.review_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_reviews(self):
        """Test listing reviews"""
        Review.objects.create(
            reviewer=self.guest_user,
            reviewed_property=self.property,
            rating=5,
            comment='Great stay'
        )
        
        response = self.client.get(self.review_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WishlistCRUDTest(APITestCase):
    """Tests for Wishlist CRUD operations"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create users
        self.guest_user = User.objects.create_user(
            username='guest',
            email='guest@example.com',
            password='testpass123'
        )
        self.host_user = User.objects.create_user(
            username='host',
            email='host@example.com',
            password='testpass123'
        )
        
        # Create properties
        self.property1 = Property.objects.create(
            property_owner=self.host_user,
            listing_title='Property 1',
            property_location='Location 1',
            nightly_rate=Decimal('100.00')
        )
        self.property2 = Property.objects.create(
            property_owner=self.host_user,
            listing_title='Property 2',
            property_location='Location 2',
            nightly_rate=Decimal('150.00')
        )
        
        self.token = Token.objects.create(user=self.guest_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        self.wishlist_url = reverse('wishlist-list')

    def test_add_to_wishlist(self):
        """Test adding property to wishlist"""
        data = {
            'property': self.property1.id,
        }
        
        response = self.client.post(self.wishlist_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Wishlist.objects.filter(
            user=self.guest_user,
            property=self.property1
        ).exists())

    def test_list_wishlist(self):
        """Test listing user's wishlist"""
        Wishlist.objects.create(user=self.guest_user, property=self.property1)
        Wishlist.objects.create(user=self.guest_user, property=self.property2)
        
        response = self.client.get(self.wishlist_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_remove_from_wishlist(self):
        """Test removing property from wishlist"""
        wishlist = Wishlist.objects.create(user=self.guest_user, property=self.property1)
        
        url = reverse('wishlist-detail', kwargs={'pk': wishlist.id})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Wishlist.objects.filter(id=wishlist.id).exists())


class AuthenticationTest(APITestCase):
    """Tests for authentication and authorization"""

    def setUp(self):
        """Set up test users"""
        self.guest_user = User.objects.create_user(
            username='guest',
            email='guest@example.com',
            password='testpass123'
        )
        self.host_user = User.objects.create_user(
            username='host',
            email='host@example.com',
            password='testpass123'
        )
        self.host_user.profile.user_role = 'host'
        self.host_user.profile.save()

    def test_unauthenticated_access_denied(self):
        """Test that unauthenticated users cannot access protected endpoints"""
        url = reverse('profile-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_authentication(self):
        """Test token-based authentication"""
        token = Token.objects.create(user=self.guest_user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        url = reverse('profile-list')
        response = client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_token(self):
        """Test that invalid token is rejected"""
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token invalid-token-123')
        
        url = reverse('profile-list')
        response = client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
