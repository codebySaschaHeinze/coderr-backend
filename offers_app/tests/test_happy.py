from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from offers_app.models import Offer, OfferDetail


User = get_user_model()


class OfferTestsHappy(APITestCase):

    def test_offers_list_is_public_and_paginated_returns_200(self):
        businessUser = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )
        offer = Offer.objects.create(
            user=businessUser,
            title='Website Design',
            description='Ein wundervolles Website-Design'
        )
        OfferDetail.objects.create(
            offer=offer,
            title='Basic',
            revisions=5,
            delivery_time_in_days=12,
            price='234.50',
            features=['Logo Design'],
            offer_type='basic',
        )
        OfferDetail.objects.create(
            offer=offer,
            title='Standard',
            revisions=7,
            delivery_time_in_days=15,
            price='345.60',
            features=['Logo Design', 'Visitenkarten'],
            offer_type='standard',
        )
        OfferDetail.objects.create(
            offer=offer,
            title='Premium',
            revisions=3,
            delivery_time_in_days=21,
            price='456.70',
            features=['Logo Design', 'Visitenkarten', 'Flyer'],
            offer_type='premium',
        )
        
        url = reverse('offers')
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertCountEqual(res.data.keys(), ['count', 'next', 'previous', 'results'])
        self.assertTrue(isinstance(res.data['results'], list))
        self.assertGreaterEqual(len(res.data['results']), 1)

    def test_offers_create_as_business_with_three_details_returns_201(self):
        businessUser = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )
        self.client.force_authenticate(user=businessUser)

        url = reverse('offers')
        payload = {
            'title': 'Grafikdesign-Paket',
            'image': None,
            'description': 'Ein wirklich nettes Grafikdesign-Paket',
            'details': [
                {
                    'title': 'Basic',
                    'revisions': 2,
                    'delivery_time_in_days': 5,
                    'price': 123.40,
                    'features': ['Logo Design'],
                    'offer_type': 'basic',
                },
                {
                    'title': 'Standard',
                    'revisions': 1,
                    'delivery_time_in_days': 7,
                    'price': 234.50,
                    'features': ['Logo Design', 'Visitenkarten'],
                    'offer_type': 'standard',
                },
                {
                    'title': 'Premium',
                    'revisions': 4,
                    'delivery_time_in_days': 9,
                    'price': 345.60,
                    'features': ['Logo Design', 'Visitenkarten', 'Flyer'],
                    'offer_type': 'premium',
                },
            ]
        }

        res = self.client.post(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertCountEqual(res.data.keys(), ['id', 'title', 'image', 'description', 'details'])
        self.assertEqual(len(res.data['details']), 3)

        for details in res.data['details']:
            self.assertIn('id', details)
            self.assertIn('offer_type', details)

    def test_offer_detail_success_and_expected_shape_returns_200(self):
        businessUser = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )
        authUser = User.objects.create_user(
            username='authUser',
            email='user@auth.com',
            password='test123',
            type='customer',
        )
        offer = Offer.objects.create(
            user=businessUser,
            title='Website Design',
            description='Ein wundervolles Website-Design'
        )
        OfferDetail.objects.create(
            offer=offer,
            title='Basic',
            revisions=5,
            delivery_time_in_days=12,
            price='234.50',
            features=['Logo Design'],
            offer_type='basic',
        )
        OfferDetail.objects.create(
            offer=offer,
            title='Standard',
            revisions=7,
            delivery_time_in_days=15,
            price='345.60',
            features=['Logo Design', 'Visitenkarten'],
            offer_type='standard',
        )
        OfferDetail.objects.create(
            offer=offer,
            title='Premium',
            revisions=3,
            delivery_time_in_days=21,
            price='456.70',
            features=['Logo Design', 'Visitenkarten', 'Flyer'],
            offer_type='premium',
        )

        self.client.force_authenticate(user=authUser)

        url = reverse('offer-detail', kwargs={'id': offer.id})
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertCountEqual(
            res.data.keys(),
            [
                'id',
                'user',
                'title',
                'image',
                'description',
                'created_at',
                'updated_at',
                'details',
                'min_price',
                'min_delivery_time',
            ],
        )
        self.assertEqual(res.data['user'], businessUser.id)
        self.assertEqual(len(res.data['details']), 3)

    def test_offer_patch_owner_updates_title_returns_200(self):
        ownerUser = User.objects.create_user(
            username='ownerUser',
            email='user@owner.com',
            password='test123',
            type='business',
        )
        offer = Offer.objects.create(
            user=ownerUser,
            title='Website Design',
            description='Ein wundervolles Website-Design'
        )
        OfferDetail.objects.create(
            offer=offer,
            title='Basic',
            revisions=5,
            delivery_time_in_days=12,
            price='234.50',
            features=['Logo Design'],
            offer_type='basic',
        )
        OfferDetail.objects.create(
            offer=offer,
            title='Standard',
            revisions=7,
            delivery_time_in_days=15,
            price='345.60',
            features=['Logo Design', 'Visitenkarten'],
            offer_type='standard',
        )
        OfferDetail.objects.create(
            offer=offer,
            title='Premium',
            revisions=3,
            delivery_time_in_days=21,
            price='456.70',
            features=['Logo Design', 'Visitenkarten', 'Flyer'],
            offer_type='premium',
        )

        self.client.force_authenticate(user=ownerUser)

        url = reverse('offer-detail', kwargs={'id': offer.id})
        res = self.client.patch(url, {'title': 'Aktualisierter Titel'}, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], 'Aktualisierter Titel')
        self.assertEqual(len(res.data['details']), 3)

    def test_offer_delete_as_owner_returns_204(self):
        ownerUser = User.objects.create_user(
            username='ownerUser',
            email='user@owner.com',
            password='test123',
            type='business',
        )
        offer = Offer.objects.create(
            user=ownerUser, 
            title='Schöner Titel', 
            description='Schöne Beschreibung'
        )
        OfferDetail.objects.create(
            offer=offer,
            title='Basic',
            revisions=1,
            delivery_time_in_days=1,
            price='123.40',
            features=[],
            offer_type='basic',
        )
        OfferDetail.objects.create(
            offer=offer,
            title='Standard',
            revisions=1,
            delivery_time_in_days=1,
            price='234.50',
            features=[],
            offer_type='standard',
        )
        OfferDetail.objects.create(
            offer=offer,
            title='Premium',
            revisions=1,
            delivery_time_in_days=1,
            price='345.60',
            features=[],
            offer_type='premium',
        )

        self.client.force_authenticate(user=ownerUser)

        url = reverse('offer-detail', kwargs={'id': offer.id})
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Offer.objects.filter(id=offer.id).exists())

    def test_offerdetail_success_and_expected_shape_returns_200(self):
        businessUser = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )
        authUser = User.objects.create_user(
            username='authUser',
            email='user@auth.com',
            password='test123',
            type='customer',
        )

        offer = Offer.objects.create(
            user=businessUser,
            title='Website Design',
            description='Ein wundervolles Website-Design'
        )
        detail = OfferDetail.objects.create(
            offer=offer,
            title='Basic',
            revisions=5,
            delivery_time_in_days=12,
            price='234.50',
            features=['Logo Design'],
            offer_type='basic',
        )

        self.client.force_authenticate(user=authUser)

        url = reverse('offer-detail-item', kwargs={'id': detail.id})
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertCountEqual(
            res.data.keys(),
            ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']
        )