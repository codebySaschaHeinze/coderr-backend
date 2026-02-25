from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from profile_app.models import Profile


User = get_user_model()


class ProfileTests(APITestCase):
    """Tests for profile detail and profile list endpoints."""

    def test_profile_detail_success_and_expected_shape_returns_200(self):
        """Profile detail returns expected response shape with status 200."""
        user = User.objects.create_user(
            username='User1',
            email='user@1.com',
            password='test123',
            type='business',
        )
        Profile.objects.create(user=user)

        self.client.force_authenticate(user=user)

        url = reverse('profile-detail', kwargs={'pk': user.id})
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertCountEqual(
            res.data.keys(),
            [
                'user',
                'username',
                'first_name',
                'last_name',
                'file',
                'location',
                'tel',
                'description',
                'working_hours',
                'type',
                'email',
                'created_at',
            ],
        )

        for key in ('first_name', 'last_name', 'location', 'tel', 'description', 'working_hours'):
            self.assertIsNotNone(res.data[key])

    def test_profile_detail_empty_fields_are_empty_string_not_null_returns_200(self):
        """Profile detail returns empty strings instead of null for empty fields."""
        user = User.objects.create_user(
            username='EmptyUser',
            email='user@empty.com',
            password='test123',
            type='customer',
        )
        Profile.objects.create(user=user)

        self.client.force_authenticate(user=user)

        url = reverse('profile-detail', kwargs={'pk': user.id})
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        for key in ('first_name', 'last_name', 'location', 'tel', 'description', 'working_hours'):
            self.assertEqual(res.data[key], '')

    def test_profile_patch_owner_and_updates_fields_returns_200(self):
        """Profile owner can patch fields and nested email with status 200."""
        user = User.objects.create_user(
            username='User1',
            email='user@1.com',
            password='test123',
            type='customer',
        )
        Profile.objects.create(user=user)

        self.client.force_authenticate(user=user)

        url = reverse('profile-detail', kwargs={'pk': user.id})
        payload = {
            'first_name': 'Monty',
            'last_name': 'Python',
            'location': 'New York',
            'tel': '987654321',
            'description': 'Updated description',
            'working_hours': '10-18',
            'email': 'monty@python.com',
        }

        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['first_name'], 'Monty')
        self.assertEqual(res.data['email'], 'monty@python.com')
        self.assertEqual(res.data['working_hours'], '10-18')

        for key in ('first_name', 'last_name', 'location', 'tel', 'description', 'working_hours'):
            self.assertIsNotNone(res.data[key])

    def test_profiles_business_returns_only_business_returns_200(self):
        """Business profile list returns only business profiles."""
        business_user = User.objects.create_user(
            username='BusinessUser',
            email='user@business.com',
            password='test1234',
            type='business',
        )
        Profile.objects.create(user=business_user)

        customer_user = User.objects.create_user(
            username='CustomerUser',
            email='user@customer.com',
            password='test123',
            type='customer',
        )
        Profile.objects.create(user=customer_user)

        self.client.force_authenticate(user=customer_user)

        url = reverse('profiles-business')
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(res.data, list))
        self.assertGreaterEqual(len(res.data), 1)

        for item in res.data:
            self.assertEqual(item['type'], 'business')

    def test_profiles_customer_returns_only_customer_returns_200(self):
        """Customer profile list returns only customer profiles."""
        customer_user = User.objects.create_user(
            username='CustomerUser',
            email='user@customer.com',
            password='test123',
            type='customer',
        )
        Profile.objects.create(user=customer_user)

        business_user = User.objects.create_user(
            username='BusinessUser',
            email='user@business.com',
            password='test1234',
            type='business',
        )
        Profile.objects.create(user=business_user)

        self.client.force_authenticate(user=business_user)

        url = reverse('profiles-customer')
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(res.data, list))

        for item in res.data:
            self.assertEqual(item['type'], 'customer')