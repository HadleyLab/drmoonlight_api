from rest_framework.permissions import BasePermission


class ResidentPermission(BasePermission):
    def has_permission(self, request, view):
        # Resident can be created by unauthenticated user
        if request.method == 'POST':
            return True

        return False
