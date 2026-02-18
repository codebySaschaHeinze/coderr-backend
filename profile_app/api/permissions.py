from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsProfileOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return obj.user_id == request.user.id