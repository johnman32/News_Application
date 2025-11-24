from rest_framework import permissions


class IsJournalist(permissions.BasePermission):
    """
    Permission  to allow only journalist for certain views
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role == "journalist"


class IsEditor(permissions.BasePermission):
    """
    Permission to allow only editor for certain views
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role == "editor"
