from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
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

class PropertyAPITest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='apiuser', password='apipass')
		self.client = APIClient()
		self.client.force_authenticate(user=self.user)

	def test_create_property(self):
		data = {
			'title': 'API House',
			'location': 'API City',
			'price': 200,
			'description': 'A nice place',
			'status': 'available'
		}
		response = self.client.post('/api/properties/', data)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.data['title'], 'API House')
