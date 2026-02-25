from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework import serializers

from offers_app.models import OfferDetail


def validate_customer_can_create(user) -> None:
    if getattr(user, 'type', None) != 'customer':
        raise PermissionDenied('Nur Käufer dürfen Bestellungen erstellen.')


def get_offer_detail_or_404(detail_id: int) -> OfferDetail:
    return get_object_or_404(
        OfferDetail.objects.select_related('offer', 'offer__user'),
        id=detail_id,
    )


def validate_order_status(status_value: str) -> str:
    if status_value is None:
        raise serializers.ValidationError({'status': 'Dieses Feld ist erforderlich.'})

    allowed = {'in_progress', 'completed', 'cancelled'}
    if status_value not in allowed:
        raise serializers.ValidationError({'status': 'Ungültiger Status.'})

    return status_value