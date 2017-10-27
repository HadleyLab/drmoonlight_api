from django.test import TestCase
from django_fsm import has_transition_perm

from apps.accounts.factories import ResidentFactory, SchedulerFactory
from apps.shifts.factories import ApplicationFactory, ShiftFactory
from apps.shifts.models import ApplicationStateEnum


class ApplicationTest(TestCase):
    def setUp(self):
        super(ApplicationTest, self).setUp()

        self.resident = ResidentFactory.create()
        self.scheduler = SchedulerFactory.create()
        self.shift = ShiftFactory.create(owner=self.scheduler)

    def test_approve(self):
        # New applications
        first_application = ApplicationFactory.create(shift=self.shift)
        second_application = ApplicationFactory.create(shift=self.shift)

        another_shift_application = ApplicationFactory.create()

        # Cancelled applications
        cancelled_application = ApplicationFactory.create(
            shift=self.shift,
            state=ApplicationStateEnum.CANCELLED)

        first_application.approve()
        first_application.save()

        first_application.refresh_from_db()
        self.assertEqual(
            first_application.state, ApplicationStateEnum.APPROVED)

        second_application.refresh_from_db()
        self.assertEqual(
            second_application.state, ApplicationStateEnum.REJECTED)

        cancelled_application.refresh_from_db()
        self.assertEqual(
            cancelled_application.state, ApplicationStateEnum.CANCELLED)

        another_shift_application.refresh_from_db()
        self.assertEqual(
            another_shift_application.state, ApplicationStateEnum.NEW)

    def test_approve_permissions(self):
        application = ApplicationFactory.create(
            owner=self.resident, shift=self.shift)

        # Resident can't approve application
        self.assertFalse(has_transition_perm(
            application.approve, self.resident))

        # Scheduler can accept own shift's applications
        self.assertTrue(has_transition_perm(
            application.approve, self.scheduler))

        another_application = ApplicationFactory.create()
        # Scheduler can't approve now own shift's applications
        self.assertFalse(has_transition_perm(
            another_application.approve, self.scheduler))

    def test_reject_permissions(self):
        application = ApplicationFactory.create(
            owner=self.resident, shift=self.shift)

        # Resident can't reject application
        self.assertFalse(has_transition_perm(
            application.reject, self.resident))

        # Scheduler can reject own shift's applications
        self.assertTrue(has_transition_perm(
            application.reject, self.scheduler))

    def test_confirm_permissions(self):
        application = ApplicationFactory.create(
            owner=self.resident, shift=self.shift,
            state=ApplicationStateEnum.APPROVED)

        # Resident can confirm approved application
        self.assertTrue(has_transition_perm(
            application.confirm, self.resident))

        # Scheduler can't confirm approved applications
        self.assertFalse(has_transition_perm(
            application.confirm, self.scheduler))

    def test_cancel_permissions(self):
        application = ApplicationFactory.create(
            owner=self.resident, shift=self.shift,
            state=ApplicationStateEnum.APPROVED)

        # Resident can cancel approved application
        self.assertTrue(has_transition_perm(
            application.cancel, self.resident))

        # Scheduler can cancel approved applications
        self.assertTrue(has_transition_perm(
            application.cancel, self.scheduler))

        application = ApplicationFactory.create(
            owner=self.resident, shift=self.shift,
            state=ApplicationStateEnum.CONFIRMED)

        # Resident can cancel confirmed application
        self.assertTrue(has_transition_perm(
            application.cancel, self.resident))

        # Scheduler can cancel confirmed applications
        self.assertTrue(has_transition_perm(
            application.cancel, self.scheduler))

    def test_complete_permissions(self):
        application = ApplicationFactory.create(
            owner=self.resident, shift=self.shift,
            state=ApplicationStateEnum.CONFIRMED)

        # Resident can't complete confirmed application
        self.assertFalse(has_transition_perm(
            application.complete, self.resident))

        # Scheduler can complete confirmed applications
        self.assertTrue(has_transition_perm(
            application.complete, self.scheduler))
