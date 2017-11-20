from rest_framework.permissions import BasePermission, SAFE_METHODS


class SchedulerPermission(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user.is_account_manager or \
                   request.user == obj.user_ptr

        if request.method in ['PUT', 'PATCH']:
            return request.user == obj.user_ptr

        return False  # pragma: no cover
