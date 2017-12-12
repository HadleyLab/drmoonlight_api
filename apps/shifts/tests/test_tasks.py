from datetime import timedelta

from django.test import TestCase, mock
from django.utils import timezone

from apps.shifts.factories import ShiftFactory, ApplicationFactory
from apps.shifts.models import ApplicationStateEnum
from apps.shifts.tasks import (
    daily_make_confirmed_applications_completed_for_ended_shifts)


class TasksTestCase(TestCase):
    @mock.patch('apps.shifts.models.application.process_completing')
    def test_daily_make_confirmed_applications_completed_for_ended_shifts(
            self, mock_process_completing):
        not_ended_shift = ShiftFactory.create()
        confirmed_application_for_not_ended_shift = ApplicationFactory.create(
            shift=not_ended_shift,
            state=ApplicationStateEnum.CONFIRMED)

        ended_shift = ShiftFactory.create(
            date_start=timezone.now() - timedelta(days=3),
            date_end=timezone.now() - timedelta(days=2))
        new_application = ApplicationFactory.create(
            shift=ended_shift, state=ApplicationStateEnum.NEW)
        confirmed_application = ApplicationFactory.create(
            shift=ended_shift, state=ApplicationStateEnum.CONFIRMED)
        completed_application = ApplicationFactory.create(
            shift=ended_shift, state=ApplicationStateEnum.COMPLETED)

        daily_make_confirmed_applications_completed_for_ended_shifts()

        confirmed_application_for_not_ended_shift.refresh_from_db()
        self.assertEqual(
            confirmed_application_for_not_ended_shift.state,
            ApplicationStateEnum.CONFIRMED)

        new_application.refresh_from_db()
        self.assertEqual(
            new_application.state, ApplicationStateEnum.NEW)

        completed_application.refresh_from_db()
        self.assertEqual(
            completed_application.state, ApplicationStateEnum.COMPLETED)

        confirmed_application.refresh_from_db()
        self.assertEqual(
            confirmed_application.state, ApplicationStateEnum.COMPLETED)

        mock_process_completing.assert_called_once_with(
            confirmed_application, ended_shift.owner.user_ptr, '')
