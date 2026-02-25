from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from profile_app.models import Profile


User = get_user_model()


class ProfileTests(APITestCase):
    """Unhappy-path tests for profile detail and profile list endpoints."""

    def test_profile_detail_requires_auth_returns_401(self):
        """Profile detail without authentication returns status 401."""
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
        """Profile patch without authentication returns status 401."""
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
        """Profile patch by non-owner returns status 403."""
        owner_user = User.objects.create_user(
            username='OwnerUser',
            email='user@owner.com',
            password='test123',
            type='customer',
        )
        Profile.objects.create(user=owner_user)

        strange_user = User.objects.create_user(
            username='StrangeUser',
            email='user@strange.com',
            password='strange123',
            type='customer',
        )
        Profile.objects.create(user=strange_user)

        self.client.force_authenticate(user=strange_user)

        url = reverse('profile-detail', kwargs={'pk': owner_user.id})
        res = self.client.patch(url, {'first_name': 'Stranger'}, format='json')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(res.data)

    def test_profiles_businnes_requires_auth_returns_401(self):
        """Business profile list without authentication returns status 401."""
        url = reverse('profiles-business')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profiles_customer_requires_auth_returns_401(self):
        """Customer profile list without authentication returns status 401."""
        url = reverse('profiles-customer')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_detail_invalid_pk_returns_404(self):
        """Profile detail with invalid user ID returns status 404."""
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