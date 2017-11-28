from channels.generic.websockets import JsonWebsocketConsumer
from rest_framework.authtoken.models import Token


class UserConsumer(JsonWebsocketConsumer):
    def get_user(self, key):
        token = Token.objects.filter(key=key).first()

        if token:
            return token.user

        return None

    def connection_groups(self, key):
        user = self.get_user(key)

        if user:
            return ['user-{0}'.format(user.pk)]

        return []

    def raw_connect(self, message, key):
        user = self.get_user(key)

        if user:
            super(UserConsumer, self).raw_connect(message, key=key)
        else:
            self.close()
