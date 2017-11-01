from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer


class UserCreateSerializer(BaseUserCreateSerializer):
    def perform_create(self, validated_data):
        UserModel = self.Meta.model

        user = UserModel(is_active=False, **validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user
