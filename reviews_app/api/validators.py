from rest_framework import serializers
from rest_framework.exceptions import NotAuthenticated, PermissionDenied


def validate_customer_can_create_review(user) -> None:
    if getattr(user, 'type', None) != 'customer':
        raise NotAuthenticated()


def validate_business_user_is_business(business_user) -> None:
    if not business_user or getattr(business_user, 'type', None) != 'business':
        raise serializers.ValidationError({'business_user': 'Muss ein Verkäufer sein.'})


def validate_no_duplicate_review(exists: bool) -> None:
    if exists:
        raise PermissionDenied()


def validate_only_allowed_patch_fields(request_data: dict, allowed_fields: set) -> None:
    unknown_fields = set(request_data.keys()) - allowed_fields
    if unknown_fields:
        raise serializers.ValidationError(
            {
                'detail': 'Unzulässige Felder.',
                'fields': sorted(unknown_fields),
            }
        )