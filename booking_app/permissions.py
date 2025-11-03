from rest_framework import permissions


class CheckStatus(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_role == 'owner'


class ReviewPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_role == 'client'


class CheckOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'owner'):
            return request.user == obj.owner
        if hasattr(obj, 'user'):
            return request.user == obj.user
        return False
