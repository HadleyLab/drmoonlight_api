from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from apps.shifts.permissions import ShiftPermission
from libs.bulk_create_model_mixin import BulkCreateModelMixin

from apps.shifts.filters import ShiftFilter
from apps.shifts.models import Shift
from apps.shifts.serializers import ShiftSerializer
from apps.shifts.services.shift import (
    process_shift_creation, process_shift_deletion, process_shift_updating)


class ShiftViewSet(BulkCreateModelMixin, viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = ShiftFilter
    permission_classes = (ShiftPermission, )

    def get_queryset(self):
        qs = super(ShiftViewSet, self).get_queryset()

        user = self.request.user

        if user.is_scheduler:
            return qs.filter_for_scheduler(user.scheduler)

        if user.is_resident:
            return qs.filter_for_resident(user.resident)

        return qs

    @transaction.atomic
    def perform_create(self, serializer):
        instance = serializer.save(owner=self.request.user.scheduler)
        process_shift_creation(instance)

        return instance

    @transaction.atomic
    def perform_update(self, serializer):
        instance = serializer.save()
        process_shift_updating(instance)

        return instance

    @transaction.atomic
    def perform_destroy(self, instance):
        process_shift_deletion(instance)
        instance.delete()
