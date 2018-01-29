from rest_framework import serializers

from apps.main.utils import get_avatar_thumbnail
from apps.shifts.models import Message


class MessageSerializer(serializers.ModelSerializer):

    owner_avatar = serializers.SerializerMethodField()

    def get_owner_avatar(self, obj):
        return get_avatar_thumbnail(obj.owner.avatar, self.context['request'])

    class Meta:
        model = Message
        fields = ('pk', 'date_created', 'owner', 'owner_avatar',
                  'application', 'text', )
        read_only_fields = ('owner', 'application', )
