from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from offers_app.models import Offer, OfferDetail
from orders_app.models import Order


User = get_user_model()


class OrderTestsHappy(APITestCase):
    
    def test_orders_create_as_customer_expected_shape_and_returns_201(self):
        businessUser = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )
        customerUser = User.objects.create_user(
            username='CustomerUser',
            email='user@customer.com',
            password='test123',
            type='customer',
        )

        offer = Offer.objects.create(
            user=businessUser,
            title='Logo Design',
            description='Ein ziemlich nices Logo',
        )
        offer_detail = OfferDetail.objects.create(
            offer=offer,
            title='Logo Design',
            revisions=3,
            delivery_time_in_days=5,
            price='123.45',
            features=['Logo Design', 'Visitenkarten'],
            offer_type='basic',
        )

        self.client.force_authenticate(user=customerUser)

        url = reverse('order')
        res = self.client.post(url, {'offer_detail_id': offer_detail.id}, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertCountEqual(
            res.data.keys(),
            [
                'id',
                'customer_user',
                'business_user',
                'title',
                'revisions',
                'delivery_time_in_days',
                'price',
                'features',
                'offer_type',
                'status',
                'created_at',
                'updated_at',
            ],
        )
        self.assertEqual(res.data['customer_user'], customerUser.id)
        self.assertEqual(res.data['business_user'], businessUser.id)
        self.assertEqual(res.data['offer_type'], 'basic')
        self.assertEqual(res.data['status'], 'in_progress')

    def test_orders_list_returns_only_related_orders_returns_200(self):
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
        customerUser1 = User.objects.create_user(
            username='CustomerUser1',
            email='user@customer1.com',
            password='test123',
            type='customer',
        )
        customerUser2 = User.objects.create_user(
            username='CustomerUser2',
            email='user@customer2.com',
            password='test123',
            type='customer',
        )

        Order.objects.create(
            customer_user=customerUser1,
            business_user=businessUser1,
            title='AAAAA',
            revisions=1,
            delivery_time_in_days=5,
            price='250.00',
            features=[],
            offer_type='basic',
            status='in_progress',
        )
        Order.objects.create(
            customer_user=customerUser1,
            business_user=businessUser2,
            title='BBBBB',
            revisions=2,
            delivery_time_in_days=7,
            price='230.00',
            features=[],
            offer_type='basic',
            status='in_progress',
        )
        Order.objects.create(
            customer_user=customerUser2,
            business_user=businessUser1,
            title='CCCCC',
            revisions=4,
            delivery_time_in_days=3,
            price='280.00',
            features=[],
            offer_type='standard',
            status='in_progress',
        )
        self.client.force_authenticate(user=customerUser1)

        url = reverse('order')
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

        for item in res.data:
            self.assertEqual(item['customer_user'], customerUser1.id)

    def test_order_patch_as_business_updates_status_returns_200(self):
        businessUser = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )
        customerUser = User.objects.create_user(
            username='CustomerUser',
            email='user@customer.com',
            password='test123',
            type='customer',
        )
        order = Order.objects.create(
            customer_user=customerUser,
            business_user=businessUser,
            title='AAAAA',
            revisions=6,
            delivery_time_in_days=12,
            price='380.00',
            features=[],
            offer_type='standard',
            status='in_progress',
        )
        self.client.force_authenticate(user=businessUser)

        url = reverse('order-detail', kwargs={'id': order.id})
        res = self.client.patch(url, {'status': 'completed'}, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['status'], 'completed')

    def test_order_delete_as_staff_returns_204(self):
        businessUser = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )
        customerUser = User.objects.create_user(
            username='CustomerUser',
            email='user@customer.com',
            password='test123',
            type='customer',
        )
        staffUser = User.objects.create_user(
            username='Admin',
            email='user@admin.com',
            password='test123',
            type='business',
            is_staff=True,
        )
        order = Order.objects.create(
            customer_user=customerUser,
            business_user=businessUser,
            title='AAAAA',
            revisions=2,
            delivery_time_in_days=4,
            price='210.00',
            features=[],
            offer_type='premium',
            status='in_progress',
        )
        
        self.client.force_authenticate(user=staffUser)

        url = reverse('order-detail', kwargs={'id': order.id})
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(id=order.id).exists())

    def test_order_count_returns_correct_number_returns_200(self):
        businessUser = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )
        customerUser = User.objects.create_user(
            username='CustomerUser',
            email='user@customer.com',
            password='test123',
            type='customer',
        )
        Order.objects.create(
            customer_user=customerUser,
            business_user=businessUser,
            title='AAAAA',
            revisions=6,
            delivery_time_in_days=2,
            price='270.00',
            features=[],
            offer_type='basic',
            status='in_progress',
        )
        Order.objects.create(
            customer_user=customerUser,
            business_user=businessUser,
            title='BBBBB',
            revisions=7,
            delivery_time_in_days=4,
            price='210.00',
            features=[],
            offer_type='premium',
            status='in_progress',
        )
        Order.objects.create(
            customer_user=customerUser,
            business_user=businessUser,
            title='CCCCC',
            revisions=5,
            delivery_time_in_days=3,
            price='240.00',
            features=[],
            offer_type='standard',
            status='completed',
        )

        self.client.force_authenticate(user=customerUser)

        url = reverse('order-count', kwargs={'business_user_id': businessUser.id})
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['order_count'], 2)

    def test_completed_order_count_returns_correct_number_returns_200(self):
        businessUser = User.objects.create_user(
            username='businessUser',
            email='user@business.com',
            password='test123',
            type='business',
        )
        customerUser = User.objects.create_user(
            username='CustomerUser',
            email='user@customer.com',
            password='test123',
            type='customer',
        )
        Order.objects.create(
            customer_user=customerUser,
            business_user=businessUser,
            title='AAAAA',
            revisions=6,
            delivery_time_in_days=2,
            price='270.00',
            features=[],
            offer_type='basic',
            status='completed',
        )
        Order.objects.create(
            customer_user=customerUser,
            business_user=businessUser,
            title='BBBBB',
            revisions=7,
            delivery_time_in_days=4,
            price='210.00',
            features=[],
            offer_type='premium',
            status='completed',
        )
        Order.objects.create(
            customer_user=customerUser,
            business_user=businessUser,
            title='CCCCC',
            revisions=5,
            delivery_time_in_days=3,
            price='240.00',
            features=[],
            offer_type='standard',
            status='in_progress',
        )

        self.client.force_authenticate(user=customerUser)

        url = reverse('completed-order-count', kwargs={'business_user_id': businessUser.id})
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['completed_order_count'], 2)