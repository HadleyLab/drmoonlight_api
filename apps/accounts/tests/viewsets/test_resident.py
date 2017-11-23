from apps.accounts.factories import ResidentFactory, SpecialityFactory, \
    ResidencyProgramFactory
from apps.accounts.models import Resident, ResidentStateEnum
from apps.main.tests import APITestCase


class ResidentViewSetTestCase(APITestCase):
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

    def test_retrieve_by_unauthenticated_failed(self):
        resp = self.client.get('/api/accounts/resident/{0}/'.format(
            self.resident.pk))
        self.assertForbidden(resp)

    def test_retrieve_myself_by_resident_success(self):
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
            self.resident.pk), data, format='json')
        self.assertSuccessResponse(resp)

        self.resident.refresh_from_db()
        self.assertSetEqual(
            set(self.resident.specialities.values_list('pk', flat=True)),
            set(data['specialities']))
        self.assertEqual(
            self.resident.residency_program.pk,
            data['residency_program'])
        self.assertEqual(self.resident.residency_year, data['residency_year'])

    def test_fill_profile_by_resident_success(self):
        self.authenticate_as_resident()
        data = {
            'specialities': [SpecialityFactory.create().pk, ],
            'residency_program': ResidencyProgramFactory.create().pk,
            'residency_year': 2017,
        }
        resp = self.client.post(
            '/api/accounts/resident/{0}/fill_profile/'.format(
                self.resident.pk),
            data, format='json')
        self.assertSuccessResponse(resp)
        self.resident.refresh_from_db()

        self.assertEqual(
            self.resident.state,
            ResidentStateEnum.PROFILE_FILLED)
        self.assertSetEqual(
            set(self.resident.specialities.values_list('pk', flat=True)),
            set(data['specialities']))
        self.assertEqual(
            self.resident.residency_program.pk,
            data['residency_program'])
        self.assertEqual(self.resident.residency_year, data['residency_year'])

        # TODO: check that email sent

    def test_approve_by_account_manager_success(self):
        self.resident.state = ResidentStateEnum.PROFILE_FILLED
        self.resident.save(update_fields=['state'])

        self.authenticate_as_account_manager()
        resp = self.client.post(
            '/api/accounts/resident/{0}/approve/'.format(self.resident.pk))
        self.assertSuccessResponse(resp)

        self.resident.refresh_from_db()
        self.assertEqual(self.resident.state, ResidentStateEnum.APPROVED)

        # TODO: check that email sent

    def test_reject_by_account_manager_success(self):
        self.resident.state = ResidentStateEnum.PROFILE_FILLED
        self.resident.save(update_fields=['state'])

        self.authenticate_as_account_manager()
        resp = self.client.post(
            '/api/accounts/resident/{0}/reject/'.format(self.resident.pk))
        self.assertSuccessResponse(resp)

        self.resident.refresh_from_db()
        self.assertEqual(self.resident.state, ResidentStateEnum.REJECTED)

        # TODO: check that email sent
