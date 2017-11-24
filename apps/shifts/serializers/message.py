from rest_framework import serializers

from apps.shifts.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('pk', 'date_created', 'owner', 'application', 'message', )


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('pk', 'message', )
