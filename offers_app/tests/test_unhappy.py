from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from offers_app.models import Offer, OfferDetail


User = get_user_model()


class OffersTestsUnhappy(APITestCase):

    def test_offers_create_requires_auth_returns_401(self):
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
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offers_create_as_customer_resturns_403(self):
        customerUser = User.objects.create_user(
            username='customerUser',
            email='user@customer.com',
            password='test123',
            type='customer',
        )
        self.client.force_authenticate(user=customerUser)

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
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(res.data)

    def test_offers_create_requires_three_details_returns_400(self):
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
                    'title': 'Nur ein Detail',
                    'revisions': 2,
                    'delivery_time_in_days': 5,
                    'price': 123.40,
                    'features': ['Logo Design'],
                    'offer_type': 'basic',
                },
            ]
        }

        res = self.client.post(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(res.data)

    def test_offer_detail_requires_auth_returns_401(self):
        businessUser = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )
        offer = Offer.objects.create(
            user=businessUser, 
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

        url = reverse('offer-detail', kwargs={'id': offer.id})
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offer_detail_invalid_id_returns_404(self):
        authUser = User.objects.create_user(
            username='authUser',
            email='user@auth.com',
            password='test123',
            type='customer',
        )
        self.client.force_authenticate(user=authUser)

        url = reverse('offer-detail', kwargs={'id': 9999999999999999999})
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(res.data)

    def test_offer_patch_requires_auth_returns_401(self):
        businessUser = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )
        offer = Offer.objects.create(
            user=businessUser, 
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

        url = reverse('offer-detail', kwargs={'id': offer.id})
        res = self.client.patch(url, {'title': 'Keine Authorisierung'}, format='json')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offer_patch_not_owner_returns_403(self):
        ownerUser = User.objects.create_user(
            username='ownerUser',
            email='user@owner.com',
            password='test123',
            type='business',
        )
        notOwnerUser = User.objects.create_user(
            username='notOwnerUser',
            email='user@notowner.com',
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

        self.client.force_authenticate(user=notOwnerUser)

        url = reverse('offer-detail', kwargs={'id': offer.id})
        res = self.client.patch(url, {'title': 'Nicht der Besitzer'}, format='json')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(res.data)

    def test_offer_patch_detail_without_offer_type_returns_400(self):
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
        res = self.client.patch(url, {'details': [{'title': 'Kein Angebots-Detail'}]}, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(res.data)

    def test_offer_delete_requires_auth_returns_401(self):
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

        url = reverse('offer-detail', kwargs={'id': offer.id})
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offer_delete_as_not_owner_returns_403(self):
        ownerUser = User.objects.create_user(
            username='ownerUser',
            email='user@owner.com',
            password='test123',
            type='business',
        )
        notOwnerUser = User.objects.create_user(
            username='notOwnerUser',
            email='user@notowner.com',
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

        self.client.force_authenticate(user=notOwnerUser)

        url = reverse('offer-detail', kwargs={'id': offer.id})
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(res.data)

    def test_offerdetail_requires_auth_returns_401(self):
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
        detail = OfferDetail.objects.create(
            offer=offer,
            title='Basic',
            revisions=5,
            delivery_time_in_days=12,
            price='234.50',
            features=['Logo Design'],
            offer_type='basic',
        )
        
        url = reverse('offer-detail-item', kwargs={'id': detail.id})
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offerdetail_invalid_id_returns_404(self):
        authUser = User.objects.create_user(
            username='authUser',
            email='user@auth.com',
            password='test123',
            type='customer',
        )
        self.client.force_authenticate(user=authUser)

        url = reverse('offer-detail-item', kwargs={'id': 99999999999999})
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(res.data)