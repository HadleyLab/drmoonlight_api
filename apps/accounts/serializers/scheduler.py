from rest_framework import serializers

from apps.accounts.models import Scheduler
from apps.accounts.models.mixins import AvatarFieldMixin
from .user import UserCreateSerializer


class SchedulerSerializer(AvatarFieldMixin):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Scheduler
        exclude = ('password', )


class SchedulerCreateSerializer(UserCreateSerializer):
    class Meta:
        model = Scheduler
        fields = ('pk', 'email', 'first_name', 'last_name', 'department_name',
                  'facility_name', 'password', 'timezone', )


class SchedulerUpdateSerializer(AvatarFieldMixin):
    class Meta:
        model = Scheduler
        fields = (
            'pk', 'email', 'first_name', 'last_name', 'avatar',
            'department_name', 'facility_name', 'timezone',
        )
