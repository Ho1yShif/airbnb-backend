from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Property

class PropertyManagementAPITest(APITestCase):
    """
    Test suite for property listing management endpoints.
    """
    def setUp(self):
        self.account = User.objects.create_user(
            username='property_owner',
            password='secure_pass_123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.account)

    def test_property_creation_endpoint(self):
        """
        Verify property creation with valid listing parameters.
        """
        endpoint = reverse('listing-list')
        payload = {
            'property_owner': self.account.id,
            'listing_title': 'Premium Vacation Residence',
            'property_location': 'Metropolitan Area',
            'nightly_rate': 250.00
        }
        response = self.client.post(endpoint, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Property.objects.filter(property_owner=self.account).count(), 1)

    def test_property_retrieval_endpoint(self):
        """
        Verify property listing retrieval.
        """
        Property.objects.create(
            property_owner=self.account,
            listing_title='Test Listing',
            property_location='Test Location',
            nightly_rate=150.00
        )
        endpoint = reverse('listing-list')
        response = self.client.get(endpoint, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
