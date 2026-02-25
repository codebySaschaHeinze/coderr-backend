from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from profile_app.models import Profile
from .serializers import LoginSerializer, RegistrationSerializer


class RegistrationView(APIView):
    """Handle user registration and return an auth token."""

    permission_classes = []

    def post(self, request):
        """Create a user, create a profile, and return token data."""
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        Profile.objects.create(user=user)
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.id,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """Handle user login and return an auth token."""

    permission_classes = []

    def post(self, request):
        """Validate credentials and return token data."""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.id,
            },
            status=status.HTTP_200_OK,
        )