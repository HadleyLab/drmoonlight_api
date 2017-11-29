import json

from channels import Group
from channels.test import TransactionChannelTestCase
from django.db import transaction
from django.test import override_settings

from apps.accounts.factories import ResidentFactory, SchedulerFactory
from apps.shifts.factories import MessageFactory, ApplicationFactory, \
    ShiftFactory
from apps.shifts.notifications import notify_message_created, \
    notify_application_state_changed


class NotificationsTestCase(TransactionChannelTestCase):
    def setUp(self):
        self.scheduler = SchedulerFactory.create()
        self.resident = ResidentFactory.create()
        self.shift = ShiftFactory.create(owner=self.scheduler)
        self.application = ApplicationFactory.create(
            shift=self.shift, owner=self.resident)

    @override_settings(SYNC_ON_COMMIT=False)
    def test_notify_message_created(self):
        message = MessageFactory.create(
            application=self.application, owner=self.resident)

        Group('user-{0}'.format(self.resident.pk)).add('ws-resident')
        Group('user-{0}'.format(self.scheduler.pk)).add('ws-scheduler')

        # Run notification inside the transaction, because
        # it will send notifications at the commit
        with transaction.atomic():
            notify_message_created(message)

        # Check message for a resident
        result = self.get_next_message('ws-resident')
        parsed_result = json.loads(result['text'])

        self.assertEqual(parsed_result['event'], 'message_created')
        self.assertEqual(parsed_result['payload']['message']['pk'], message.pk)

        # Check message for a scheduler
        result = self.get_next_message('ws-scheduler')
        parsed_result = json.loads(result['text'])

        self.assertEqual(parsed_result['event'], 'message_created')
        self.assertEqual(parsed_result['payload']['message']['pk'], message.pk)

    @override_settings(SYNC_ON_COMMIT=False)
    def test_notify_application_state_changed(self):
        message = MessageFactory.create(
            application=self.application, owner=self.resident)

        Group('user-{0}'.format(self.resident.pk)).add('ws-resident')
        Group('user-{0}'.format(self.scheduler.pk)).add('ws-scheduler')

        # Run notification inside the transaction, because
        # it will send notifications at the commit
        with transaction.atomic():
            notify_application_state_changed(self.application, message)

        # Check message for a resident
        result = self.get_next_message('ws-resident')
        parsed_result = json.loads(result['text'])

        self.assertEqual(parsed_result['event'], 'application_state_changed')
        payload = parsed_result['payload']
        self.assertEqual(payload['message']['pk'], message.pk)
        self.assertEqual(payload['application']['pk'], self.application.pk)
        # The available transitions depends on user
        self.assertEqual(
            payload['application']['available-transitions'],
            [])

        # Check message for a scheduler
        result = self.get_next_message('ws-scheduler')
        parsed_result = json.loads(result['text'])

        self.assertEqual(parsed_result['event'], 'application_state_changed')
        payload = parsed_result['payload']
        self.assertEqual(payload['message']['pk'], message.pk)
        self.assertEqual(payload['application']['pk'], self.application.pk)
        # The available transitions depends on user
        self.assertEqual(
            payload['application']['available-transitions'],
            ['approve', 'reject'])
