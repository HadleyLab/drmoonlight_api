from django.test import TestCase
from django_fsm import has_transition_perm

from apps.accounts.factories import (
    AccountManagerFactory, ResidentFactory, SchedulerFactory)
from apps.accounts.models import ResidentStateEnum


class ResidentTest(TestCase):
    def setUp(self):
        super(ResidentTest, self).setUp()

        self.account_manager = AccountManagerFactory.create()

    def test_fill_profile(self):
        new_resident = ResidentFactory.create()
        new_resident.fill_profile()
        new_resident.save()
        new_resident.refresh_from_db()
        self.assertEqual(new_resident.state, ResidentStateEnum.PROFILE_FILLED)

    def test_approve(self):
        resident = ResidentFactory.create(
            state=ResidentStateEnum.PROFILE_FILLED)
        resident.approve()
        resident.save()
        resident.refresh_from_db()
        self.assertEqual(resident.state, ResidentStateEnum.APPROVED)

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
