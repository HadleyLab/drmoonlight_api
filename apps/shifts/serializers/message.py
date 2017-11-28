from rest_framework import serializers

from apps.shifts.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('pk', 'date_created', 'owner', 'application', 'text', )
        read_only_fields = ('owner', 'application', )
