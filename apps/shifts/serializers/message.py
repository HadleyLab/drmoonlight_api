from rest_framework import serializers

from apps.shifts.models import Message


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('pk', 'date_created', 'owner', 'application', 'message', )
        read_only_fields = ('owner', 'application', )
