from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.accounts.serializers import ResidentSerializer
from apps.shifts.models import Application, Shift, ShiftStateEnum
from .shift import ShiftSerializer


class ApplicationSerializer(serializers.ModelSerializer):
    owner = ResidentSerializer()
    shift = ShiftSerializer()

    class Meta:
        model = Application
        fields = ('pk', 'date_created', 'owner', 'shift', 'state', )


class BaseApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('pk', 'shift', )

    def validate_shift(self, shift):
        if shift.is_started:
            raise ValidationError(
                'You can not create an application for a started shift')

        if shift.state == ShiftStateEnum.COVERAGE_COMPLETED:
            raise ValidationError(
                'You can not create an application for coverage '
                'completed shift')

        return shift


class ApplicationCreateSerializer(BaseApplicationCreateSerializer):
    class Meta:
        model = Application
        fields = ('pk', 'shift', )

    def validate_shift(self, shift):
        shift = super(ApplicationCreateSerializer, self).validate_shift(shift)
        user = self.context['request'].user

        assert user.is_resident, \
            'ApplicationCreateSerializer only for a resident'

        suitable_shifts = Shift.objects.filter_for_resident(user.resident)

        if not suitable_shifts.filter(pk=shift.pk).exists():
            raise ValidationError(
                'You can not create an application for not suitable shift')

        return shift


class InvitationCreateSerializer(BaseApplicationCreateSerializer):
    class Meta:
        model = Application
        fields = ('pk', 'owner', 'shift', )

    def validate_shift(self, shift):
        shift = super(InvitationCreateSerializer, self).validate_shift(shift)
        user = self.context['request'].user

        assert user.is_scheduler, \
            'InvitationCreateSerializer only for a scheduler'

        # TODO:  can the scheduler invite an unsuitable resident?
        if shift.owner != user.scheduler:
            raise ValidationError(
                'You can not create an application for not own shift')

        return shift

    def validate_owner(self, owner):
        if not owner.resident.is_approved:
            raise ValidationError(
                'You can not create an application for a not approved resident')
        return owner
