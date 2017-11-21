from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseUserCreateSerializer)


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ('pk', 'email', 'is_resident', 'is_scheduler',
                  'is_account_manager', )


class UserCreateSerializer(BaseUserCreateSerializer):
    def perform_create(self, validated_data):
        UserModel = self.Meta.model

        user = UserModel(is_active=False, **validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user
