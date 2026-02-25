from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class AuthTestsUnhappy(APITestCase):
    """Unhappy-path tests for registration and login endpoints."""

    def test_login_with_wrong_password_returns_400(self):
        """Login with wrong password returns status 400."""
        User.objects.create_user(
            username='User2',
            email='user@2.com',
            password='correctpw',
            type='business',
        )

        url = reverse('login')
        res = self.client.post(
            url,
            {'username': 'User2', 'password': 'wrongpw'},
            format='json',
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(res.data)

    def test_registration_duplicate_email_returns_400(self):
        """Registration with duplicate email returns status 400."""
        url = reverse('registration')
        payload = {
            'username': 'User1',
            'email': 'dup@mail.com',
            'password': 'test123',
            'repeated_password': 'test123',
            'type': 'customer',
        }

        res1 = self.client.post(url, payload, format='json')
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)

        payload['username'] = 'User2'
        res2 = self.client.post(url, payload, format='json')
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_password_mismatch_returns_400(self):
        """Registration with mismatched passwords returns status 400."""
        url = reverse('registration')
        payload = {
            'username': 'User3',
            'email': 'user@3.com',
            'password': 'test123',
            'repeated_password': 'test123456789',
            'type': 'customer',
        }

        res = self.client.post(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('repeated_password', res.data)
        self.assertTrue(res.data)

    def test_login_unknown_user_returns_400(self):
        """Login with unknown username returns status 400."""
        User.objects.create_user(
            username='Existing',
            email='ex@mail.de',
            password='correctPW123',
            type='customer',
        )

        login_url = reverse('login')
        res = self.client.post(
            login_url,
            {'username': 'DoesNotExist', 'password': 'whatever'},
            format='json',
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(res.data)