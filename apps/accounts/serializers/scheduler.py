from rest_framework import serializers

from apps.accounts.models import Scheduler
from .user import UserCreateSerializer


class SchedulerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheduler
        fields = ('pk', 'email', 'first_name', 'last_name', 'department_name',
            'facility_name', )


class SchedulerCreateSerializer(UserCreateSerializer):
    class Meta:
        model = Scheduler
        fields = ('pk', 'email', 'first_name', 'last_name', 'department_name',
                  'facility_name', 'password', )


class SchedulerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheduler
        fields = (
            'pk', 'email', 'first_name', 'last_name', 'department_name',
            'facility_name',
        )


