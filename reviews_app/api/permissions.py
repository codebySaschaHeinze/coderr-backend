from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

from reviews_app.models import Review


class IsCustomerUser(BasePermission):
    """Allow access only to authenticated customer users."""

    def has_permission(self, request, view):
        """Return True if the authenticated user is a customer user."""
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.type == 'customer'
        )


class CanCreateReview(BasePermission):
    """Permission for creating reviews."""

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if getattr(user, 'type', None) != 'customer':
            raise PermissionDenied('Only customers can create reviews.')

        business_user_id = request.data.get('business_user')
        if business_user_id and Review.objects.filter(
            business_user_id=business_user_id,
            reviewer=user,
        ).exists():
            raise PermissionDenied('Only one review per business user is allowed.')

        return True


class IsReviewOwner(BasePermission):
    """Allow access only to the owner of the review object."""

    def has_object_permission(self, request, view, obj):
        """Return True if the authenticated user owns the review."""
        return bool(
            request.user
            and request.user.is_authenticated
            and obj.reviewer_id == request.user.id
        )