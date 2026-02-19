from django.urls import path

from .views import OfferListCreateView, OfferDetailView, OfferDetailItemView


urlpatterns = [
    path('offers/', OfferListCreateView.as_view(), name='offers'),
    path('offers/<int:id>/', OfferDetailView.as_view(), name='offer-detail'),
    path('offerdetails/<int:id>/', OfferDetailItemView.as_view(), name='offer-detail-item'),
]