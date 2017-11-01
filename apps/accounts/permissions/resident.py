from rest_framework.permissions import BasePermission


class ResidentPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return True

        if view.action == 'me':
            return request.user.is_resident

        # These actions are handled in has_object_permission
        if view.action in ['retrieve', 'partial_update', 'update']:
            return True

        return False  # pragma: no cover

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return request.user.is_account_manager

        if view.action in ['partial_update', 'update']:
            return request.user == obj.user_ptr

        return False  # pragma: no cover
