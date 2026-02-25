from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from reviews_app.models import Review


User = get_user_model()


class ReviewTestsHappy(APITestCase):
    """Happy-path tests for review endpoints."""

    def test_reviews_list_as_auth_and_expected_shape_returns_200(self):
        """Authenticated user can list reviews and receives expected shape."""
        auth_user = User.objects.create_user(
            username='CustomerUser',
            email='user@customer.com',
            password='test123',
            type='customer',
        )
        business_user = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )
        Review.objects.create(
            business_user=business_user,
            reviewer=auth_user,
            rating=4,
            description='Sehr professionell.',
        )

        self.client.force_authenticate(user=auth_user)

        url = reverse('reviews')
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(res.data, list))
        self.assertGreaterEqual(len(res.data), 1)
        self.assertCountEqual(
            res.data[0].keys(),
            [
                'id',
                'business_user',
                'reviewer',
                'rating',
                'description',
                'created_at',
                'updated_at',
            ],
        )

    def test_reviews_create_as_customer_and_expected_shape_returns_201(self):
        """Customer can create a review and receives expected response shape."""
        customer_user = User.objects.create_user(
            username='CustomerUser',
            email='user@customer.com',
            password='test123',
            type='customer',
        )
        business_user = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )

        self.client.force_authenticate(user=customer_user)

        url = reverse('reviews')
        res = self.client.post(
            url,
            {'business_user': business_user.id, 'rating': 3, 'description': 'Alles gut soweit'},
            format='json',
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertCountEqual(
            res.data.keys(),
            [
                'id',
                'business_user',
                'reviewer',
                'rating',
                'description',
                'created_at',
                'updated_at',
            ],
        )

        self.assertEqual(res.data['business_user'], business_user.id)
        self.assertEqual(res.data['reviewer'], customer_user.id)

    def test_review_patch_owner_updates_fields_returns_200(self):
        """Review owner can update rating and description with status 200."""
        reviewer_user = User.objects.create_user(
            username='reviewerUser',
            email='user@reviewer.de',
            password='test123',
            type='customer',
        )
        business_user = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )

        review = Review.objects.create(
            business_user=business_user,
            reviewer=reviewer_user,
            rating=4,
            description='Ok',
        )

        self.client.force_authenticate(user=reviewer_user)

        url = reverse('review-detail', kwargs={'id': review.id})
        res = self.client.patch(
            url,
            {'rating': 5, 'description': 'Noch besser als erwartet!'},
            format='json',
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['rating'], 5)
        self.assertEqual(res.data['description'], 'Noch besser als erwartet!')

    def test_review_delete_owner_returns_204(self):
        """Review owner can delete a review and receives status 204."""
        reviewer_user = User.objects.create_user(
            username='reviewerUser',
            email='user@reviewer.de',
            password='test123',
            type='customer',
        )
        business_user = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )
        review = Review.objects.create(
            business_user=business_user,
            reviewer=reviewer_user,
            rating=4,
            description='Ok',
        )

        self.client.force_authenticate(user=reviewer_user)

        url = reverse('review-detail', kwargs={'id': review.id})
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.filter(id=review.id).exists())