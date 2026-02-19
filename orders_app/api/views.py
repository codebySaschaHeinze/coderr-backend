from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from orders_app.models import Order
from offers_app.models import OfferDetail
from .permissions import IsBusinessUser, IsCustomerUser, IsStaffUser
from .serializers import OrderCreateSerializer, OrderSerializer


User = get_user_model()


class OrdersView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(Q(customer_user=user) | Q(business_user=user)).order_by('-created_at')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer
    
    def create(self, request, *args, **kwargs):
        if request.user.type != "customer":
            return Response({"detail": "Nur Käufer dürfen Bestellungen erstellen."}, status=status.HTTP_403_FORBIDDEN)

        serializer = OrderCreateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        detail_id = serializer.validated_data["offer_detail_id"]
        detail = get_object_or_404(OfferDetail.objects.select_related("offer", "offer__user"), id=detail_id)
        order = Order.objects.create(
            customer_user=request.user,
            business_user=detail.offer.user,
            title=detail.title,
            revisions=detail.revisions,
            delivery_time_in_days=detail.delivery_time_in_days,
            price=detail.price,
            features=detail.features,
            offer_type=detail.offer_type,
            status="in_progress",
        )

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'id'
    queryset = Order.objects.all()

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [permissions.IsAuthenticated(), IsBusinessUser()]
        
        if self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), IsStaffUser()]
        
        return [permissions.IsAuthenticated()]
    
    def get_serializer_class(self):
        return OrderSerializer
    
    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        status_value = request.data.get('status')
        if status_value is None:
            return Response({'status': 'Dieses Feld ist erforderlich.'}, status=status.HTTP_400_BAD_REQUEST)
        
        allowed = {'in_progress', 'completed', 'cancelled'}
        if status_value not in allowed:
            return Response({'status': 'Ungültiger Status.'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = status_value
        order.save(update_fields=['status', 'updated_at'])
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
    

class OrderCountView(APIView):
    
    permission_classes =[permissions.IsAuthenticated]

    def get(self, request, business_user_id):
        busines_user = get_object_or_404(User, id=business_user_id, type='business')
        count = Order.objects.filter(business_user=busines_user, status='in_progress').count()
        return Response({'order_count': count}, status=status.HTTP_200_OK)
    

class CompletedOrderCountView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, business_user_id):
        business_user = get_object_or_404(User, id=business_user_id, type='business')
        count = Order.objects.filter(business_user=business_user, status=status.HTTP_200_OK)


