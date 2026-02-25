from django.contrib.auth import authenticate
from rest_framework import serializers


def validate_passwords_match(password: str, repeated_password: str) -> None:
    """Raise ValidationError if password and repeated_password differ."""
    if password != repeated_password:
        raise serializers.ValidationError(
            {'repeated_password': 'Passwörter stimmen nicht überein.'}
        )


def validate_login(username: str, password: str):
    """Authenticate a user and return it, or raise ValidationError."""
    user = authenticate(username=username, password=password)
    if not user:
        raise serializers.ValidationError('Ungültige Anmeldeinformationen.')
    if not user.is_active:
        raise serializers.ValidationError('Benutzer ist nicht aktiv.')
    return user