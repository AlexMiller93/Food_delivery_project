from rest_framework import permissions


class StaffOrReadOnly(permissions.BasePermission):
    """
    Check if user is staff worker / manager
    """
    def has_staff_permission(self, request, view):
        if request.account.user_type in ('Manager', 'Courier', 'Cook'):
            return True
        return False


class ManagerOrReadOnly(permissions.BasePermission):
    """
    Check if user is manager
    """
    def has_staff_permission(self, request, view):
        if request.account.user_type == 'Manager':
            return True
        return False