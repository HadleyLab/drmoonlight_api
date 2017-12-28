from django.test import mock
from django.utils import timezone

from apps.main.tests import APITestCase
from apps.shifts.factories import ShiftFactory, ApplicationFactory
from apps.shifts.models import ApplicationStateEnum
from apps.shifts.tests.mixins import ShiftsTestCaseMixin


class ApplicationViewSetTestCase(ShiftsTestCaseMixin, APITestCase):
    def setUp(self):
        super(ApplicationViewSetTestCase, self).setUp()
        self.first_shift.owner = self.scheduler
        self.first_shift.save()

    def get_apply_data(self, **kwargs):
        data = {
            'shift': self.first_shift.pk,
            'text': 'Comment',
        }
        data.update(**kwargs)

        return data

    def test_apply_by_unauthenticated_failed(self):
        data = self.get_apply_data()
        resp = self.client.post(
            '/api/shifts/application/apply/', data, format='json')
        self.assertForbidden(resp)

    def test_apply_by_account_manager_failed(self):
        self.authenticate_as_account_manager()

        data = self.get_apply_data()
        resp = self.client.post(
            '/api/shifts/application/apply/', data, format='json')
        self.assertForbidden(resp)

    def test_apply_by_scheduler_failed(self):
        self.authenticate_as_scheduler()

        data = self.get_apply_data()
        resp = self.client.post(
            '/api/shifts/application/apply/', data, format='json')
        self.assertForbidden(resp)

    def test_apply_by_not_approved_resident_failed(self):
        self.authenticate_as_resident()

        data = self.get_apply_data()
        resp = self.client.post(
            '/api/shifts/application/apply/', data, format='json')
        self.assertForbidden(resp)

    def test_apply_for_started_shift_by_approved_resident_failed(self):
        self.authenticate_as_resident(self.approved_resident)

        started_shift = ShiftFactory.create(
            speciality=self.first_speciality, date_start=timezone.now())

        data = self.get_apply_data(shift=started_shift.pk)
        resp = self.client.post(
            '/api/shifts/application/apply/', data, format='json')
        self.assertBadRequest(resp)
        self.assertEqual(
            resp.data['shift'],
            ['You can not create an application for a started shift'])

    def test_apply_for_coverage_completed_shift_by_approved_resident_failed(
            self):
        self.authenticate_as_resident(self.approved_resident)

        ApplicationFactory.create(
            shift=self.first_shift, state=ApplicationStateEnum.APPROVED)

        data = self.get_apply_data()
        resp = self.client.post(
            '/api/shifts/application/apply/', data, format='json')
        self.assertBadRequest(resp)
        self.assertEqual(
            resp.data['shift'],
            ['You can not create an application for coverage completed shift'])

    def test_apply_for_unsuitable_shift_by_approved_resident_failed(self):
        self.authenticate_as_resident(self.approved_resident)

        started_shift = ShiftFactory.create()

        data = self.get_apply_data(shift=started_shift.pk)
        resp = self.client.post(
            '/api/shifts/application/apply/', data, format='json')
        self.assertBadRequest(resp)
        self.assertEqual(
            resp.data['shift'],
            ['You can not create an application for not suitable shift'])

    def test_apply_second_time_by_approved_resident_failed(self):
        self.authenticate_as_resident(self.approved_resident)

        # Create an early-created application
        ApplicationFactory.create(
            owner=self.approved_resident, shift=self.first_shift)

        data = self.get_apply_data()
        resp = self.client.post(
            '/api/shifts/application/apply/', data, format='json')

        self.assertBadRequest(resp)
        self.assertEqual(
            resp.data['non_field_errors'],
            ['There is an already created application for the shift'])

    @mock.patch(
        'apps.shifts.viewsets.application.process_application', autospec=True)
    def test_apply_by_approved_resident_success(
            self, mock_process_application):
        self.authenticate_as_resident(self.approved_resident)

        data = self.get_apply_data()
        resp = self.client.post(
            '/api/shifts/application/apply/', data, format='json')
        self.assertSuccessResponse(resp)

        application = self.first_shift.applications.all()
        self.assertEqual(len(application), 1)
        application = application.first()
        self.assertEqual(application.owner, self.approved_resident)

        mock_process_application.assert_called_with(
            application, data['text'])

    def get_invite_data(self, **kwargs):
        data = {
            'shift': self.first_shift.pk,
            'owner': self.approved_resident.pk,
            'text': 'Comment',
        }
        data.update(**kwargs)

        return data

    def test_invite_by_unauthenticated_failed(self):
        data = self.get_invite_data()
        resp = self.client.post(
            '/api/shifts/application/invite/', data, format='json')
        self.assertForbidden(resp)

    def test_invite_by_account_manager_failed(self):
        self.authenticate_as_account_manager()

        data = self.get_invite_data()
        resp = self.client.post(
            '/api/shifts/application/invite/', data, format='json')
        self.assertForbidden(resp)

    def test_invite_by_resident_failed(self):
        self.authenticate_as_resident()

        data = self.get_invite_data()
        resp = self.client.post(
            '/api/shifts/application/invite/', data, format='json')
        self.assertForbidden(resp)

    def test_invite_for_not_own_shift_by_scheduler_failed(self):
        self.authenticate_as_scheduler()

        data = self.get_invite_data(shift=self.second_shift.pk)
        resp = self.client.post(
            '/api/shifts/application/invite/', data, format='json')
        self.assertBadRequest(resp)
        self.assertEqual(
            resp.data['shift'],
            ['You can not create an application for not own shift'])

    def test_invite_not_approved_resident_by_scheduler_failed(self):
        self.authenticate_as_scheduler()

        data = self.get_invite_data(owner=self.resident.pk)
        resp = self.client.post(
            '/api/shifts/application/invite/', data, format='json')
        self.assertBadRequest(resp)
        self.assertEqual(
            resp.data['owner'],
            ['You can not create an application for a not approved resident'])

    def test_invite_for_started_shift_by_scheduler_failed(self):
        self.authenticate_as_scheduler()

        started_shift = ShiftFactory.create(
            owner=self.scheduler,
            speciality=self.first_speciality,
            date_start=timezone.now())

        data = self.get_invite_data(shift=started_shift.pk)
        resp = self.client.post(
            '/api/shifts/application/invite/', data, format='json')
        self.assertBadRequest(resp)
        self.assertEqual(
            resp.data['shift'],
            ['You can not create an application for a started shift'])

    def test_invite_for_covered_completed_shift_by_scheduler_failed(
            self):
        self.authenticate_as_scheduler()

        ApplicationFactory.create(
            shift=self.first_shift, state=ApplicationStateEnum.APPROVED)

        data = self.get_invite_data()
        resp = self.client.post(
            '/api/shifts/application/invite/', data, format='json')
        self.assertBadRequest(resp)
        self.assertEqual(
            resp.data['shift'],
            ['You can not create an application for coverage completed shift'])

    def test_invite_second_time_by_approved_resident_failed(self):
        self.authenticate_as_scheduler()

        # Create an early-created application
        ApplicationFactory.create(
            owner=self.approved_resident, shift=self.first_shift)

        data = self.get_invite_data()
        resp = self.client.post(
            '/api/shifts/application/invite/', data, format='json')

        self.assertBadRequest(resp)
        self.assertEqual(
            resp.data['non_field_errors'],
            ['There is an already created application for the shift'])

    @mock.patch(
        'apps.shifts.viewsets.application.process_invitation', autospec=True)
    def test_invite_approved_resident_by_scheduler_success(
            self, mock_process_invitation):
        self.authenticate_as_scheduler()

        data = self.get_invite_data()
        resp = self.client.post(
            '/api/shifts/application/invite/', data, format='json')
        self.assertSuccessResponse(resp)

        application = self.first_shift.applications.all()
        self.assertEqual(len(application), 1)
        application = application.first()
        self.assertEqual(application.owner, self.approved_resident)

        mock_process_invitation.assert_called_with(
            application, data['text'])

    def test_list_by_unauthenticated_failed(self):
        resp = self.client.get('/api/shifts/application/')
        self.assertForbidden(resp)

    def test_list_by_account_manager_failed(self):
        self.authenticate_as_account_manager()

        resp = self.client.get('/api/shifts/application/')
        self.assertForbidden(resp)

    def test_list_by_not_approved_resident_failed(self):
        self.authenticate_as_resident()

        resp = self.client.get('/api/shifts/application/')
        self.assertForbidden(resp)

    def test_list_by_approved_resident_success(self):
        self.authenticate_as_resident(self.approved_resident)

        first_application = ApplicationFactory.create(
            owner=self.approved_resident, shift=self.first_shift)
        second_application = ApplicationFactory.create(
            owner=self.approved_resident, shift=self.second_shift)

        resp = self.client.get('/api/shifts/application/')
        self.assertSuccessResponse(resp)

        data = resp.data
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['pk'], second_application.pk)
        self.assertEqual(data[1]['pk'], first_application.pk)

    def test_list_by_scheduler_success(self):
        self.authenticate_as_scheduler()

        application = ApplicationFactory.create(
            owner=self.approved_resident, shift=self.first_shift)

        ApplicationFactory.create(
            owner=self.approved_resident, shift=self.second_shift)

        resp = self.client.get('/api/shifts/application/')
        self.assertSuccessResponse(resp)

        data = resp.data
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['pk'], application.pk)

    # TODO: cover transition actions
