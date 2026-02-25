from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from .validators import validate_passwords_match, validate_login


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):

    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'repeated_password', 'type')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        validate_passwords_match(attrs.get('password'), attrs.get('repeated_password'))
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('repeated_password')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = validate_login(attrs.get('username'), attrs.get('password'))
        attrs['user'] = user
        return attrs
    

