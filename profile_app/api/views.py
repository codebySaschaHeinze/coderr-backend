from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions

from profile_app.models import Profile
from .permissions import IsProfileOwnerOrReadOnly
from .serializers import (
    BusinessProfileListSerializer,
    CustomerProfileListSerializer,
    ProfileDetailSerializer,
)


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """Retrieve and update a user profile by user ID."""

    queryset = Profile.objects.select_related('user')
    serializer_class = ProfileDetailSerializer
    permission_classes = [IsProfileOwnerOrReadOnly]

    def get_object(self):
        """Fetch profile by user ID and enforce object-level permissions."""
        profile = get_object_or_404(self.queryset, user_id=self.kwargs['pk'])
        self.check_object_permissions(self.request, profile)
        return profile


class BusinessProfilesListView(generics.ListAPIView):
    """List all business user profiles."""

    serializer_class = BusinessProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return profiles belonging to business users."""
        return Profile.objects.select_related('user').filter(user__type='business')


class CustomerProfilesListView(generics.ListAPIView):
    """List all customer user profiles."""

    serializer_class = CustomerProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return profiles belonging to customer users."""
        return Profile.objects.select_related('user').filter(user__type='customer')