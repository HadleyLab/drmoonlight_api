from rest_framework import serializers

from apps.main.utils import get_avatar_thumbnail
from apps.main.validators import validate_file_size
from apps.shifts.models import Message


class MessageSerializer(serializers.ModelSerializer):

    owner_avatar = serializers.SerializerMethodField()
    attachment = serializers.FileField(
        validators=[validate_file_size],
        required=False)
    thumbnail = serializers.ImageField(read_only=True)

    def get_owner_avatar(self, obj):
        return get_avatar_thumbnail(obj.owner.avatar, self.context['request'])

    class Meta:
        model = Message
        fields = ('pk', 'date_created', 'owner', 'owner_avatar',
                  'application', 'text', 'attachment', 'thumbnail')
        read_only_fields = ('owner', 'application', )
