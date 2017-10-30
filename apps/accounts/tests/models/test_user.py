from django.test import TestCase

from apps.accounts.factories import (
    AccountManagerFactory, ResidentFactory, SchedulerFactory)


class UserTest(TestCase):
    def setUp(self):
        self.resident = ResidentFactory.create()
        self.scheduler = SchedulerFactory.create()
        self.account_manager = AccountManagerFactory.create()

    def test_is_resident(self):
        self.assertTrue(self.resident.is_resident)
        self.assertFalse(self.scheduler.is_resident)
        self.assertFalse(self.account_manager.is_resident)

    def test_is_scheduler(self):
        self.assertFalse(self.resident.is_scheduler)
        self.assertTrue(self.scheduler.is_scheduler)
        self.assertFalse(self.account_manager.is_scheduler)

    def test_is_account_manager(self):
        self.assertFalse(self.resident.is_account_manager)
        self.assertFalse(self.scheduler.is_account_manager)
        self.assertTrue(self.account_manager.is_account_manager)

    def test_full_name(self):
        user = SchedulerFactory.create(
            first_name='', last_name='', username='username')
        self.assertEqual(user.full_name, 'username')

        user = SchedulerFactory.create(
            first_name='first', last_name='')
        self.assertEqual(user.full_name, 'first')

        user = SchedulerFactory.create(
            first_name='', last_name='last')
        self.assertEqual(user.full_name, 'last')

        user = SchedulerFactory.create(
            first_name='first', last_name='last')
        self.assertEqual(user.full_name, 'last first')
