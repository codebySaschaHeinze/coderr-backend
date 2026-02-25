from rest_framework.permissions import BasePermission


class IsCustomerUser(BasePermission):
    """Allow access only to authenticated customer users."""

    def has_permission(self, request, view):
        """Return True if the authenticated user is a customer user."""
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.type == 'customer'
        )


class IsReviewOwner(BasePermission):
    """Allow access only to the owner of the review object."""

    def has_object_permission(self, request, view, obj):
        """Return True if the authenticated user owns the review."""
        return bool(
            request.user
            and request.user.is_authenticated
            and obj.reviewer_id == request.user.id
        )