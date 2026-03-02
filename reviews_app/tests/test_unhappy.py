from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from reviews_app.models import Review


User = get_user_model()


class ReviewTestsUnhappy(APITestCase):
    """Unhappy-path tests for review endpoints."""

    def test_reviews_list_requires_auth_returns_401(self):
        """Review list without authentication returns status 401."""
        url = reverse('reviews')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reviews_create_requires_auth_returns_401(self):
        """Review creation without authentication returns status 401."""
        url = reverse('reviews')
        res = self.client.post(
            url,
            {'business_user': 1, 'rating': 4, 'description': 'Alles gut soweit.'},
            format='json',
        )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reviews_create_requires_customer_type_returns_403(self):
        """Review creation by business user returns status 403."""
        business_user_1 = User.objects.create_user(
            username='businessUser1',
            email='user@business1.com',
            password='test123',
            type='business',
        )
        business_user_2 = User.objects.create_user(
            username='businessUser2',
            email='user@business2.com',
            password='test123',
            type='business',
        )

        self.client.force_authenticate(user=business_user_1)

        url = reverse('reviews')
        res = self.client.post(
            url,
            {'business_user': business_user_2.id, 'rating': 4, 'description': 'Nicht erlaubt!'},
            format='json',
        )

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', res.data)

    def test_reviews_create_duplicate_review_returns_403(self):
        """Duplicate review creation for same business/reviewer returns status 403."""
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
        payload = {
            'business_user': business_user.id,
            'rating': 4,
            'description': 'Erster!',
        }

        self.client.post(url, payload, format='json')
        res = self.client.post(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', res.data)

    def test_reviews_create_business_user_must_be_business_returns_400(self):
        """Review creation with non-business target returns status 400."""
        customer_user = User.objects.create_user(
            username='CustomerUser',
            email='user@customer.com',
            password='test123',
            type='customer',
        )
        not_business_user = User.objects.create_user(
            username='NotBusinessUser',
            email='user@notbusiness.com',
            password='test123',
            type='customer',
        )

        self.client.force_authenticate(user=customer_user)

        url = reverse('reviews')
        res = self.client.post(
            url,
            {
                'business_user': not_business_user.id,
                'rating': 4,
                'description': 'Sollte fehlschlagen',
            },
            format='json',
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Review.objects.count(), 0)

    def test_review_patch_requires_auth_returns_401(self):
        """Review patch without authentication returns status 401."""
        business_user = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )
        review = Review.objects.create(
            business_user=business_user,
            reviewer=business_user,
            rating=4,
            description='Ok.',
        )

        url = reverse('review-detail', kwargs={'id': review.id})
        res = self.client.patch(url, {'rating': 5}, format='json')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_patch_not_owner_returns_403(self):
        """Review patch by non-owner returns status 403."""
        reviewer_user = User.objects.create_user(
            username='reviewerUser',
            email='user@reviewer.de',
            password='test123',
            type='customer',
        )
        other_user = User.objects.create_user(
            username='otherUser',
            email='user@other.de',
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

        self.client.force_authenticate(user=other_user)

        url = reverse('review-detail', kwargs={'id': review.id})
        res = self.client.patch(url, {'rating': 5}, format='json')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_patch_disallowed_field_returns_400(self):
        """Review patch with disallowed field returns status 400."""
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
        res = self.client.patch(url, {'business_user': business_user.id}, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_delete_requires_auth_returns_401(self):
        """Review delete without authentication returns status 401."""
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

        url = reverse('review-detail', kwargs={'id': review.id})
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_delete_not_owner_returns_403(self):
        """Review delete by non-owner returns status 403."""
        reviewer_user = User.objects.create_user(
            username='reviewerUser',
            email='user@reviewer.de',
            password='test123',
            type='customer',
        )
        other_user = User.objects.create_user(
            username='otherUser',
            email='user@other.de',
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

        self.client.force_authenticate(user=other_user)

        url = reverse('review-detail', kwargs={'id': review.id})
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_delete_invalid_id_returns_404(self):
        """Review delete with invalid ID returns status 404."""
        auth_user = User.objects.create_user(
            username='authUser',
            email='user@auth.de',
            password='test123',
            type='customer',
        )
        self.client.force_authenticate(user=auth_user)

        url = reverse('review-detail', kwargs={'id': 999999999999})
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)