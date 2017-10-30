from datetime import timedelta
from django.test import TestCase
from django.utils import timezone

from apps.shifts.factories import ShiftFactory


class ShiftTest(TestCase):
    def setUp(self):
        super(ShiftTest, self).setUp()

        self.shift = ShiftFactory.create()

    def test_is_started(self):
        self.shift.date_start = timezone.now() - timedelta(hours=1)
        self.shift.save()
        self.assertTrue(self.shift.is_started)

        self.shift.date_start = timezone.now() + timedelta(hours=1)
        self.shift.save()
        self.assertFalse(self.shift.is_started)

    def test_is_ended(self):
        self.shift.date_end = timezone.now() - timedelta(hours=1)
        self.shift.save()
        self.assertTrue(self.shift.is_ended)

        self.shift.date_end = timezone.now() + timedelta(hours=1)
        self.shift.save()
        self.assertFalse(self.shift.is_ended)
