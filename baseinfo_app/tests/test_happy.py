from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from offers_app.models import Offer
from reviews_app.models import Review


User = get_user_model()


class BaseInfoTestsHappy(APITestCase):

    def test_base_info_and_expected_aggregations_returns_200(self):
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
        customerUser = User.objects.create_user(
            username='CustomerUser',
            email='user@customer.com',
            password='test123',
            type='customer',
        )

        Offer.objects.create(
            user=businessUser1,
            title='AAAAA',
            description='DDDDD',
        )
        Offer.objects.create(
            user=businessUser2,
            title='BBBBB',
            description='DDDDD',
        )
        Offer.objects.create(
            user=businessUser2,
            title='CCCCC',
            description='DDDDD',
        )

        Review.objects.create(
            business_user=businessUser1,
            reviewer=customerUser,
            rating=4,
            description='ok',
        )
        Review.objects.create(
            business_user=businessUser2,
            reviewer=customerUser,
            rating=5,
            description='ok',
        )

        url = reverse('base-info')
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertCountEqual(
            res.data.keys(),
            ['review_count', 'average_rating', 'business_profile_count', 'offer_count'],
        )

        self.assertEqual(res.data['review_count'], 2)
        self.assertEqual(res.data['offer_count'], 3)
        self.assertEqual(res.data['business_profile_count'], 2)
        self.assertEqual(res.data['average_rating'], 4.5)