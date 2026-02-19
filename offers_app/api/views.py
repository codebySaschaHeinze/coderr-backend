from django.db.models import Min
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics, permissions

from offers_app.models import Offer, OfferDetail
from .filters import OfferFilter
from .pagination import OfferPagination
from .permissions import IsBusinessUser, IsOfferOwner
from .serializers import OfferCreateSerializer, OfferDetailSerializer, OfferDetailViewSerializer, OfferListSerializer, OfferUpdateSerializer


class OfferListCreateView(generics.ListCreateAPIView):
    
    pagination_class = OfferPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ["title", "description"]
    ordering_fields = ["updated_at", "min_price"]
    ordering = ["-updated_at"] 

    def get_queryset(self):
        return (
            Offer.objects.select_related("user")
            .prefetch_related("details", "user__profile")
            .annotate(
                min_price=Min("details__price"),
                min_delivery_time=Min("details__delivery_time_in_days"),
            )
        )

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsBusinessUser()]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return OfferListSerializer
        return OfferCreateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
    

class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        return (
            Offer.objects.select_related('user')
            .prefetch_related('details')
            .annotate(
                min_price=Min('details__price'),
                min_delivery_time=Min('details__delivery_time_in_days'),
            )
        )
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsOfferOwner()]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OfferDetailViewSerializer
        return OfferUpdateSerializer
    

class OfferDetailItemView(generics.RetrieveAPIView):
    lookup_url_kwarg = 'id'
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.IsAuthenticated]