from django.db.models import Min

from rest_framework import serializers

from offers_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):

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

    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        path = f'/api/offerdetails/{obj.id}/'
        return request.build_absolute_uri(path) if request else path
    

class OfferListSerializer(serializers.ModelSerializer):

    user = serializers.IntegerField(source='user.id', read_only=True)
    details = OfferDetailLinkSerializer(many=True, read_only=True)

    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_detail = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
            "user_details",
        ]

        def get_min_price(self, obj):
            return obj.details.aggregate(v=Min("price"))["v"]
            

        def get_min_delivery_timer(self, obj):
            return obj.details.aggregate(v=Min('delivery_time_in_days'))['v']
        
        def get_user_details(self, obj):
            profile = getattr(obj.user, 'profile', None)
            return {
                'first_name': getattr(profile, 'first_name', '') or '',
                'last_name': getattr(profile, 'last_name', '') or '',
                'username': obj.user.username,
            }
        


class OfferCreateSerializer(serializers.ModelSerializer):

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
        if len(details) != 3:
            raise serializers.ValidationError('Ein Angebot muss genau 3 Details enthalten.')
        return details
    
    def create(self, validated_data):
        details_data = validated_data.pop('details')
        request = self.context.get('request')
        offer = Offer.objects.create(user=request.user, **validated_data)

        OfferDetail.objects.bulk_create(
            [OfferDetail(offer=offer, **details) for details in details_data]
        )

        return offer
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['details'] = OfferDetailSerializer(instance.details.all(), many=True).data
        return data