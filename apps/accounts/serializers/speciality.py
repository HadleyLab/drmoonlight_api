from rest_framework import serializers

from apps.accounts.models import Speciality


class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = ('pk', 'name', )
