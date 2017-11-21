from apps.accounts.factories import (
    ResidencyProgramFactory, SpecialityFactory, ResidentFactory)
from apps.accounts.models import ResidentStateEnum
from apps.main.tests import APITestCase
from apps.shifts.factories import ShiftFactory
from apps.shifts.models import Shift


class ShiftViewSetTestCase(APITestCase):
    def setUp(self):
        super(ShiftViewSetTestCase, self).setUp()

        self.residency_program = ResidencyProgramFactory.create()
        self.first_speciality = SpecialityFactory.create()
        self.second_speciality = SpecialityFactory.create()
        self.first_shift = ShiftFactory.create(
            owner=self.scheduler,
            residency_years_required=0,
            residency_program=self.residency_program,
            speciality=self.first_speciality
        )
        self.second_shift = ShiftFactory.create(
            residency_years_required=5,
            residency_program=self.residency_program,
            speciality=self.second_speciality
        )

        self.approved_resident = ResidentFactory.create(
            state=ResidentStateEnum.APPROVED,
            residency_program=self.residency_program,
            residency_year=5,
        )
        self.approved_resident.specialities.add(
            self.first_speciality, self.second_speciality)

    def test_list_by_unauthenticated_failed(self):
        resp = self.client.get('/api/shifts/shift/')
        self.assertForbidden(resp)

    def test_list_by_account_manager_failed(self):
        self.authenticate_as_account_manager()

        resp = self.client.get('/api/shifts/shift/')
        self.assertForbidden(resp)

    def test_list_by_scheduler_success(self):
        """
        A scheduler should fetch only own shifts
        """
        self.authenticate_as_scheduler()

        resp = self.client.get('/api/shifts/shift/')
        self.assertSuccessResponse(resp)
        data = resp.data
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['pk'], self.first_shift.pk)

    def test_list_by_not_approved_resident_success(self):
        """
        A not approved resident should fetch all shifts
        """
        self.authenticate_as_resident()

        resp = self.client.get('/api/shifts/shift/')
        self.assertSuccessResponse(resp)
        self.assertEqual(len(resp.data), 2)

    def test_list_by_approved_resident_success(self):
        """
        An approved resident should fetch shifts which suit the resident
        """
        self.authenticate_as_resident(self.approved_resident)

        resp = self.client.get('/api/shifts/shift/')
        self.assertSuccessResponse(resp)
        data = resp.data
        self.assertEqual(len(data), 2)

        # Change residency year, it should decrease results count
        self.approved_resident.residency_year = 4
        self.approved_resident.save(update_fields=['residency_year'])

        resp = self.client.get('/api/shifts/shift/')
        self.assertSuccessResponse(resp)
        data = resp.data
        self.assertEqual(len(data), 1)

        # Remove one speciality, it should decrease results count
        self.approved_resident.specialities.remove(self.first_speciality)

        resp = self.client.get('/api/shifts/shift/')
        self.assertSuccessResponse(resp)
        data = resp.data
        self.assertEqual(len(data), 0)

    def get_shift_data(self, **kwargs):
        data = {
            'date_start': '2017-11-10T10:00Z',
            'date_end': '2017-11-10T18:00Z',
            'residency_program': self.residency_program.pk,
            'residency_years_required': 0,
            'speciality': self.first_speciality.pk,
            'payment_per_hour': True,
            'payment_amount': 100,
            'description': 'Description',
        }
        data.update(kwargs)

        return data

    def test_create_by_unauthenticated_failed(self):
        data = self.get_shift_data()
        resp = self.client.post('/api/shifts/shift/', data, format='json')
        self.assertForbidden(resp)

    def test_create_by_account_manager_failed(self):
        self.authenticate_as_account_manager()

        data = self.get_shift_data()
        resp = self.client.post('/api/shifts/shift/', data, format='json')
        self.assertForbidden(resp)

    def test_create_by_resident_failed(self):
        self.authenticate_as_resident()

        data = self.get_shift_data()
        resp = self.client.post('/api/shifts/shift/', data, format='json')
        self.assertForbidden(resp)

    def test_create_by_scheduler_success(self):
        self.authenticate_as_scheduler()

        data = self.get_shift_data()
        resp = self.client.post('/api/shifts/shift/', data, format='json')
        self.assertSuccessResponse(resp)

        shift = Shift.objects.get(pk=resp.data['pk'])
        self.assertIsNotNone(shift.date_start)
        self.assertIsNotNone(shift.date_end)
        self.assertEqual(shift.owner, self.scheduler)
        self.assertEqual(shift.description, data['description'])
        self.assertEqual(shift.residency_program.pk, data['residency_program'])
        self.assertEqual(
            shift.residency_years_required, data['residency_years_required'])
        self.assertEqual(shift.speciality.pk, data['speciality'])
        self.assertEqual(shift.payment_amount, data['payment_amount'])
        self.assertEqual(shift.payment_per_hour, data['payment_per_hour'])

    def test_bulk_create_by_scheduler_success(self):
        """
        A scheduler should create some shifts and them should be by himself 
        """
        self.authenticate_as_scheduler()

        data = self.get_shift_data()
        resp = self.client.post(
            '/api/shifts/shift/', [data, data], format='json')
        self.assertSuccessResponse(resp)
        self.assertEqual(len(resp.data), 2)
        shifts = [Shift.objects.get(pk=shift_data['pk'])
                  for shift_data in resp.data]
        self.assertEqual(shifts[0].owner, self.scheduler)
        self.assertEqual(shifts[1].owner, self.scheduler)

    def test_update_by_unauthenticated_failed(self):
        data = self.get_shift_data()
        resp = self.client.put(
            '/api/shifts/shift/{0}/'.format(self.first_shift.pk),
            data, format='json')
        self.assertForbidden(resp)

    def test_update_by_account_manager_failed(self):
        self.authenticate_as_account_manager()

        data = self.get_shift_data()
        resp = self.client.put(
            '/api/shifts/shift/{0}/'.format(self.first_shift.pk),
            data, format='json')
        self.assertForbidden(resp)

    def test_update_by_resident_failed(self):
        self.authenticate_as_resident()

        data = self.get_shift_data()
        resp = self.client.put(
            '/api/shifts/shift/{0}/'.format(self.first_shift.pk),
            data, format='json')
        self.assertForbidden(resp)

    def test_update_not_own_shift_by_scheduler_failed(self):
        self.authenticate_as_scheduler()

        data = self.get_shift_data()
        resp = self.client.put(
            '/api/shifts/shift/{0}/'.format(self.second_shift.pk),
            data, format='json')
        self.assertNotFound(resp)

    def test_update_by_scheduler_success(self):
        self.authenticate_as_scheduler()

        data = self.get_shift_data()
        resp = self.client.put(
            '/api/shifts/shift/{0}/'.format(self.first_shift.pk),
            data, format='json')
        self.assertSuccessResponse(resp)

    def test_get_by_unauthenticated_failed(self):
        resp = self.client.get(
            '/api/shifts/shift/{0}/'.format(self.first_shift.pk))
        self.assertForbidden(resp)

    def test_get_by_account_manager_failed(self):
        self.authenticate_as_account_manager()

        resp = self.client.get(
            '/api/shifts/shift/{0}/'.format(self.first_shift.pk))
        self.assertForbidden(resp)

    def test_get_by_not_approved_resident_success(self):
        self.authenticate_as_resident()

        resp = self.client.get(
            '/api/shifts/shift/{0}/'.format(self.first_shift.pk))
        self.assertSuccessResponse(resp)

        resp = self.client.get(
            '/api/shifts/shift/{0}/'.format(self.second_shift.pk))
        self.assertSuccessResponse(resp)

    def test_get_by_approved_resident_success(self):
        self.authenticate_as_resident(self.approved_resident)

        resp = self.client.get(
            '/api/shifts/shift/{0}/'.format(self.first_shift.pk))
        self.assertSuccessResponse(resp)

        resp = self.client.get(
            '/api/shifts/shift/{0}/'.format(self.second_shift.pk))
        self.assertSuccessResponse(resp)

    def test_get_not_own_shift_by_scheduler_failed(self):
        self.authenticate_as_scheduler()

        resp = self.client.get(
            '/api/shifts/shift/{0}/'.format(self.second_shift.pk))
        self.assertNotFound(resp)

    def test_get_by_scheduler_success(self):
        self.authenticate_as_scheduler()

        resp = self.client.get(
            '/api/shifts/shift/{0}/'.format(self.first_shift.pk))
        self.assertSuccessResponse(resp)

    def test_delete_by_unauthenticated_failed(self):
        resp = self.client.delete(
            '/api/shifts/shift/{0}/'.format(self.first_shift.pk))
        self.assertForbidden(resp)

    def test_delete_by_account_manager_failed(self):
        self.authenticate_as_account_manager()

        resp = self.client.delete(
            '/api/shifts/shift/{0}/'.format(self.first_shift.pk))
        self.assertForbidden(resp)

    def test_delete_by_resident_failed(self):
        self.authenticate_as_resident()

        resp = self.client.delete(
            '/api/shifts/shift/{0}/'.format(self.first_shift.pk))
        self.assertForbidden(resp)

    def test_delete_not_own_shift_by_scheduler_failed(self):
        self.authenticate_as_scheduler()

        resp = self.client.delete(
            '/api/shifts/shift/{0}/'.format(self.second_shift.pk))
        self.assertNotFound(resp)

    def test_delete_by_scheduler_success(self):
        self.authenticate_as_scheduler()

        resp = self.client.delete(
            '/api/shifts/shift/{0}/'.format(self.first_shift.pk))
        self.assertSuccessResponse(resp)

        self.assertFalse(Shift.objects.filter(pk=self.first_shift.pk).exists())
