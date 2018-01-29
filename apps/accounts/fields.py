import re
from rest_framework import serializers


class MultipartM2MField(serializers.Field):
    def to_representation(self, obj):
        return obj.values_list('id', flat=True).order_by('id')

    def to_internal_value(self, data):
        data = data[1:-1]
        return data.split(',') if data else []


class MultipartArrayField(serializers.Field):
    def to_representation(self, obj):
        return obj

    def to_internal_value(self, data):
        return re.findall('"(\w{2})"', data)
