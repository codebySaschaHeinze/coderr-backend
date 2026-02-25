from rest_framework.permissions import BasePermission


class IsBusinessUser(BasePermission):
    """Allow access only to authenticated business users."""

    def has_permission(self, request, view):
        """Return True if the authenticated user is a business user."""
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.type == 'business'
        )


class IsOfferOwner(BasePermission):
    """Allow access only to the owner of the offer object."""

    def has_object_permission(self, request, view, obj):
        """Return True if the authenticated user owns the object."""
        return bool(
            request.user
            and request.user.is_authenticated
            and obj.user_id == request.user.id
        )