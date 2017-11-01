from apps.accounts.factories import ResidentFactory, SpecialityFactory, \
    ResidencyProgramFactory
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

    def test_retrieve_myself_by_resident_failed(self):
        self.authenticate_as_resident()
        resp = self.client.get('/api/accounts/resident/{0}/'.format(
            self.resident.pk))
        self.assertSuccessResponse(resp)

    def test_retrieve_not_myself_by_resident_failed(self):
        resident = ResidentFactory.create()
        self.authenticate_as_resident(resident)
        resp = self.client.get('/api/accounts/resident/{0}/'.format(
            self.resident.pk))
        self.assertForbidden(resp)

    def test_retrieve_by_scheduler_failed(self):
        self.authenticate_as_scheduler()
        resp = self.client.get('/api/accounts/resident/{0}/'.format(
            self.resident.pk))
        self.assertForbidden(resp)

    def test_retrieve_by_account_manager_success(self):
        self.authenticate_as_account_manager()
        resp = self.client.get('/api/accounts/resident/{0}/'.format(
            self.resident.pk))
        self.assertSuccessResponse(resp)

    def test_update_by_account_manager_failed(self):
        self.authenticate_as_account_manager()
        resp = self.client.patch('/api/accounts/resident/{0}/'.format(
            self.resident.pk))
        self.assertForbidden(resp)

    def test_update_by_scheduler_failed(self):
        self.authenticate_as_scheduler()
        resp = self.client.patch('/api/accounts/resident/{0}/'.format(
            self.resident.pk))
        self.assertForbidden(resp)

    def test_update_not_self_by_resident_failed(self):
        resident = ResidentFactory.create()
        self.authenticate_as_resident(resident)
        resp = self.client.patch('/api/accounts/resident/{0}/'.format(
            self.resident.pk))
        self.assertForbidden(resp)

    def test_update_myself_by_resident_success(self):
        self.authenticate_as_resident()
        data = {
            'specialities': [SpecialityFactory.create().pk, ],
            'residency_program': ResidencyProgramFactory.create().pk,
            'residency_year': 2017,
        }
        resp = self.client.patch('/api/accounts/resident/{0}/'.format(
            self.resident.pk), format='json')
        self.assertSuccessResponse(resp)
