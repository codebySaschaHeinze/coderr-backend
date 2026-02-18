from rest_framework import generics, permissions

from profile_app.models import Profile
from .serializers import BusinessProfileListSerializer, CustomerProfileListSerializer, ProfileSerializer


class ProfileDetailView(generics.RetrieveUpdateAPIView):

    queryset = Profile.objects.select_related('user')
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class BusinessProfilesListView(generics.ListAPIView):

    
    serializer_class = BusinessProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.select_related("user").filter(user__type="business")
    

class CustomerProfilesListView(generics.ListAPIView):


    serializer_class = CustomerProfileListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.select_related("user").filter(user__type="customer")