from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.musician.user == request.user


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.musician.user == request.user


class IsAuthenticatedAndSafe(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (request.method in SAFE_METHODS and
                request.user.is_authenticated()):
            return True
        elif (request.method == 'DELETE' and
                obj.musician.user == request.user):
            return True
        return False
