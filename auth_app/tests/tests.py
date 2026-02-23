from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from profile_app.models import Profile


User = get_user_model()


class AuthTests(APITestCase):

    def test_registration_returns_token_and_creates_profile(self):
        url = reverse('registration')
        payload = {
            'username': 'User1',
            'email': 'user@1.com',
            'password': 'test123',
            'repeated_password': 'test123',
            'type': 'customer',
        }

        res = self.client.post(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertCountEqual(res.data.keys(), ['token', 'username', 'email', 'user_id'])

        user = User.objects.get(id=res.data['user_id'])
        self.assertTrue(Profile.objects.filter(user=user).exists())
        self.assertTrue(Token.objects.filter(user=user).exists())

    def test_login_success_returns_token_and_user_fields(self):
        User.objects.create_user(
            username="User1",
            email="user@1.com",
            password="test123",
            type="customer",
        )

        login_url = reverse("login")
        res = self.client.post(
            login_url,
            {"username": "User1", "password": "test123"},
            format="json",
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertCountEqual(res.data.keys(), ["token", "username", "email", "user_id"])
        self.assertTrue(res.data["token"])

    def test_login_with_wrong_password_returns_400(self):
        User.objects.create_user(
            username='User2',
            email='user@2.com',
            password='correctpw',
            type='business'
        )

        url = reverse('login')
        res = self.client.post(url, {'username': 'User2','password': 'wrongpw'}, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(res.data)

    def test_registration_duplicate_email_returns_400(self):
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
        User.objects.create_user(
            username="Existing",
            email="ex@mail.de",
            password="correctPW123",
            type="customer",
        )

        login_url = reverse("login")
        res = self.client.post(
            login_url,
            {"username": "DoesNotExist", "password": "whatever"},
            format="json",
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(res.data)



