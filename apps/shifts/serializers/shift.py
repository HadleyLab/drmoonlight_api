from django.utils import timezone
from rest_framework import serializers

from apps.accounts.serializers import SchedulerSerializer
from apps.shifts.models import Shift


class ShiftSerializer(serializers.ModelSerializer):
    owner = SchedulerSerializer(read_only=True)
    has_already_applied = serializers.SerializerMethodField()

    class Meta:
        model = Shift
        fields = (
            'pk', 'owner', 'date_created', 'date_modified', 'date_end',
            'date_start', 'speciality', 'residency_program',
            'residency_years_required', 'payment_amount', 'payment_per_hour',
            'description', 'state', 'has_already_applied', )

    def get_has_already_applied(self, obj):
        request = self.context['request']

        user = request.user

        if user.is_resident:
            # `applications.all()` are already prefetched
            applicants_pks = [
                application.owner.pk
                for application in obj.applications.all()]
            return user.pk in applicants_pks

        return None

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
