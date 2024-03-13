from rest_framework.exceptions import PermissionDenied
from rest_framework import permissions

class UserPermission(permissions.BasePermission):
    """
    Custom permission class for user permissions.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to perform the action.
        """
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to perform the action on the object.
        """
        if not self.has_permission(request, view):
            return False

        if view.action in ['retrieve', 'update', 'partial_update']:
            return obj.created_by.id == request.user.id or request.user.is_staff
        elif view.action == 'destroy':
            return obj.created_by == request.user or request.user.is_staff
        else:
            raise PermissionDenied("Action not allowed")