from rest_framework import serializers

from offers_app.models import Offer, OfferDetail
from .validators import validate_offer_details_count, validate_offer_type_for_update


class OfferDetailSerializer(serializers.ModelSerializer):
    """Serializer for offer detail packages."""

    class Meta:
        model = OfferDetail
        fields = [
            'id',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
        ]


class OfferDetailLinkSerializer(serializers.ModelSerializer):
    """Serializer that exposes offer-detail links."""

    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        """Build an absolute URL for an offer detail if request is available."""
        request = self.context.get('request')
        path = f'/api/offerdetails/{obj.id}/'
        return request.build_absolute_uri(path) if request else path


class OfferListSerializer(serializers.ModelSerializer):
    """Serializer for listing offers with aggregated and user-related data."""

    user = serializers.IntegerField(source='user.id', read_only=True)
    details = OfferDetailLinkSerializer(many=True, read_only=True)

    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
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
            'user_details',
        ]

    def get_min_price(self, obj):
        """Return annotated minimum price if available."""
        return getattr(obj, 'min_price', None)

    def get_min_delivery_time(self, obj):
        """Return annotated minimum delivery time if available."""
        return getattr(obj, 'min_delivery_time', None)

    def get_user_details(self, obj):
        """Return selected profile and username information for the offer owner."""
        profile = getattr(obj.user, 'profile', None)
        return {
            'first_name': getattr(profile, 'first_name', '') or '',
            'last_name': getattr(profile, 'last_name', '') or '',
            'username': obj.user.username,
        }


class OfferCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating offers with nested offer details."""

    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            'id',
            'title',
            'image',
            'description',
            'details',
        ]

    def validate_details(self, details):
        """Validate the number of nested offer details."""
        return validate_offer_details_count(details)

    def create(self, validated_data):
        """Create an offer and its related offer details."""
        details_data = validated_data.pop('details')
        request = self.context.get('request')
        offer = Offer.objects.create(user=request.user, **validated_data)

        OfferDetail.objects.bulk_create(
            [OfferDetail(offer=offer, **details) for details in details_data]
        )

        return offer

    def to_representation(self, instance):
        """Return created offer representation with expanded detail objects."""
        data = super().to_representation(instance)
        data['details'] = OfferDetailSerializer(instance.details.all(), many=True).data
        return data


class OfferUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating an offer and selected nested details."""

    details = OfferDetailSerializer(many=True, required=False)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def update(self, instance, validated_data):
        """Update offer fields and nested details by offer_type."""
        details_data = validated_data.pop('details', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data is not None:
            details_by_type = {d.offer_type: d for d in instance.details.all()}
            for d in details_data:
                offer_type = d.get('offer_type')
                validate_offer_type_for_update(offer_type, set(details_by_type.keys()))
                detail_obj = details_by_type[offer_type]
                for k, v in d.items():
                    setattr(detail_obj, k, v)
                detail_obj.save()

        return instance


class OfferDetailViewSerializer(serializers.ModelSerializer):
    """Serializer for offer detail endpoint responses."""

    user = serializers.IntegerField(source='user.id', read_only=True)
    details = OfferDetailLinkSerializer(many=True, read_only=True)

    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
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
        ]

    def get_min_price(self, obj):
        """Return annotated minimum price if available."""
        return getattr(obj, 'min_price', None)

    def get_min_delivery_time(self, obj):
        """Return annotated minimum delivery time if available."""
        return getattr(obj, 'min_delivery_time', None)