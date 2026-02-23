from rest_framework import serializers
from profile_app.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('user", "created_at')


class BusinessProfileListSerializer(serializers.ModelSerializer):
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
        data = super().to_representation(instance)
        for key in ('first_name', 'last_name', 'location', 'tel', 'description', 'working_hours'):
            if data.get(key) is None:
                data[key] = ''
        return data
    

class CustomerProfileListSerializer(serializers.ModelSerializer):
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
        data = super().to_representation(instance)
        for key in ('first_name', 'last_name'):
            if data.get(key) is None:
                data[key] = ''
        return data
    

class ProfileDetailSerializer(serializers.ModelSerializer):
    
    user = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email')
    type = serializers.CharField(source="user.type", read_only=True)

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
        user_data = validated_data.pop('user', {})

        instance = super().update(instance, validated_data)

        if 'email' in user_data:
            instance.user.email = user_data['email']
            instance.user.save(update_fields=['email'])

        return instance