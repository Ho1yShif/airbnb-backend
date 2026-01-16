from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Property

class TestPropertyAPI(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='host', password='pass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_property(self):
        url = reverse('property-list')
        data = {
            'owner': self.user.id,
            'title': 'API House',
            'location': 'API City',
            'price': 200
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Property.objects.count(), 1)
        self.assertEqual(Property.objects.get().title, 'API House')

    def test_list_properties(self):
        Property.objects.create(owner=self.user, title='House1', location='Loc1', price=100)
        url = reverse('property-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
