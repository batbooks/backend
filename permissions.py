from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    message = 'You are not a user '

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user