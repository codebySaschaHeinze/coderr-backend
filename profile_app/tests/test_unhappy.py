from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from profile_app.models import Profile


User = get_user_model()


class ProfileTests(APITestCase):

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

    def test_profiles_businnes_requires_auth_returns_401(self):
        url = reverse('profiles-business')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
            
    def test_profiles_customer_requires_auth_returns_401(self):
        url = reverse('profiles-customer')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
            
    def test_profile_detail_invalid_pk_returns_404(self):
        user = User.objects.create_user(
            username='User1',
            email='user@1.com',
            password='test123',
            type='customer',
        )
        Profile.objects.create(user=user)
        self.client.force_authenticate(user=user)

        url = reverse('profile-detail', kwargs={'pk': 999999})
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)