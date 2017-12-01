from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.accounts.serializers import (
    ResidentSerializer, CurrentUserResidentDefault)
from apps.main.serializers import FSMAvailableUserTransitionsField
from apps.shifts.models import Application, Shift
from .message import MessageSerializer
from .shift import ShiftSerializer


class ApplicationSerializer(serializers.ModelSerializer):
    owner = ResidentSerializer()
    shift = ShiftSerializer()
    messages_count = serializers.IntegerField()
    last_message = MessageSerializer()
    available_transitions = FSMAvailableUserTransitionsField()

    class Meta:
        model = Application
        fields = ('pk', 'date_created', 'owner', 'shift', 'state',
                  'messages_count', 'last_message', 'available_transitions', )


class BaseApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('pk', 'owner', 'shift', )

    def validate_shift(self, shift):
        if shift.is_started:
            raise ValidationError(
                'You can not create an application for a started shift')

        if shift.is_coverage_completed:
            raise ValidationError(
                'You can not create an application for coverage '
                'completed shift')

        return shift

    def validate(self, attrs):
        shift = attrs['shift']
        owner = attrs['owner']
        existing_applications = Application.objects.filter(
            owner=owner, shift=shift)

        if existing_applications.exists():
            raise ValidationError(
                'There is an already created application for the shift')

        return attrs


class ApplicationCreateSerializer(BaseApplicationCreateSerializer):
    owner = serializers.HiddenField(default=CurrentUserResidentDefault())

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

        # TODO: think about an adding a restriction for inviting
        # TODO: an unsuitable resident
        if shift.owner != user.scheduler:
            raise ValidationError(
                'You can not create an application for not own shift')

        return shift

    def validate_owner(self, owner):
        if not owner.resident.is_approved:
            raise ValidationError(
                'You can not create an application for a not approved resident')
        return owner


class ApplicationTransitionSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    text = serializers.CharField(
        required=False, allow_blank=True, allow_null=True)

    class Meta:
        fields = ('user', 'text', )
