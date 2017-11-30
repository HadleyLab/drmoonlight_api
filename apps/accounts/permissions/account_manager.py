from rest_framework.permissions import BasePermission


class IsAccountManager(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        return user.is_account_manager
