from rest_framework.permissions import BasePermission, SAFE_METHODS


class ResidentPermission(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        if not user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return user.is_account_manager or \
                   user == obj.user_ptr

        if request.method in ['PUT', 'PATCH']:
            return user == obj.user_ptr

        return False  # pragma: no cover
