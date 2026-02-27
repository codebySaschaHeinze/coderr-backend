from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from orders_app.models import Order
from .permissions import IsBusinessUser, IsStaffUser
from .serializers import OrderCreateSerializer, OrderSerializer
from .validators import (
    get_offer_detail_or_404,
    validate_customer_can_create,
    validate_order_status,
)


User = get_user_model()


class OrdersView(generics.ListCreateAPIView):
    """List user-related orders and allow customers to create new orders."""

    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return orders where the authenticated user is customer or business."""
        user = self.request.user
        return Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        ).order_by('-created_at')

    def get_serializer_class(self):
        """Use create serializer for POST and read serializer otherwise."""
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        """Create an order from an offer detail for an authenticated customer."""
        validate_customer_can_create(request.user)

        serializer = OrderCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        detail_id = serializer.validated_data['offer_detail_id']
        detail = get_offer_detail_or_404(detail_id)

        order = Order.objects.create(
            customer_user=request.user,
            business_user=detail.offer.user,
            title=detail.title,
            revisions=detail.revisions,
            delivery_time_in_days=detail.delivery_time_in_days,
            price=detail.price,
            features=detail.features,
            offer_type=detail.offer_type,
            status='in_progress',
        )

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update status (PATCH), or delete (DELETE) a single order."""
    
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def get_permissions(self):
        """Apply method-specific permissions for PATCH and DELETE actions."""
        if self.request.method == "PATCH":
            return [permissions.IsAuthenticated(), IsBusinessUser()]

        if self.request.method == "DELETE":
            return [permissions.IsAuthenticated(), IsStaffUser()]

        return [permissions.IsAuthenticated()]

    def patch(self, request, *args, **kwargs):
        """Only the owning business user is allowed to update the status."""
        order = self.get_object() 

        if request.user != order.business_user:
            raise PermissionDenied("You do not have permission to update this order.")

        status_value = validate_order_status(request.data.get("status"))
        order.status = status_value
        order.save(update_fields=["status", "updated_at"])

        return Response(self.get_serializer(order).data, status=status.HTTP_200_OK)


class OrderCountView(APIView):
    """Return the count of in-progress orders for a business user."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, business_user_id):
        """Return the number of in-progress orders for the given business user."""
        business_user = get_object_or_404(User, id=business_user_id, type='business')
        count = Order.objects.filter(
            business_user=business_user,
            status='in_progress',
        ).count()
        return Response({'order_count': count}, status=status.HTTP_200_OK)


class CompletedOrderCountView(APIView):
    """Return the count of completed orders for a business user."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, business_user_id):
        """Return the number of completed orders for the given business user."""
        business_user = get_object_or_404(User, id=business_user_id, type='business')
        count = Order.objects.filter(
            business_user=business_user,
            status='completed',
        ).count()
        return Response({'completed_order_count': count}, status=status.HTTP_200_OK)