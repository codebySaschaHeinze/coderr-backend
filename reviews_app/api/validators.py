from rest_framework import serializers
from rest_framework.exceptions import NotAuthenticated, PermissionDenied


def validate_customer_can_create_review(user) -> None:
    """Validate that only customer users can create reviews."""
    if getattr(user, 'type', None) != 'customer':
        raise NotAuthenticated()


def validate_business_user_is_business(business_user) -> None:
    """Validate that the review target is a business user."""
    if not business_user or getattr(business_user, 'type', None) != 'business':
        raise serializers.ValidationError({'business_user': 'Muss ein Verkäufer sein.'})


def validate_no_duplicate_review(exists: bool):
    if exists:
        raise PermissionDenied("Only one review per business user is allowed.")


def validate_only_allowed_patch_fields(request_data: dict, allowed_fields: set) -> None:
    """Validate that PATCH payload contains only allowed fields."""
    unknown_fields = set(request_data.keys()) - allowed_fields
    if unknown_fields:
        raise serializers.ValidationError(
            {
                'detail': 'Unzulässige Felder.',
                'fields': sorted(unknown_fields),
            }
        )