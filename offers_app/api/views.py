from django.db.models import Min
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions

from offers_app.models import Offer, OfferDetail
from .filters import OfferFilter
from .pagination import OfferPagination
from .permissions import IsBusinessUser, IsOfferOwner
from .serializers import (
    OfferCreateSerializer,
    OfferDetailSerializer,
    OfferDetailViewSerializer,
    OfferListSerializer,
    OfferUpdateSerializer,
)


class OfferListCreateView(generics.ListCreateAPIView):
    """List offers publicly and allow business users to create offers."""

    pagination_class = OfferPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['-updated_at']

    def get_queryset(self):
        """Return offers with related data and aggregated min values."""
        return (
            Offer.objects.select_related('user')
            .prefetch_related('details', 'user__profile')
            .annotate(
                min_price=Min('details__price'),
                min_delivery_time=Min('details__delivery_time_in_days'),
            )
        )

    def get_permissions(self):
        """Allow public reads and restrict creates to authenticated business users."""
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsBusinessUser()]

    def get_serializer_class(self):
        """Use list serializer for GET and create serializer for POST."""
        if self.request.method == 'GET':
            return OfferListSerializer
        return OfferCreateSerializer

    def get_serializer_context(self):
        """Add request to serializer context for absolute URL generation."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a single offer."""

    lookup_url_kwarg = 'id'

    def get_queryset(self):
        """Return offers with aggregated detail values for detail responses."""
        return (
            Offer.objects.select_related('user')
            .prefetch_related('details')
            .annotate(
                min_price=Min('details__price'),
                min_delivery_time=Min('details__delivery_time_in_days'),
            )
        )

    def get_permissions(self):
        """Require auth for reads and ownership for write/delete actions."""
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsOfferOwner()]

    def get_serializer_class(self):
        """Use detail serializer for GET and update serializer otherwise."""
        if self.request.method == 'GET':
            return OfferDetailViewSerializer
        return OfferUpdateSerializer


class OfferDetailItemView(generics.RetrieveAPIView):
    """Retrieve a single offer detail item."""

    lookup_url_kwarg = 'id'
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.IsAuthenticated]