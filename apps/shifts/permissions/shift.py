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
            return request.user == obj.owner.user_ptr

        return True
