from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews_app.models import Review
from .validators import validate_business_user_is_business


User = get_user_model()


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "file"]


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for review read operations."""

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
    """Serializer for creating reviews."""

    business_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(type='business')
    )
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)

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
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']

    def validate(self, attrs):
        validate_business_user_is_business(attrs.get('business_user'))
        return attrs

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError('Rating must be between 1 and 5.')
        return value

    def create(self, validated_data):
        request = self.context['request']
        return Review.objects.create(reviewer=request.user, **validated_data)


class ReviewUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating review content."""

    class Meta:
        model = Review
        fields = [
            'rating',
            'description',
        ]

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError('Rating must be between 1 and 5.')
        return value
