from rest_framework import permissions


class IsMusician(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_musician


class IsTrackCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_musician and obj.musician.user == request.user
