from djoser import email
from djoser.compat import get_user_email
from rest_framework import viewsets, mixins

from apps.accounts.models import Scheduler
from apps.accounts.permissions import SchedulerPermission
from apps.accounts.serializers import (
    SchedulerCreateSerializer, SchedulerUpdateSerializer, SchedulerSerializer)


class SchedulerViewSet(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = SchedulerSerializer
    queryset = Scheduler.objects.all()
    permission_classes = [SchedulerPermission, ]

    def get_serializer_class(self):
        if self.action == 'create':
            return SchedulerCreateSerializer

        if self.action in ['update', 'partial_update']:
            return SchedulerUpdateSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        user = serializer.save()

        context = {'user': user}
        to = [get_user_email(user)]
        email.ActivationEmail(self.request, context).send(to)
