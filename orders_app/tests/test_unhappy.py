from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from orders_app.models import Order


User = get_user_model()


class OrderTestsUnhappy(APITestCase):
    """Unhappy-path tests for order endpoints."""

    def test_orders_list_requires_auth_returns_401(self):
        """Order list without authentication returns status 401."""
        url = reverse('order')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_orders_create_requires_auth_returns_401(self):
        """Order creation without authentication returns status 401."""
        url = reverse('order')
        res = self.client.post(url, {'offer_detail_id': 1}, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_orders_create_as_business_returns_403(self):
        """Order creation as business user returns status 403."""
        business_user = User.objects.create_user(
            username='User1',
            email='user@1.com',
            password='test123',
            type='business',
        )
        self.client.force_authenticate(user=business_user)

        url = reverse('order')
        res = self.client.post(url, {'offer_detail_id': 1}, format='json')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(res.data)

    def test_orders_create_without_offer_detail_id_returns_400(self):
        """Order creation without offer_detail_id returns status 400."""
        customer_user = User.objects.create_user(
            username='User1',
            email='user@1.com',
            password='test123',
            type='customer',
        )
        self.client.force_authenticate(user=customer_user)

        url = reverse('order')
        res = self.client.post(url, {}, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(res.data)

    def test_order_create_invalid_offer_detail_id_returns_404(self):
        """Order creation with invalid offer_detail_id returns status 404."""
        customer_user = User.objects.create_user(
            username='User1',
            email='user@1.com',
            password='test123',
            type='customer',
        )
        self.client.force_authenticate(user=customer_user)

        url = reverse('order')
        res = self.client.post(url, {'offer_detail_id': 99999999999999}, format='json')

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(res.data)

    def test_order_patch_as_customer_returns_403(self):
        """Order status update as customer user returns status 403."""
        business_user = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )
        customer_user = User.objects.create_user(
            username='CustomerUser',
            email='user@customer.com',
            password='test123',
            type='customer',
        )

        order = Order.objects.create(
            customer_user=customer_user,
            business_user=business_user,
            title='AAAAA',
            revisions=2,
            delivery_time_in_days=4,
            price='210.00',
            features=[],
            offer_type='premium',
            status='in_progress',
        )
        self.client.force_authenticate(user=customer_user)

        url = reverse('order-detail', kwargs={'id': order.id})
        res = self.client.patch(url, {'status': 'completed'}, format='json')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(res.data)

    def test_order_patch_invalid_status_returns_400(self):
        """Order status update with invalid status returns status 400."""
        business_user = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )
        customer_user = User.objects.create_user(
            username='CustomerUser',
            email='user@customer.com',
            password='test123',
            type='customer',
        )
        order = Order.objects.create(
            customer_user=customer_user,
            business_user=business_user,
            title='AAAAA',
            revisions=2,
            delivery_time_in_days=4,
            price='210.00',
            features=[],
            offer_type='premium',
            status='in_progress',
        )
        self.client.force_authenticate(user=business_user)

        url = reverse('order-detail', kwargs={'id': order.id})
        res = self.client.patch(url, {'status': 'invalid_status'}, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(res.data)

    def test_order_delete_requires_auth_returns_401(self):
        """Order delete without authentication returns status 401."""
        business_user = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )
        customer_user = User.objects.create_user(
            username='CustomerUser',
            email='user@customer.com',
            password='test123',
            type='customer',
        )
        order = Order.objects.create(
            customer_user=customer_user,
            business_user=business_user,
            title='AAAAA',
            revisions=2,
            delivery_time_in_days=4,
            price='210.00',
            features=[],
            offer_type='premium',
            status='in_progress',
        )

        url = reverse('order-detail', kwargs={'id': order.id})
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_delete_as_non_staff_returns_403(self):
        """Order delete by non-staff user returns status 403."""
        business_user = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )
        customer_user = User.objects.create_user(
            username='CustomerUser',
            email='user@customer.com',
            password='test123',
            type='customer',
        )
        order = Order.objects.create(
            customer_user=customer_user,
            business_user=business_user,
            title='AAAAA',
            revisions=2,
            delivery_time_in_days=4,
            price='210.00',
            features=[],
            offer_type='premium',
            status='in_progress',
        )

        self.client.force_authenticate(user=customer_user)

        url = reverse('order-detail', kwargs={'id': order.id})
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(res.data)

    def test_order_count_requires_auth_returns_401(self):
        """Order-count endpoint without authentication returns status 401."""
        url = reverse('order-count', kwargs={'business_user_id': 1})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_count_invalid_business_user_returns_404(self):
        """Order-count endpoint with invalid business user returns status 404."""
        auth_user = User.objects.create_user(
            username='CustomerUser',
            email='user@customer.com',
            password='test123',
            type='customer',
        )

        self.client.force_authenticate(user=auth_user)

        url = reverse('order-count', kwargs={'business_user_id': 9999999999999999})
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(res.data)

    def test_completed_order_count_invalid_business_user_returns_404(self):
        """Completed-order-count with invalid business user returns status 404."""
        auth_user = User.objects.create_user(
            username='CustomerUser',
            email='user@customer.com',
            password='test123',
            type='customer',
        )

        self.client.force_authenticate(user=auth_user)

        url = reverse(
            'completed-order-count',
            kwargs={'business_user_id': 9999999999999999},
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(res.data)

    def test_order_patch_invalid_id_as_business_returns_404(self):
        business_user = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
         password='test123',
            type='business',
        )
        self.client.force_authenticate(user=business_user)

        url = reverse('order-detail', kwargs={'id': 999999999999})
        res = self.client.patch(url, {'status': 'completed'}, format='json')

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)