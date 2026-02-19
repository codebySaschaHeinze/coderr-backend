from rest_framework.permissions import BasePermission


class IsBusinessUser(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user 
            and request.user.is_authenticated 
            and request.user.type == 'business')
    

class IsOfferOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user and
            request.user.is_authenticated and
            obj.user_id == request.user.id)