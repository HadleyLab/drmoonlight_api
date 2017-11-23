from rest_framework import serializers

from apps.accounts.models import Resident
from apps.shifts.models import Shift, Application


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = (
            'pk', 'owner', 'date_end', 'date_start', 'speciality',
            'residency_program', 'residency_years_required',
            'payment_amount', 'payment_per_hour', 'description', )

        read_only_fields = ('owner', )
