from django.utils import timezone
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
            'description', 'state', )

    def validate(self, attrs):
        attrs = super(ShiftSerializer, self).validate(attrs)

        date_start = attrs['date_start']
        date_end = attrs['date_end']

        if date_start <= timezone.now():
            raise serializers.ValidationError({
                'date_start': [
                    'The starting date must occur after the current date'
                ],
            })

        if date_end <= date_start:
            raise serializers.ValidationError({
                'date_end': [
                    'The ending date must occur after the starting date'
                ],
            })

        return attrs
