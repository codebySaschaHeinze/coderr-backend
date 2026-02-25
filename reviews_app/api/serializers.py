from rest_framework import serializers

from reviews_app.models import Review
from .validators import validate_business_user_is_business


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
        """Validate that the target user is a business user."""
        validate_business_user_is_business(attrs.get('business_user'))
        return attrs

    def create(self, validated_data):
        """Create a review and set the authenticated user as reviewer."""
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