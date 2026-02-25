from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsProfileOwnerOrReadOnly(BasePermission):
    """Allow authenticated read access and owner-only write access."""

    def has_object_permission(self, request, view, obj):
        """Allow safe methods for authenticated users, writes only for owner."""
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return obj.user_id == request.user.id