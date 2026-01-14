from django.test import TestCase
from django.contrib.auth.models import User
from .models import Property, UserProfile, Booking

class UserProfileModelTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='testuser', password='testpass')
		self.profile = UserProfile.objects.create(user=self.user, name='Test User')

	def test_profile_str(self):
		self.assertEqual(str(self.profile), 'testuser - guest')

class PropertyModelTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='host', password='pass')
		self.property = Property.objects.create(owner=self.user, title='Test House', location='Test City', price=100)

	def test_property_str(self):
		self.assertEqual(str(self.property), 'Test House')

class BookingModelTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='guest', password='pass')
		self.host = User.objects.create_user(username='host', password='pass')
		self.property = Property.objects.create(owner=self.host, title='Test House', location='Test City', price=100)
		self.booking = Booking.objects.create(user=self.user, property=self.property, check_in_date='2026-01-15', check_out_date='2026-01-20')

	def test_booking_str(self):
		self.assertIn('Test House', str(self.booking))
		self.assertIn('guest', str(self.booking))
