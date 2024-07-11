from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPostAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and (
            request.user.is_superuser
            or request.method in SAFE_METHODS
            or obj.author == request.user
        ):
            return True
        return False
