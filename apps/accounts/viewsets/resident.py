from djoser import email
from djoser.compat import get_user_email
from rest_framework import viewsets, mixins
from rest_framework.decorators import list_route
from rest_framework.response import Response

from apps.accounts.models import Resident, ResidentStateEnum
from apps.accounts.permissions import ResidentPermission, IsAccountManager
from apps.accounts.serializers import (
    ResidentCreateSerializer, ResidentUpdateSerializer,
    ResidentFillProfileSerializer, ResidentSerializer)
from apps.main.viewsets import add_transition_actions


@add_transition_actions(serializers={
    'fill_profile': ResidentFillProfileSerializer})
class ResidentViewSet(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = ResidentSerializer
    queryset = Resident.objects.all()
    permission_classes = [ResidentPermission, ]

    def get_serializer_class(self):
        if self.action == 'create':
            return ResidentCreateSerializer

        if self.action in ['update', 'partial_update']:
            return ResidentUpdateSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        user = serializer.save()

        context = {'user': user}
        to = [get_user_email(user)]
        email.ActivationEmail(self.request, context).send(to)

    @list_route(permission_classes=(IsAccountManager, ))
    def waiting_for_approval(self, request):
        qs = Resident.objects.filter(state=ResidentStateEnum.PROFILE_FILLED)
        serializer = self.get_serializer(qs, many=True)

        return Response(serializer.data)
