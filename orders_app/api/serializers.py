from rest_framework import serializers

from orders_app.models import Order
from .validators import get_offer_detail_or_404


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for order read and status update operations."""

    class Meta:
        model = Order
        fields = [
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
        ]
        read_only_fields = [
            'id',
            'customer_user',
            'business_user',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'created_at',
            'updated_at',
        ]


class OrderCreateSerializer(serializers.Serializer):
    """Serializer for creating an order from an offer detail."""

    offer_detail_id = serializers.IntegerField()

    def create(self, validated_data):
        """Create an order from the selected offer detail."""
        request = self.context['request']
        detail = get_offer_detail_or_404(validated_data['offer_detail_id'])

        order = Order.objects.create(
            customer_user=request.user,
            business_user=detail.offer.user,
            title=detail.title,
            revisions=detail.revisions,
            delivery_time_in_days=detail.delivery_time_in_days,
            price=detail.price,
            features=detail.features,
            offer_type=detail.offer_type,
            status='in_progress',
        )

        return order