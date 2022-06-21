from rest_framework import permissions
from reviews.models import User


class IsAuthorOrModeratorPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        return bool(request.method in permissions.SAFE_METHODS or
                    obj.author == request.user or
                    request.user.role == User.MODERATOR)
