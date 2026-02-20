from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCustomerUser(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.type == 'customer'
        )
    

class IsReviewOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user
            and request.user.is_authenticated
            and obj.reviewer_id == request.user.id
        )
    
