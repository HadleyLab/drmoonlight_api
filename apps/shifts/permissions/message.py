from rest_framework.permissions import BasePermission


class  MessagePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        return user.is_scheduler or \
               (user.is_resident and user.resident.is_approved)
