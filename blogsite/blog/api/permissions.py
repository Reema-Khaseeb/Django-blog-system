"""Object level custom permissions"""
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Check whether the requesting user is the owner of the given object

    Args:
        permissions

    Returns:
        bool: whether the requesting user is the owner of the given object
    """
    def has_object_permission(self, request, view, obj):
        """Override has_object_permission() method to check whether the given 
        HTTP method is included in (SAFE_METHODS) tuple then return authorization check
        
        Returns:
            bool: Whether the requesting user is the owner of the given object
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
