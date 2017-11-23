from rest_framework.permissions import BasePermission, SAFE_METHODS


class ShiftPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if request.method == 'POST':
            return user.is_scheduler

        if request.method in SAFE_METHODS:
            return user.is_scheduler or user.is_resident

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            # Only a scheduler can update/delete own not started shifts
            return not obj.is_started and \
                   request.user.is_scheduler and \
                   request.user.scheduler == obj.owner

        return True
