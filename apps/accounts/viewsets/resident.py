from djoser import email
from djoser.compat import get_user_email
from rest_framework import viewsets, mixins

from apps.accounts.models import Resident
from apps.accounts.permissions import ResidentPermission
from apps.accounts.serializers import (
    ResidentCreateSerializer, ResidentListSerializer)
from apps.main.viewsets import add_transition_actions


@add_transition_actions
class ResidentViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ResidentListSerializer
    queryset = Resident.objects.all()
    permission_classes = [ResidentPermission, ]

    def get_serializer_class(self):
        if self.action == 'create':
            return ResidentCreateSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        context = {'user': user}
        to = [get_user_email(user)]
        email.ActivationEmail(self.request, context).send(to)
