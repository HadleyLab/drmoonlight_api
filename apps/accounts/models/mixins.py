from rest_framework import serializers
from sorl.thumbnail import get_thumbnail


class AvatarFieldMixin(serializers.Serializer):
    def get_avatar(self, obj):
        if obj.avatar:
            return self.context['request'].build_absolute_uri(
                get_thumbnail(obj.avatar, '100x100',
                              crop='center', quality=90).url)

