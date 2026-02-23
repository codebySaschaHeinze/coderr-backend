from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from orders_app.models import Order


User = get_user_model()


class OrderTestsUnhappy(APITestCase):
    
    def test_orders_list_requires_auth_returns_401(self):
        url = reverse('order')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_orders_create_requires_auth_returns_401(self):
        url = reverse('order')
        res = self.client.post(url, {'offer_detail_id': 1}, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_orders_create_as_business_returns_403(self):
        businessUser = User.objects.create_user(
            username='User1',
            email='user@1.com',
            password='test123',
            type='business',
        )
        self.client.force_authenticate(user=businessUser)

        url = reverse('order')
        res = self.client.post(url, {'offer_detail_id': 1}, format='json')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(res.data)

    def test_orders_create_without_offer_detail_id_returns_400(self):
        customerUser = User.objects.create_user(
            username='User1',
            email='user@1.com',
            password='test123',
            type='customer',
        )
        self.client.force_authenticate(user=customerUser)

        url = reverse('order')
        res = self.client.post(url, {}, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(res.data)

    def test_order_create_invalid_offer_detail_id_returns_404(self):
        customerUser = User.objects.create_user(
            username='User1',
            email='user@1.com',
            password='test123',
            type='customer',
        )
        self.client.force_authenticate(user=customerUser)

        url = reverse('order')
        res = self.client.post(url, {'offer_detail_id': 99999999999999}, format='json')

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(res.data)
        