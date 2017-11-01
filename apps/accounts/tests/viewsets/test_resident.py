from apps.accounts.factories import ResidentFactory
from apps.accounts.models import Resident
from apps.main.tests import APITestCase


class ResidentTestCase(APITestCase):
    def test_create_token_as_resident(self):
        token = self.create_token(self.resident)
        self.assertIsNotNone(token)

    def test_create_token_as_not_active_resident(self):
        resident = ResidentFactory.create(is_active=False)
        token = self.create_token(resident)
        self.assertIsNone(token)

    def test_create(self):
        data = {
            'email': 'resident@gmail.com',
            'password': 'Str0ngPassW0RD',
            'first_name': 'First',
            'last_name': 'Last',
        }
        resp = self.client.post('/api/accounts/resident/', data)
        self.assertSuccessResponse(resp)

        resident = Resident.objects.get(pk=resp.data['pk'])
        self.assertFalse(resident.is_active)
        self.assertEqual(resident.email, data['email'])
        self.assertEqual(resident.first_name, data['first_name'])
        self.assertEqual(resident.last_name, data['last_name'])
        self.assertTrue(resident.check_password(data['password']))
