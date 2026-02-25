from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from offers_app.models import Offer, OfferDetail


User = get_user_model()


class OffersTestsUnhappy(APITestCase):
    """Unhappy-path tests for offer and offer-detail endpoints."""

    def test_offers_create_requires_auth_returns_401(self):
        """Offer creation without authentication returns status 401."""
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
            ],
        }

        res = self.client.post(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_offers_create_as_customer_returns_403(self):
        """Offer creation as customer user returns status 403."""
        customer_user = User.objects.create_user(
            username='customerUser',
            email='user@customer.com',
            password='test123',
            type='customer',
        )
        self.client.force_authenticate(user=customer_user)

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
            ],
        }

        res = self.client.post(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(res.data)

    def test_offers_create_requires_three_details_returns_400(self):
        """Offer creation with fewer than three details returns status 400."""
        business_user = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )
        self.client.force_authenticate(user=business_user)

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
            ],
        }

        res = self.client.post(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(res.data)

    def test_offer_detail_requires_auth_returns_401(self):
        """Offer detail retrieval without authentication returns status 401."""
        business_user = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )
        offer = Offer.objects.create(
            user=business_user,
            title='Schöner Titel',
            description='Schöne Beschreibung',
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
        """Offer detail retrieval with invalid ID returns status 404."""
        auth_user = User.objects.create_user(
            username='authUser',
            email='user@auth.com',
            password='test123',
            type='customer',
        )
        self.client.force_authenticate(user=auth_user)

        url = reverse('offer-detail', kwargs={'id': 9999999999999999999})
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(res.data)

    def test_offer_patch_requires_auth_returns_401(self):
        """Offer patch without authentication returns status 401."""
        business_user = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )
        offer = Offer.objects.create(
            user=business_user,
            title='Schöner Titel',
            description='Schöne Beschreibung',
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
        """Offer patch by non-owner returns status 403."""
        owner_user = User.objects.create_user(
            username='ownerUser',
            email='user@owner.com',
            password='test123',
            type='business',
        )
        not_owner_user = User.objects.create_user(
            username='notOwnerUser',
            email='user@notowner.com',
            password='test123',
            type='business',
        )
        offer = Offer.objects.create(
            user=owner_user,
            title='Schöner Titel',
            description='Schöne Beschreibung',
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

        self.client.force_authenticate(user=not_owner_user)

        url = reverse('offer-detail', kwargs={'id': offer.id})
        res = self.client.patch(url, {'title': 'Nicht der Besitzer'}, format='json')

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(res.data)

    def test_offer_patch_detail_without_offer_type_returns_400(self):
        """Offer patch with nested detail missing offer_type returns status 400."""
        owner_user = User.objects.create_user(
            username='ownerUser',
            email='user@owner.com',
            password='test123',
            type='business',
        )
        offer = Offer.objects.create(
            user=owner_user,
            title='Website Design',
            description='Ein wundervolles Website-Design',
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

        self.client.force_authenticate(user=owner_user)

        url = reverse('offer-detail', kwargs={'id': offer.id})
        res = self.client.patch(
            url,
            {'details': [{'title': 'Kein Angebots-Detail'}]},
            format='json',
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(res.data)

    def test_offer_delete_requires_auth_returns_401(self):
        """Offer delete without authentication returns status 401."""
        owner_user = User.objects.create_user(
            username='ownerUser',
            email='user@owner.com',
            password='test123',
            type='business',
        )
        offer = Offer.objects.create(
            user=owner_user,
            title='Website Design',
            description='Ein wundervolles Website-Design',
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
        """Offer delete by non-owner returns status 403."""
        owner_user = User.objects.create_user(
            username='ownerUser',
            email='user@owner.com',
            password='test123',
            type='business',
        )
        not_owner_user = User.objects.create_user(
            username='notOwnerUser',
            email='user@notowner.com',
            password='test123',
            type='business',
        )
        offer = Offer.objects.create(
            user=owner_user,
            title='Schöner Titel',
            description='Schöne Beschreibung',
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

        self.client.force_authenticate(user=not_owner_user)

        url = reverse('offer-detail', kwargs={'id': offer.id})
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(res.data)

    def test_offerdetail_requires_auth_returns_401(self):
        """Offer-detail item retrieval without authentication returns status 401."""
        business_user = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )
        offer = Offer.objects.create(
            user=business_user,
            title='Website Design',
            description='Ein wundervolles Website-Design',
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
        """Offer-detail item retrieval with invalid ID returns status 404."""
        auth_user = User.objects.create_user(
            username='authUser',
            email='user@auth.com',
            password='test123',
            type='customer',
        )
        self.client.force_authenticate(user=auth_user)

        url = reverse('offer-detail-item', kwargs={'id': 99999999999999})
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(res.data)