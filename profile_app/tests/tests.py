from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from profile_app.models import Profile


User = get_user_model()


class ProfileTests(APITestCase):

    def test_profile_detail_success_and_expected_shape_returns_200(self):
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
                'user', 'username', 'first_name', 'last_name', 'file',
                'location', 'tel', 'description', 'working_hours',
                'type', 'email', 'created_at',
            ],
        )

        for key in ('first_name', 'last_name', 'location', 'tel', 'description', 'working_hours'):
            self.assertIsNotNone(res.data[key])

    def test_profile_detail_requires_auth_returns_401(self):
        user = User.objects.create_user(
            username='User1',
            email='user@1.com',
            password='test123',
            type='customer',
        )
        Profile.objects.create(user=user)

        url = reverse('profile-detail', kwargs={'pk': user.id})
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_detail_empty_fields_are_empty_string_not_null_returns_200(self):

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
        
    def test_profile_patch_requires_auth_returns_401(self):
        user = User.objects.create_user(
            username='User1',
            email='user@1.com',
            password='test123',
            type='customer',
        )
        Profile.objects.create(user=user)

        url = reverse('profile-detail', kwargs={'pk': user.id})
        res = self.client.patch(url, {'first_name': 'Monty'}, format='json')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_patch_owner_and_updates_fields_returns_200(self):
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
        self.assertEqual(res.data["working_hours"], '10-18')

        for key in ('first_name', 'last_name', 'location', 'tel', 'description', 'working_hours'):
            self.assertIsNotNone(res.data[key])

    def test_profile_patch_not_owner_returns_403(self):
        ownerUser = User.objects.create_user(
            username='OwnerUser',
            email='user@owner.com',
            password='test123',
            type='customer',
        )
        Profile.objects.create(user=ownerUser)

        strangeUser = User.objects.create_user(
            username='StrangeUser',
            email='user@strange.com',
            password='strange123',
            type='customer',
        )
        Profile.objects.create(user=strangeUser)

        self.client.force_authenticate(user=strangeUser)

        url = reverse('profile-detail', kwargs={'pk': ownerUser.id})
        res = self.client.patch(url, {'first_name': 'Stranger'}, format='json')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(res.data)

    def test_profiles_business_returns_only_business_returns_200(self):
        businessUser = User.objects.create_user(
            username='BusinessUser',
            email='user@business.com',
            password='test1234',
            type='business',
        )
        Profile.objects.create(user=businessUser)

        customerUser = User.objects.create_user(
            username='CustomerUser',
            email='user@customer.com',
            password='test123',
            type='customer'
        )
        Profile.objects.create(user=customerUser)

        self.client.force_authenticate(user=customerUser)

        url = reverse('profiles-business')
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(res.data, list))
        self.assertGreaterEqual(len(res.data), 1)

        for item in res.data:
            self.assertEqual(item['type'], 'business')

    def test_profiles_businnes_requires_auth_returns_401(self):
        url = reverse('profiles-business')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profiles_customer_returns_only_customer_returns_200(self):
        customerUser = User.objects.create_user(
            username='CustomerUser',
            email='user@customer.com',
            password='test123',
            type='customer'
        )
        Profile.objects.create(user=customerUser)

        businessUser = User.objects.create_user(
            username='BusinessUser',
            email='user@business.com',
            password='test1234',
            type='business',
        )
        Profile.objects.create(user=businessUser)

        self.client.force_authenticate(user=businessUser)

        url = reverse('profiles-customer')
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(res.data, list))
        self.assertGreaterEqual(len(res.data), 1)

        for item in res.data:
            self.assertEqual(item['type'], 'customer')
            
    def test_profiles_customer_requires_auth_returns_401(self):
        url = reverse('profiles-customer')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
            