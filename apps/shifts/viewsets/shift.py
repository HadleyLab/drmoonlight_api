from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from libs.bulk_create_model_mixin import BulkCreateModelMixin

from apps.accounts.models import ResidentStateEnum
from apps.shifts.filters import ShiftFilter
from apps.shifts.models import Shift
from apps.shifts.permissions import ShiftPermission
from apps.shifts.serializers import ShiftSerializer


class ShiftViewSet(BulkCreateModelMixin, viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_class = ShiftFilter
    permission_classes = (ShiftPermission, )

    def get_queryset(self):
        qs = super(ShiftViewSet, self).get_queryset()

        user = self.request.user
        if user.is_resident:
            resident = user.resident
            if resident.state == ResidentStateEnum.APPROVED:
                # An approved resident can see only suitable shifts for him
                qs = qs.filter(
                    speciality__in=resident.specialities.all(),
                    residency_program=resident.residency_program,
                    residency_years_required__lte=resident.residency_year
                )

        return qs

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user.scheduler)
