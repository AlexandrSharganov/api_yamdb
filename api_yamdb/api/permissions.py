from rest_framework import permissions


class IsModerOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or (request.user.is_authenticated
                and (request.user.is_administrator()
                     or request.user.is_moderator())
                )
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return(
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_administrator()
            )
        )


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.is_administrator()
            )
        )
