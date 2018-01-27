from django.utils import timezone
from rest_framework import serializers

from apps.accounts.serializers import SchedulerSerializer
from apps.shifts.models import Shift, ApplicationStateEnum


class ShiftSerializer(serializers.ModelSerializer):
    owner = SchedulerSerializer(read_only=True)
    has_already_applied = serializers.SerializerMethodField()
    was_rejected = serializers.SerializerMethodField()

    class Meta:
        model = Shift
        fields = (
            'pk', 'owner', 'date_created', 'date_modified', 'date_end',
            'date_start', 'speciality',
            'residency_years_required', 'payment_amount', 'payment_per_hour',
            'description', 'state', 'has_already_applied', 'was_rejected', )

    def get_has_already_applied(self, obj):
        request = self.context['request']

        user = request.user

        if user.is_resident:
            # `applications.all()` are already prefetched
            applicants_pks = [
                application.owner_id
                for application in obj.applications.all()]
            return user.pk in applicants_pks

        return None

    def get_was_rejected(self, obj):
        request = self.context['request']

        user = request.user

        if user.is_resident:
            # `applications.all()` are already prefetched
            applications = [
                application
                for application in obj.applications.all()
                if application.owner_id == user.pk]
            if len(applications) > 0:
                return applications[0].state == ApplicationStateEnum.REJECTED

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
