from django.urls import path

from .views import (
    OrdersView,
    OrderDetailView,
    OrderCountView,
    CompletedOrderCountView
)

urlpatterns = [
    path('orders/', OrdersView.as_view(), name='order'),
    path('orders/<int:id>/', OrderDetailView.as_view(), name='order-detail'),
    path('order-count/<int:business_user_id>/', OrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:business_user_id>', CompletedOrderCountView.as_view(), name='completed-order-count'),
]