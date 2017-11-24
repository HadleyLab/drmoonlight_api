from rest_framework import serializers

from apps.accounts.serializers import SchedulerSerializer
from apps.shifts.models import Shift


class ShiftSerializer(serializers.ModelSerializer):
    owner = SchedulerSerializer(read_only=True)

    class Meta:
        model = Shift
        fields = (
            'pk', 'owner', 'date_created', 'date_modified', 'date_end',
            'date_start', 'speciality', 'residency_program',
            'residency_years_required', 'payment_amount', 'payment_per_hour',
            'description', )
