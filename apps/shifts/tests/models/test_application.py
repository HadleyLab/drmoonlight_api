from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django_fsm import has_transition_perm

from apps.accounts.factories import ResidentFactory, SchedulerFactory
from apps.shifts.factories import ApplicationFactory, ShiftFactory, \
    MessageFactory
from apps.shifts.models import ApplicationStateEnum, Application


class ApplicationTest(TestCase):
    def setUp(self):
        super(ApplicationTest, self).setUp()

        self.resident = ResidentFactory.create()
        self.scheduler = SchedulerFactory.create()
        self.shift = ShiftFactory.create(owner=self.scheduler)

    def test_aggregate_count_by_state(self):
        ApplicationFactory.create(state=ApplicationStateEnum.CANCELLED)
        ApplicationFactory.create(state=ApplicationStateEnum.APPROVED)
        ApplicationFactory.create(state=ApplicationStateEnum.REJECTED)
        ApplicationFactory.create(state=ApplicationStateEnum.REJECTED)
        ApplicationFactory.create(state=ApplicationStateEnum.POSTPONED)
        ApplicationFactory.create(state=ApplicationStateEnum.POSTPONED)

        applications_count = Application.objects.aggregate_count_by_state()
        self.assertDictEqual(applications_count, {
            ApplicationStateEnum.CANCELLED: 1,
            ApplicationStateEnum.APPROVED: 1,
            ApplicationStateEnum.REJECTED: 2,
            ApplicationStateEnum.POSTPONED: 2,
        })

    def test_order_by_without_messages_first(self):
        def assert_applications_pks_equal_to(pks):
            applications = Application.objects \
                .order_by_without_messages_first() \
                .values_list('pk', flat=True)
            self.assertListEqual(list(applications), pks)

        # Create fourths applications without messages
        # They should be ordered by date
        first_application = ApplicationFactory.create()
        second_application = ApplicationFactory.create()
        third_application = ApplicationFactory.create()
        fourth_application = ApplicationFactory.create()

        assert_applications_pks_equal_to(
            [
                fourth_application.pk, third_application.pk,
                second_application.pk, first_application.pk,
            ]
        )

        # Create a message for third application. So, the third application
        # should be places after all application without messages
        MessageFactory.create(
            owner=self.resident, application=third_application)

        assert_applications_pks_equal_to(
            [
                fourth_application.pk, second_application.pk,
                first_application.pk, third_application.pk,
            ]
        )

        # Create a message for first application. So, the first application
        # should be places after all application without messages and
        # ordered by date
        MessageFactory.create(
            owner=self.resident, application=first_application)

        assert_applications_pks_equal_to(
            [
                fourth_application.pk, second_application.pk,
                third_application.pk, first_application.pk,
            ]
        )

        # Create a message for fourth application. So, the fourth application
        # should be places after all application without messages and
        # ordered by date
        MessageFactory.create(
            owner=self.resident, application=fourth_application)

        assert_applications_pks_equal_to(
            [
                second_application.pk, fourth_application.pk,
                third_application.pk, first_application.pk,
            ]
        )

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
            second_application.state, ApplicationStateEnum.POSTPONED)

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

    def test_reject(self):
        application = ApplicationFactory.create()
        application.reject()
        application.save()
        application.refresh_from_db()
        self.assertEqual(application.state, ApplicationStateEnum.REJECTED)

    def test_reject_permissions(self):
        application = ApplicationFactory.create(
            owner=self.resident, shift=self.shift)

        # Resident can't reject application
        self.assertFalse(has_transition_perm(
            application.reject, self.resident))

        # Scheduler can reject own shift's applications
        self.assertTrue(has_transition_perm(
            application.reject, self.scheduler))

    def test_confirm(self):
        application = ApplicationFactory.create(
            state=ApplicationStateEnum.APPROVED)
        application.confirm()
        application.save()
        application.refresh_from_db()
        self.assertEqual(application.state, ApplicationStateEnum.CONFIRMED)

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

    def test_cancel_approved_not_started(self):
        """
        Checks that cancelling an application for the not started shift
        makes the application cancelled and renews all postponed applications
        """
        self.shift.date_start = timezone.now() + timedelta(hours=1)
        self.shift.save()

        another_shift_postponed_application = ApplicationFactory(
            state=ApplicationStateEnum.POSTPONED
        )
        postponed_application = ApplicationFactory.create(
            shift=self.shift,
            state=ApplicationStateEnum.POSTPONED
        )

        application = ApplicationFactory.create(
            shift=self.shift,
            state=ApplicationStateEnum.APPROVED)
        application.cancel()
        application.save()
        application.refresh_from_db()
        self.assertEqual(application.state, ApplicationStateEnum.CANCELLED)

        postponed_application.refresh_from_db()
        self.assertEqual(postponed_application.state, ApplicationStateEnum.NEW)

        another_shift_postponed_application.refresh_from_db()
        self.assertEqual(
            another_shift_postponed_application.state,
            ApplicationStateEnum.POSTPONED)

    def test_cancel_confirmed_not_started(self):
        """
        Checks that cancelling an application for the not started shift
        makes the application failed and renews all postponed applications
        """
        self.shift.date_start = timezone.now() + timedelta(hours=1)
        self.shift.save()

        postponed_application = ApplicationFactory.create(
            shift=self.shift,
            state=ApplicationStateEnum.POSTPONED
        )

        application = ApplicationFactory.create(
            shift=self.shift,
            state=ApplicationStateEnum.CONFIRMED)
        application.cancel()
        application.save()
        application.refresh_from_db()
        self.assertEqual(application.state, ApplicationStateEnum.FAILED)

        postponed_application.refresh_from_db()
        self.assertEqual(postponed_application.state, ApplicationStateEnum.NEW)

    def test_cancel_started(self):
        """
        Checks that cancelling an application for the started shift
        makes the application failed and doesn't renew all postponed
        applications
        """
        self.shift.date_start = timezone.now() - timedelta(hours=1)
        self.shift.save()

        postponed_application = ApplicationFactory.create(
            shift=self.shift,
            state=ApplicationStateEnum.POSTPONED
        )

        application = ApplicationFactory.create(
            shift=self.shift,
            state=ApplicationStateEnum.APPROVED)
        application.cancel()
        application.save()
        application.refresh_from_db()
        self.assertEqual(application.state, ApplicationStateEnum.FAILED)

        postponed_application.refresh_from_db()
        self.assertEqual(postponed_application.state, ApplicationStateEnum.POSTPONED)

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

    def test_complete(self):
        application = ApplicationFactory.create(
            state=ApplicationStateEnum.CONFIRMED)
        application.complete()
        application.save()
        application.refresh_from_db()
        self.assertEqual(application.state, ApplicationStateEnum.COMPLETED)

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
