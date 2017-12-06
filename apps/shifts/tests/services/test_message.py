from django.test import TestCase, mock

from apps.accounts.factories import ResidentFactory
from apps.shifts.factories import (
    MessageFactory, ApplicationFactory, ShiftFactory)
from apps.shifts.models import Message
from apps.shifts.services.message import (
    process_message_creation, create_message)


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

        mock_notify_message_created.assert_not_called()

    def test_create_message_without_text_does_not_create_message(self):
        message = create_message(self.application, self.resident, '')

        self.assertIsNone(message)

    def test_create_message_with_text_creates_message(self):
        message = create_message(self.application, self.resident, 'Comment')

        self.assertIsNotNone(message)

        # Refresh message to fetch actual data from db
        message = Message.objects.get(pk=message.pk)
        self.assertEqual(message.owner, self.resident.user_ptr)
        self.assertEqual(message.text, 'Comment')
