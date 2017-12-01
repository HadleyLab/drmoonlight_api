from rest_framework import serializers

from apps.accounts.models import ResidencyProgram


class ResidencyProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidencyProgram
        fields = ('pk', 'name', )
