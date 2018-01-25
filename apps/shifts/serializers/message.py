from rest_framework import serializers

from apps.shifts.models import Message


class MessageSerializer(serializers.ModelSerializer):

    owner_avatar = serializers.ImageField(
        source='owner.avatar',
        read_only=True)

    class Meta:
        model = Message
        fields = ('pk', 'date_created', 'owner', 'owner_avatar',
                  'application', 'text', )
        read_only_fields = ('owner', 'application', )
