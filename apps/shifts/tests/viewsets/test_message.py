from django.test import mock

from apps.main.tests import APITestCase
from apps.shifts.factories import ApplicationFactory, MessageFactory
from apps.shifts.tests.mixins import ShiftsTestCaseMixin


class MessageViewSetTestCase(ShiftsTestCaseMixin, APITestCase):
    def setUp(self):
        super(MessageViewSetTestCase, self).setUp()
        self.first_shift.owner = self.scheduler
        self.first_shift.save(update_fields=['owner'])

        self.first_application = ApplicationFactory.create(
            owner=self.approved_resident,
            shift=self.first_shift
        )
        self.second_application = ApplicationFactory.create(
            owner=self.approved_resident,
            shift=self.second_shift
        )
        self.third_application = ApplicationFactory.create(
            shift=self.second_shift
        )
        self.first_application_message = MessageFactory.create(
            application=self.first_application, owner=self.scheduler)
        self.second_application_message = MessageFactory.create(
            application=self.second_application, owner=self.approved_resident)

    def test_list_by_unauthenticated_failed(self):
        resp = self.client.get(
            '/api/shifts/application/{0}/message/'.format(
                self.first_application.pk))
        self.assertForbidden(resp)

    def test_list_by_account_manager_failed(self):
        self.authenticate_as_account_manager()

        resp = self.client.get(
            '/api/shifts/application/{0}/message/'.format(
                self.first_application.pk))
        self.assertForbidden(resp)

    def test_list_by_not_approved_failed(self):
        self.authenticate_as_account_manager()

        resp = self.client.get(
            '/api/shifts/application/{0}/message/'.format(
                self.first_application.pk))
        self.assertForbidden(resp)

    def test_list_for_not_own_application_by_approved_resident_failed(self):
        self.authenticate_as_resident(self.approved_resident)

        resp = self.client.get(
            '/api/shifts/application/{0}/message/'.format(
                self.third_application.pk))
        self.assertNotFound(resp)

    def test_list_for_not_own_application_by_scheduler_failed(self):
        self.authenticate_as_scheduler()

        resp = self.client.get(
            '/api/shifts/application/{0}/message/'.format(
                self.third_application.pk))
        self.assertNotFound(resp)

    def test_list_for_own_application_by_approved_resident_success(self):
        self.authenticate_as_resident(self.approved_resident)

        resp = self.client.get(
            '/api/shifts/application/{0}/message/'.format(
                self.first_application.pk))
        self.assertSuccessResponse(resp)

        data = resp.data
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['pk'], self.first_application_message.pk)

        resp = self.client.get(
            '/api/shifts/application/{0}/message/'.format(
                self.second_application.pk))
        self.assertSuccessResponse(resp)

        data = resp.data
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['pk'], self.second_application_message.pk)

    def test_list_for_own_application_by_scheduler_success(self):
        self.authenticate_as_scheduler()

        resp = self.client.get(
            '/api/shifts/application/{0}/message/'.format(
                self.first_application.pk))
        self.assertSuccessResponse(resp)

        data = resp.data
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['pk'], self.first_application_message.pk)

    def get_message_data(self, **kwargs):
        data = {
            'message': 'Message',
        }
        data.update(**kwargs)

        return data

    def test_create_by_unauthenticated_failed(self):
        data = self.get_message_data()
        resp = self.client.post(
            '/api/shifts/application/{0}/message/'.format(
                self.first_application.pk),
            data,
            format='json')
        self.assertForbidden(resp)

    def test_create_by_account_manager_failed(self):
        self.authenticate_as_account_manager()

        data = self.get_message_data()
        resp = self.client.post(
            '/api/shifts/application/{0}/message/'.format(
                self.first_application.pk),
            data,
            format='json')
        self.assertForbidden(resp)

    def test_create_by_not_approved_resident_failed(self):
        self.authenticate_as_resident()

        data = self.get_message_data()
        resp = self.client.post(
            '/api/shifts/application/{0}/message/'.format(
                self.first_application.pk),
            data,
            format='json')
        self.assertForbidden(resp)

    def test_create_for_not_own_application_by_approved_resident_failed(self):
        self.authenticate_as_resident(self.approved_resident)

        data = self.get_message_data()
        resp = self.client.post(
            '/api/shifts/application/{0}/message/'.format(
                self.third_application.pk),
            data,
            format='json')
        self.assertNotFound(resp)

    def test_create_for_not_own_application_by_scheduler_failed(self):
        self.authenticate_as_scheduler()

        data = self.get_message_data()
        resp = self.client.post(
            '/api/shifts/application/{0}/message/'.format(
                self.third_application.pk),
            data,
            format='json')
        self.assertNotFound(resp)

    @mock.patch(
        'apps.shifts.viewsets.message.process_message_creation', autospec=True)
    def test_create_for_own_application_by_scheduler_success(
            self, mock_process_message_creation):
        self.authenticate_as_scheduler()

        data = self.get_message_data()
        resp = self.client.post(
            '/api/shifts/application/{0}/message/'.format(
                self.first_application.pk),
            data,
            format='json')
        self.assertSuccessResponse(resp)

        message = self.first_application.messages.get(pk=resp.data['pk'])
        self.assertEqual(message.owner, self.scheduler.user_ptr)
        self.assertEqual(message.message, data['message'])
        mock_process_message_creation.assert_called_with(message)

    @mock.patch(
        'apps.shifts.viewsets.message.process_message_creation', autospec=True)
    def test_create_for_own_application_by_approved_resident_success(
            self, mock_process_message_creation):
        self.authenticate_as_resident(self.approved_resident)

        data = self.get_message_data()
        resp = self.client.post(
            '/api/shifts/application/{0}/message/'.format(
                self.first_application.pk),
            data,
            format='json')
        self.assertSuccessResponse(resp)

        message = self.first_application.messages.get(pk=resp.data['pk'])
        self.assertEqual(message.owner, self.approved_resident.user_ptr)
        self.assertEqual(message.message, data['message'])
        mock_process_message_creation.assert_called_with(message)



