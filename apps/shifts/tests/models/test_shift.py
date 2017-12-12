from datetime import timedelta
from django.test import TestCase
from django.utils import timezone

from apps.shifts.factories import ShiftFactory, ApplicationFactory
from apps.shifts.models import ApplicationStateEnum, ShiftStateEnum

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
        self.shift.date_end = timezone.now()
        self.shift.save()
        self.assertTrue(self.shift.is_ended)

        self.shift.date_end = timezone.now() - timedelta(hours=1)
        self.shift.save()
        self.assertTrue(self.shift.is_ended)

        self.shift.date_end = timezone.now() + timedelta(hours=1)
        self.shift.save()
        self.assertFalse(self.shift.is_ended)

    def test_state_for_not_started_shift(self):
        self.assertEqual(self.shift.state, ShiftStateEnum.WITHOUT_APPLIES)

        application = ApplicationFactory.create(
            shift=self.shift, state=ApplicationStateEnum.NEW)
        self.assertEqual(self.shift.state, ShiftStateEnum.REQUIRE_APPROVAL)

        application.state = ApplicationStateEnum.APPROVED
        application.save()

        self.assertEqual(self.shift.state, ShiftStateEnum.COVERAGE_COMPLETED)

        application.state = ApplicationStateEnum.CANCELLED
        application.save()
        self.assertEqual(self.shift.state, ShiftStateEnum.WITHOUT_APPLIES)

    def test_state_for_started_shift(self):
        self.shift.date_start = timezone.now() - timedelta(hours=1)
        self.shift.save()

        self.assertEqual(self.shift.state, ShiftStateEnum.ACTIVE)

    def test_state_for_ended_shift(self):
        self.shift.date_end = timezone.now() - timedelta(hours=1)
        self.shift.save()

        self.assertEqual(self.shift.state, ShiftStateEnum.FAILED)

        application = ApplicationFactory.create(
            shift=self.shift, state=ApplicationStateEnum.NEW)
        self.assertEqual(self.shift.state, ShiftStateEnum.FAILED)

        application.state = ApplicationStateEnum.CANCELLED
        application.save()
        self.assertEqual(self.shift.state, ShiftStateEnum.FAILED)

        application.state = ApplicationStateEnum.APPROVED
        application.save()
        self.assertEqual(self.shift.state, ShiftStateEnum.FAILED)

        application.state = ApplicationStateEnum.CONFIRMED
        application.save()
        self.assertEqual(self.shift.state, ShiftStateEnum.COMPLETED)

        application.state = ApplicationStateEnum.COMPLETED
        application.save()
        self.assertEqual(self.shift.state, ShiftStateEnum.COMPLETED)
