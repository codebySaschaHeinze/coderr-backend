from django.db.models import Min
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics, permissions

from offers_app.models import Offer
from .filters import OfferFilter
from .pagination import OfferPagination
from .permissions import IsBusinessUser
from .serializers import OfferCreateSerializer, OfferListSerializer


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