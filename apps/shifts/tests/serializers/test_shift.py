from django.test import TestCase

from apps.accounts.factories import SchedulerFactory, ResidentFactory
from apps.shifts.factories import ShiftFactory, ApplicationFactory
from apps.shifts.factories.request import ExtendedRequestFactory
from apps.shifts.serializers import ShiftSerializer


class ShiftSerializerTestCase(TestCase):
    def setUp(self):
        self.request = ExtendedRequestFactory()
        self.scheduler = SchedulerFactory.create()
        self.resident = ResidentFactory.create()
        self.shift = ShiftFactory.create(owner=self.scheduler)

    def test_has_already_applied_for_scheduler_equals_none(self):
        self.request.user = self.scheduler.user_ptr

        serializer = ShiftSerializer(
            instance=self.shift, context={'request': self.request})

        self.assertIsNone(serializer.data['has_already_applied'])

    def test_has_already_applied_for_resident_equals_false(self):
        # Create an application by another resident
        ApplicationFactory.create(shift=self.shift)
        self.request.user = self.resident.user_ptr

        serializer = ShiftSerializer(
            instance=self.shift, context={'request': self.request})

        self.assertFalse(serializer.data['has_already_applied'])

    def test_has_already_applied_for_resident_equals_true(self):
        # Create an application by our resident
        ApplicationFactory.create(shift=self.shift, owner=self.resident)
        self.request.user = self.resident.user_ptr

        serializer = ShiftSerializer(
            instance=self.shift, context={'request': self.request})

        self.assertTrue(serializer.data['has_already_applied'])
