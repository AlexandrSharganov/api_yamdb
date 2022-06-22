from rest_framework import permissions
from reviews.models import User



class IsAuthorOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # return bool(request.method in permissions.SAFE_METHODS or
        #             obj.author == request.user or
        #             request.user.role == User.MODERATOR)
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user == User.MODERATOR)



class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return(
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.role == 'admin'
            )
        )


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.role == 'admin' or request.user.is_superuser
            )
        )
