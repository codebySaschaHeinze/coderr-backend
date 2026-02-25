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


class IsBusinessUser(BasePermission):
    """Allow access only to authenticated business users."""

    def has_permission(self, request, view):
        """Return True if the authenticated user is a business user."""
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.type == 'business'
        )


class IsStaffUser(BasePermission):
    """Allow access only to authenticated staff users."""

    def has_permission(self, request, view):
        """Return True if the authenticated user is a staff user."""
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )