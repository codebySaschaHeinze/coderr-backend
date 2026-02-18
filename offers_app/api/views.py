from rest_framework import generics, permissions

from offers_app.models import Offer
from .serializers import OfferCreateSerializer, OfferListSerializer
from .permissions import IsBusinessUser


class OfferListCreateView(generics.ListCreateAPIView):

    queryset = Offer.objects.all()
    

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsBusinessUser()]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context