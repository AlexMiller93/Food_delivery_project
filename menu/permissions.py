from rest_framework import permissions


class StaffOrReadOnly(permissions.BasePermission):
    """
    Check if user is staff worker / manager
    """
    def has_staff_permission(self, request, view):
        if request.user == 'STAFF':
            return True
        return False
