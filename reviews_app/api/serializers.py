from rest_framework import serializers

from reviews_app.models import Review


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = [
            'id',
            'business_user',
            'reviewer',
            'rating',
            'description',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'reviewer',
            'created_at',
            'updated_at',
        ]


class ReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = [
            'id',
            'business_user',
            'rating',
            'description',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]

    def validate(self, attrs):
        request = self.context['request']
        business_user = attrs.get('business_user')

        if not business_user or business_user.type != 'business':
            raise serializers.ValidationError({'business_user': 'Muss ein Verkäufer sein.'})
        return attrs
    
    def create(self, validated_data):
        request = self.context['request']
        return Review.objects.create(reviewer=request.user, **validated_data)
    

class ReviewUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = [
            'rating',
            'description',
        ]