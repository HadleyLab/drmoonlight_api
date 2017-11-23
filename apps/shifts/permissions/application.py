from rest_framework.permissions import BasePermission, SAFE_METHODS


class ApplicationPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        return user.is_scheduler or \
               (user.is_resident and user.resident.is_approved)


class ApplicationApplyPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        return user.is_resident and user.resident.is_approved


class ApplicationInvitePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        return user.is_scheduler
