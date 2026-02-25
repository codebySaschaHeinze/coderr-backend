from rest_framework import serializers

from profile_app.models import Profile
from .validators import normalize_none_to_empty_str


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for generic profile model access."""

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('user', 'created_at')


class BusinessProfileListSerializer(serializers.ModelSerializer):
    """Serializer for listing business profiles."""

    user = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    type = serializers.CharField(source='user.type', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'user',
            'username',
            'first_name',
            'last_name',
            'file',
            'location',
            'tel',
            'description',
            'working_hours',
            'type',
        ]

    def to_representation(self, instance):
        """Normalize nullable profile fields to empty strings in responses."""
        data = super().to_representation(instance)
        return normalize_none_to_empty_str(
            data,
            ('first_name', 'last_name', 'location', 'tel', 'description', 'working_hours'),
        )


class CustomerProfileListSerializer(serializers.ModelSerializer):
    """Serializer for listing customer profiles."""

    user = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    type = serializers.CharField(source='user.type', read_only=True)

    uploaded_at = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'user',
            'username',
            'first_name',
            'last_name',
            'file',
            'uploaded_at',
            'type',
        ]

    def to_representation(self, instance):
        """Normalize nullable profile fields to empty strings in responses."""
        data = super().to_representation(instance)
        return normalize_none_to_empty_str(
            data,
            ('first_name', 'last_name'),
        )


class ProfileDetailSerializer(serializers.ModelSerializer):
    """Serializer for profile detail responses and profile updates."""

    user = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email')
    type = serializers.CharField(source='user.type', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'user',
            'username',
            'email',
            'first_name',
            'last_name',
            'file',
            'location',
            'tel',
            'description',
            'working_hours',
            'type',
            'created_at',
        ]
        read_only_fields = ('user', 'username', 'type', 'created_at')

    def update(self, instance, validated_data):
        """Update profile fields and nested user email if provided."""
        user_data = validated_data.pop('user', {})

        instance = super().update(instance, validated_data)

        if 'email' in user_data:
            instance.user.email = user_data['email']
            instance.user.save(update_fields=['email'])

        return instance