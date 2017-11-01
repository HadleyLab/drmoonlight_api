from rest_framework.permissions import BasePermission


class ResidentPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return request.user.is_account_manager

        if view.action in ['partial_update', 'update']:
            return request.user == obj.user

        if view.action == 'me':
            return request.user == obj.user

        return False
