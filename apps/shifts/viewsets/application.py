from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, pagination, status, response
from rest_framework.decorators import list_route

from apps.main.viewsets import add_transition_actions

from apps.shifts.models import Application
from apps.shifts.permissions import (
    ApplicationPermission, ApplicationApplyPermission,
    ApplicationInvitePermission)
from apps.shifts.serializers import (
    ApplicationSerializer, ApplicationCreateSerializer,
    InvitationCreateSerializer)
from apps.shifts.services.application import (
    process_application, process_invitation)


@add_transition_actions
class ApplicationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = (ApplicationPermission, )
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('state', )

    def get_queryset(self):
        qs = super(ApplicationViewSet, self).get_queryset()

        # TODO: set up ordering. Without messages should be first
        qs = qs.order_by('-date_created')

        user = self.request.user

        if user.is_scheduler:
            return qs.filter(shift__owner=user.scheduler)

        if user.is_resident:
            return qs.filter(owner=user.resident)

        return qs

    @list_route(
        methods=['POST'],
        serializer_class=ApplicationCreateSerializer,
        permission_classes=(ApplicationApplyPermission, )
    )
    def apply(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_apply(serializer)

        return response.Response(
            data=serializer.data, status=status.HTTP_201_CREATED)

    def perform_apply(self, serializer):
        user = self.request.user

        instance = serializer.save(owner=user.resident)
        process_application(instance)

        return instance

    @list_route(
        methods=['POST'],
        serializer_class=InvitationCreateSerializer,
        permission_classes=(ApplicationInvitePermission, )
    )
    def invite(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_invite(serializer)

        return response.Response(
            data=serializer.data, status=status.HTTP_201_CREATED)

    def perform_invite(self, serializer):
        instance = serializer.save()
        process_invitation(instance)

        return instance
