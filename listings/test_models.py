from django.test import TestCase
from django.contrib.auth.models import User
from .models import Property, UserProfile, Booking, Address, CustomerPreferences

class UserProfileModelTest(TestCase):
    """
    Tests for UserProfile model validation and relationships.
    """
    def setUp(self):
        self.user_account = User.objects.create_user(
            username='marketplace_user',
            password='test_password_123'
        )
        self.profile = UserProfile.objects.get(user=self.user_account)

    def test_profile_string_representation(self):
        """
        Verify profile string output includes user and role.
        """
        profile_str = str(self.profile)
        self.assertIn(self.user_account.username, profile_str)
        self.assertIn('guest', profile_str)

class PropertyListingModelTest(TestCase):
    """
    Tests for Property model and business logic.
    """
    def setUp(self):
        self.owner_account = User.objects.create_user(
            username='property_manager',
            password='secure_test_123'
        )
        self.property_instance = Property.objects.create(
            property_owner=self.owner_account,
            listing_title='Elegant Downtown Apartment',
            property_location='Financial District',
            nightly_rate=180.00
        )

    def test_property_string_representation(self):
        """
        Verify property display format.
        """
        expected_output = f"{self.property_instance.listing_title} - {self.property_instance.property_location}"
        self.assertEqual(str(self.property_instance), expected_output)

class BookingManagementModelTest(TestCase):
    """
    Tests for Booking model constraints and validations.
    """
    def setUp(self):
        self.guest_account = User.objects.create_user(
            username='guest_user',
            password='guest_pass_123'
        )
        self.owner_account = User.objects.create_user(
            username='host_user',
            password='host_pass_123'
        )
        self.property_instance = Property.objects.create(
            property_owner=self.owner_account,
            listing_title='Cozy Studio',
            property_location='Residential Zone',
            nightly_rate=120.00
        )
        self.booking_instance = Booking.objects.create(
            guest=self.guest_account,
            reserved_property=self.property_instance,
            arrival_date='2026-03-15',
            departure_date='2026-03-20'
        )

    def test_booking_string_representation(self):
        """
        Verify booking details in string format.
        """
        booking_str = str(self.booking_instance)
        self.assertIn(self.guest_account.username, booking_str)
        self.assertIn(self.property_instance.listing_title, booking_str)
