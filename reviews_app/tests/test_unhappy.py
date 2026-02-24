from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from reviews_app.models import Review


User = get_user_model()


class ReviewTestsUnhappy(APITestCase):

    def test_reviews_list_requires_auth_returns_401(self):
        url = reverse('reviews')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reviews_create_requires_auth_returns_401(self):
        url = reverse('reviews')
        res = self.client.post(
            url, 
            {'business_user': 1, 'rating': 4, 'description': 'Alles gut soweit.'},
            format='json',
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reviews_create_requires_customer_type_returns_401(self):
        businessUser1 = User.objects.create_user(
            username='businessUser1',
            email='user@business1.com',
            password='test123',
            type='business',
        )
        businessUser2 = User.objects.create_user(
            username='businessUser2',
            email='user@business2.com',
            password='test123',
            type='business',
        )

        self.client.force_authenticate(user=businessUser1)

        url = reverse('reviews')
        res = self.client.post(
            url,
            {'business_user': businessUser2.id, 'rating': 4, 'description': 'Nicht erlaubt!'},
            format='json',
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED) 

    def test_reviews_create_duplicate_review_returns_403(self):
        customerUser = User.objects.create_user(
            username='CustomerUser',
            email='user@customer.com',
            password='test123',
            type='customer',
        )
        businessUser = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )

        self.client.force_authenticate(user=customerUser)

        url = reverse('reviews')
        payload = {
            'business_user': businessUser.id,
            'rating': 4,
            'description': 'Erster!'
        }

        self.client.post(url, payload, format='json')
        res = self.client.post(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_patch_requires_auth_returns_401(self):
        customerUser = User.objects.create_user(
            username='CustomerUser',
            email='user@customer.com',
            password='test123',
            type='customer',
        )
        businessUser = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )
        review = Review.objects.create(
            business_user=businessUser,
            reviewer=businessUser,
            rating=4,
            description='Ok.',
        )

        url = reverse('review-detail', kwargs={'id': review.id})
        res = self.client.patch(url, {'rating': 5}, format='json')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_patch_not_owner_returns_403(self):
        reviewerUser = User.objects.create_user(
            username='reviewerUser',
            email='user@reviewer.de',
            password='test123',
            type='customer',
        )
        otherUser = User.objects.create_user(
            username='otherUser',
            email='user@other.de',
            password='test123',
            type='customer',
        )
        businessUser = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )
        review = Review.objects.create(
            business_user=businessUser,
            reviewer=reviewerUser,
            rating=4,
            description='Ok',
        )

        self.client.force_authenticate(user=otherUser)

        url = reverse('review-detail', kwargs={'id': review.id})
        res = self.client.patch(url, {'rating': 5}, format='json')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_patch_disallowed_field_returns_400(self):
        reviewerUser = User.objects.create_user(
            username='reviewerUser',
            email='user@reviewer.de',
            password='test123',
            type='customer',
        )
        businessUser = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )
        review = Review.objects.create(
            business_user=businessUser,
            reviewer=reviewerUser,
            rating=4,
            description='Ok',
        )

        self.client.force_authenticate(user=reviewerUser)

        url = reverse('review-detail', kwargs={'id': review.id})
        res = self.client.patch(url, {'business_user': businessUser.id}, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_delete_requires_auth_returns_401(self):
        reviewerUser = User.objects.create_user(
            username='reviewerUser',
            email='user@reviewer.de',
            password='test123',
            type='customer',
        )
        businessUser = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )
        review = Review.objects.create(
            business_user=businessUser,
            reviewer=reviewerUser,
            rating=4,
            description='Ok',
        )

        url = reverse('review-detail', kwargs={'id': review.id})
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_review_delete_not_owner_returns_403(self):
        reviewerUser = User.objects.create_user(
            username='reviewerUser',
            email='user@reviewer.de',
            password='test123',
            type='customer',
        )
        otherUser = User.objects.create_user(
            username='otherUser',
            email='user@other.de',
            password='test123',
            type='customer',
        )
        businessUser = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )
        review = Review.objects.create(
            business_user=businessUser,
            reviewer=reviewerUser,
            rating=4,
            description='Ok',
        )

        self.client.force_authenticate(user=otherUser)

        url = reverse('review-detail', kwargs={'id': review.id})
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_delete_invalid_id_returns_404(self):
        authUser = User.objects.create_user(
            username='authUser',
            email='user@auth.de',
            password='test123',
            type='customer',
        )
        self.client.force_authenticate(user=authUser)

        url = reverse('review-detail', kwargs={'id': 999999999999})
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)