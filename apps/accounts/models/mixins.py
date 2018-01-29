from rest_framework import serializers

from apps.main.utils import get_avatar_thumbnail


class AvatarFieldMixin(serializers.ModelSerializer):
    def get_avatar(self, obj):
        return get_avatar_thumbnail(obj.avatar, self.context['request'])

    def update(self, instance, validated_data):
        result = super(AvatarFieldMixin, self).update(instance, validated_data)
        self.fields['avatar'] = serializers.SerializerMethodField()
        return result
