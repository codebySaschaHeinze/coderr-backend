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
    queryset = Profile.objects.select_related('user')
    serializer_class = ProfileDetailSerializer
    permission_classes = [IsProfileOwnerOrReadOnly]

    def get_object(self):
        profile = get_object_or_404(self.queryset, user_id=self.kwargs['pk'])
        self.check_object_permissions(self.request, profile)
        return profile


class BusinessProfilesListView(generics.ListAPIView):


    serializer_class = BusinessProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.select_related('user').filter(user__type='business')
    

class CustomerProfilesListView(generics.ListAPIView):


    serializer_class = CustomerProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.select_related('user').filter(user__type='customer')