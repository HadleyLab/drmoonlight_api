from django.test import TestCase, mock

from apps.accounts.factories import ResidentFactory, SchedulerFactory
from apps.shifts.factories import (
    MessageFactory, ApplicationFactory, ShiftFactory)
from apps.shifts.services.application import (
    get_opposite_side, process_application, process_invitation,
    process_approving, process_rejecting, process_renewing, process_postponing,
    process_confirming, process_completing, process_cancelling)


@mock.patch(
    'apps.shifts.services.application.create_message', autospec=True)
class ApplicationServiceTestCase(TestCase):
    def setUp(self):
        self.scheduler = SchedulerFactory.create()
        self.resident = ResidentFactory.create()
        self.shift = ShiftFactory.create(owner=self.scheduler)
        self.application = ApplicationFactory.create(
            shift=self.shift, owner=self.resident)

    def test_get_opposite_side_works_correctly(self, mock_create_message):
        self.assertEqual(
            get_opposite_side(self.application, self.resident), self.scheduler)
        self.assertEqual(
            get_opposite_side(self.application, self.scheduler), self.resident)

    def test_process_application_works_without_errors(
            self, mock_create_message):
        process_application(self.application)

    def test_process_invitation_works_without_errors(self, mock_create_message):
        process_invitation(self.application)

    def test_process_approving_works_without_errors(self, mock_create_message):
        mock_create_message.return_value = MessageFactory.create(
            application=self.application, owner=self.scheduler)

        process_approving(self.application, self.scheduler, 'Comment')

        mock_create_message.assert_called_with(
            self.application, self.scheduler, 'Comment')

    def test_process_rejecting_works_without_errors(self, mock_create_message):
        mock_create_message.return_value = MessageFactory.create(
            application=self.application, owner=self.scheduler)

        process_rejecting(self.application, self.scheduler, 'Comment')

        mock_create_message.assert_called_with(
            self.application, self.scheduler, 'Comment')

    def test_process_postponing_works_without_errors(self, mock_create_message):
        mock_create_message.return_value = MessageFactory.create(
            application=self.application, owner=self.scheduler)

        process_postponing(self.application)

        mock_create_message.assert_called_with(
            self.application,
            self.scheduler,
            'You application was postponed due to accepting an '
            'another application')

    def test_process_renewing_works_without_errors(self, mock_create_message):
        mock_create_message.return_value = MessageFactory.create(
            application=self.application, owner=self.scheduler)

        process_renewing(self.application)

        mock_create_message.assert_called_with(
            self.application,
            self.scheduler,
            'The shift became available and your application was renewed')

    def test_process_confirming_works_without_errors(self, mock_create_message):
        mock_create_message.return_value = MessageFactory.create(
            application=self.application, owner=self.scheduler)

        process_confirming(self.application, self.scheduler, 'Comment')

        mock_create_message.assert_called_with(
            self.application, self.scheduler, 'Comment')

    def test_process_cancelling_by_resident_works_without_errors(
            self, mock_create_message):
        mock_create_message.return_value = MessageFactory.create(
            application=self.application, owner=self.scheduler)

        process_cancelling(self.application, self.resident, 'Comment')

        mock_create_message.assert_called_with(
            self.application, self.resident, 'Comment')

    def test_process_cancelling_by_scheduler_works_without_errors(
            self, mock_create_message):
        mock_create_message.return_value = MessageFactory.create(
            application=self.application, owner=self.scheduler)

        process_cancelling(self.application, self.scheduler, 'Comment')

        mock_create_message.assert_called_with(
            self.application, self.scheduler, 'Comment')

    def test_process_completing_works_without_errors(self, mock_create_message):
        mock_create_message.return_value = MessageFactory.create(
            application=self.application, owner=self.scheduler)

        process_completing(self.application, self.scheduler, 'Comment')

        mock_create_message.assert_called_with(
            self.application, self.scheduler, 'Comment')
