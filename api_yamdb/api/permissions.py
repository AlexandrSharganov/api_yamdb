from rest_framework import permissions


class IsModerOrAdminOrSuperOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or (request.user.is_authenticated
                and (request.user.is_administrator()
                     or request.user.is_moderator())
                )
        )


class IsAdminOrSuperOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return(
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and (request.user.is_administrator())
            )
        )


class IsAdminOrSuper(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.is_administrator()
            )
        )


class IsAllowedToSignUp(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
        )
