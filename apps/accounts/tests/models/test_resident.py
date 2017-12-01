from django.test import TestCase, mock
from django_fsm import has_transition_perm

from apps.accounts.factories import (
    AccountManagerFactory, ResidentFactory, SchedulerFactory)
from apps.accounts.models import ResidentStateEnum, Resident


class ResidentTest(TestCase):
    def setUp(self):
        super(ResidentTest, self).setUp()

        self.account_manager = AccountManagerFactory.create()

    @mock.patch(
        'apps.accounts.models.resident.process_resident_profile_filling',
        autospec=True)
    def test_fill_profile(self, mock_process_resident_profile_filling):
        new_resident = ResidentFactory.create()
        new_resident.fill_profile({})
        new_resident.save()
        new_resident.refresh_from_db()
        self.assertEqual(new_resident.state, ResidentStateEnum.PROFILE_FILLED)

        mock_process_resident_profile_filling.assert_called_with(new_resident)

    @mock.patch(
        'apps.accounts.models.resident.process_resident_approving',
        autospec=True)
    def test_approve(self, mock_process_resident_approving):
        resident = ResidentFactory.create(
            state=ResidentStateEnum.PROFILE_FILLED)
        resident.approve()
        resident.save()
        resident.refresh_from_db()
        self.assertEqual(resident.state, ResidentStateEnum.APPROVED)

        mock_process_resident_approving.assert_called_with(resident)

    def test_approve_permission(self):
        resident = ResidentFactory.create(
            state=ResidentStateEnum.PROFILE_FILLED)

        # Scheduler (not account manager) can't approve resident
        scheduler = SchedulerFactory.create()

        self.assertFalse(has_transition_perm(
            resident.approve, scheduler))

        # Account manager can approve resident
        self.assertTrue(has_transition_perm(
            resident.approve, self.account_manager))

    @mock.patch(
        'apps.accounts.models.resident.process_resident_rejecting',
        autospec=True)
    def test_reject(self, mock_process_resident_rejecting):
        resident = ResidentFactory.create(
            state=ResidentStateEnum.PROFILE_FILLED)
        resident.reject()
        resident.save()
        resident.refresh_from_db()
        self.assertEqual(resident.state, ResidentStateEnum.REJECTED)

        mock_process_resident_rejecting.assert_called_with(resident)

    def test_reject_permission(self):
        resident = ResidentFactory.create(
            state=ResidentStateEnum.PROFILE_FILLED)

        # Scheduler (not account manager) can't approve resident
        scheduler = SchedulerFactory.create()

        self.assertFalse(has_transition_perm(
            resident.reject, scheduler))

        # Account manager can approve resident
        self.assertTrue(has_transition_perm(
            resident.reject, self.account_manager))

    def test_create(self):
        resident = Resident.objects.create(
            first_name='first', last_name='last', email='test@gmail.com')
        self.assertFalse(resident.is_staff)
