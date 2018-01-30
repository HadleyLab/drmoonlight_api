import os

from django.test import TestCase
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.accounts.factories import SchedulerFactory, ResidentFactory
from apps.shifts.factories import ShiftFactory, ApplicationFactory, \
    MessageFactory
from apps.shifts.factories.request import ExtendedRequestFactory
from apps.shifts.serializers import MessageSerializer


class MessageSerializerTestCase(TestCase):
    def setUp(self):
        self.request = ExtendedRequestFactory()
        self.scheduler = SchedulerFactory.create()
        self.resident = ResidentFactory.create()
        self.shift = ShiftFactory.create(owner=self.scheduler)
        self.application = ApplicationFactory.create(shift=self.shift)
        self.message = MessageFactory.create(
            owner=self.resident,
            application=self.application,
            text='test text')
        self.message2 = MessageFactory.create(
            owner=self.resident,
            application=self.application,
            text='see attachment',
            attachment=SimpleUploadedFile('text.txt', b'Some text in file'))

    def test_serialize_message(self):
        serializer = MessageSerializer(
            self.message, context={'request': self.request})
        self.assertEqual(serializer.data['owner'], self.resident.pk)
        self.assertEqual(serializer.data['application'], self.application.pk)
        self.assertEqual(serializer.data['text'], 'test text')
        self.assertIsNone(serializer.data['attachment'])
        self.assertIsNone(serializer.data['thumbnail'])

    def test_serialize_with_text_file(self):
        serializer = MessageSerializer(
            self.message2, context={'request': self.request})
        self.assertEqual('see attachment', serializer.data['text'])
        self.assertIsNotNone(serializer.data['attachment'])
        self.assertIsNone(serializer.data['thumbnail'])

    def test_serialize_with_thumbnail(self):
        avatar_path = os.path.join(
            settings.BASE_DIR, 'apps/accounts/tests/fixtures/avatar.jpg')
        message3 = MessageFactory.create(
            owner=self.resident,
            application=self.application,
            text='attach image',
            attachment=SimpleUploadedFile('avatar.jpg',
                                          open(avatar_path, 'rb').read()))

        serializer = MessageSerializer(
            message3, context={'request': self.request})
        self.assertIsNotNone(serializer.data['attachment'])
        self.assertIsNotNone(serializer.data['thumbnail'])
