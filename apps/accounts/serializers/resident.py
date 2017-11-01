from rest_framework import serializers

from apps.accounts.models import Resident
from .user import UserCreateSerializer


class ResidentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        fields = ('pk', 'email', )


class ResidentCreateSerializer(UserCreateSerializer):
    class Meta:
        model = Resident
        fields = ('pk', 'email', 'first_name', 'last_name', 'password', )

