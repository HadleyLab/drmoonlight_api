from channels import Channel, Group
from channels.test import ChannelTestCase, WSClient

from apps.accounts.factories import ResidentFactory, TokenFactory


class UserConsumerTestCase(ChannelTestCase):
    def test_authentication_with_token_success(self):
        client = WSClient()

        resident = ResidentFactory.create()
        token = TokenFactory.create(user=resident)

        client.send_and_consume(
            'websocket.connect',
            path='/accounts/user/{0}/'.format(token.key),
            check_accept=False
        )

        received = client.receive(json=False)
        self.assertEqual(received, {"accept": True})

    def test_authentication_with_wrong_token_failed(self):
        client = WSClient()

        client.send_and_consume(
            'websocket.connect',
            path='/accounts/user/wrong/',
            check_accept=False
        )

        received = client.receive(json=False)
        self.assertEqual(received, {"close": True})

    def test_receive_for_authenticated_success(self):
        client = WSClient()

        resident = ResidentFactory.create()
        token = TokenFactory.create(user=resident)

        client.send_and_consume(
            'websocket.connect',
            path='/accounts/user/{0}/'.format(token.key),
        )

        Group('user-{0}'.format(resident.pk)).send(
            {'text': 'ok'}, immediately=True)
        self.assertEqual(client.receive(json=False), 'ok')
