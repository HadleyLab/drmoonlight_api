from django.db import transaction
from rest_framework import viewsets, pagination, mixins
from rest_framework.generics import get_object_or_404

from apps.shifts.models import Message, Application
from apps.shifts.permissions import MessagePermission
from apps.shifts.serializers import MessageSerializer
from apps.shifts.services.message import process_message_creation


class MessageViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (MessagePermission, )
    pagination_class = pagination.LimitOffsetPagination

    def initial(self, request, *args, **kwargs):
        super(MessageViewSet, self).initial(request, *args, **kwargs)

        # Check that application is accessible by user and store it
        self.application = self.get_application()

    def get_application(self):
        application_pk = self.kwargs['application_pk']

        return get_object_or_404(
            Application.objects.filter_for_user(self.request.user),
            pk=application_pk)

    def get_queryset(self):
        qs = super(MessageViewSet, self).get_queryset()

        qs = qs.filter(application=self.application).order_by('-date_created')

        return qs

    @transaction.atomic
    def perform_create(self, serializer):
        instance = serializer.save(
            application=self.application, owner=self.request.user)
        process_message_creation(instance)
