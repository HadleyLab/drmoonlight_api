from django.test import TestCase, mock

from apps.accounts.factories import ResidentFactory
from apps.shifts.factories import MessageFactory, ApplicationFactory, \
    ShiftFactory
from apps.shifts.services.message import process_message_creation


class MessageServiceTestCase(TestCase):
    def setUp(self):
        self.resident = ResidentFactory.create()
        self.shift = ShiftFactory.create()
        self.application = ApplicationFactory.create(
            shift=self.shift, owner=self.resident)

    @mock.patch(
        'apps.shifts.services.message.notify_message_created', autospec=True)
    def test_process_message_creation_with_notification_notifies(
            self, mock_notify_message_created):
        message = MessageFactory.create(
            application=self.application, owner=self.resident)

        process_message_creation(message, notify=True)

        mock_notify_message_created.assert_called_with(message)

    @mock.patch(
        'apps.shifts.services.message.notify_message_created', autospec=True)
    def test_process_message_creation_without_notification_notifies(
            self, mock_notify_message_created):
        message = MessageFactory.create(
            application=self.application, owner=self.resident)

        process_message_creation(message, notify=False)

        self.assertFalse(mock_notify_message_created.called)
