from django.test import TestCase

from apps.accounts.factories import (
    AccountManagerFactory, ResidentFactory, SchedulerFactory, SuperUserFactory)
from apps.accounts.models import User


class UserTest(TestCase):
    def setUp(self):
        self.resident = ResidentFactory.create()
        self.scheduler = SchedulerFactory.create()
        self.account_manager = AccountManagerFactory.create()
        self.superuser = SuperUserFactory.create()

    def test_is_resident(self):
        self.assertTrue(self.resident.is_resident)
        self.assertFalse(self.scheduler.is_resident)
        self.assertFalse(self.account_manager.is_resident)
        self.assertFalse(self.superuser.is_resident)

    def test_is_scheduler(self):
        self.assertFalse(self.resident.is_scheduler)
        self.assertTrue(self.scheduler.is_scheduler)
        self.assertFalse(self.account_manager.is_scheduler)
        self.assertFalse(self.superuser.is_scheduler)

    def test_is_account_manager(self):
        self.assertFalse(self.resident.is_account_manager)
        self.assertFalse(self.scheduler.is_account_manager)
        self.assertTrue(self.account_manager.is_account_manager)
        self.assertFalse(self.superuser.is_account_manager)

    def test_full_name(self):
        user = SchedulerFactory.create(
            first_name='', last_name='', email='test@gmail.com')
        self.assertEqual(user.full_name, 'test@gmail.com')

        user = SchedulerFactory.create(
            first_name='first', last_name='')
        self.assertEqual(user.full_name, 'first')

        user = SchedulerFactory.create(
            first_name='', last_name='last')
        self.assertEqual(user.full_name, 'last')

        user = SchedulerFactory.create(
            first_name='first', last_name='last')
        self.assertEqual(user.full_name, 'last first')

    def test_create_user_raises_value_error_in_email_is_not_specified(self):
        with self.assertRaises(ValueError):
            User.objects.create_user('', 'qwertyuiop')

    def test_create_user(self):
        user = User.objects.create_user('email@gmail.com', 'qwertyuiop')
        self.assertEqual(user.email, 'email@gmail.com')
        self.assertTrue(user.check_password('qwertyuiop'))
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        user = User.objects.create_superuser('email@gmail.com', 'qwertyuiop')
        self.assertEqual(user.email, 'email@gmail.com')
        self.assertTrue(user.check_password('qwertyuiop'))
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_superuser_raises_value_error_for_false_is_staff(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                'email@gmail.com', 'qwertyuiop', is_staff=False)

    def test_create_superuser_raises_value_error_for_false_is_superuser(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                'email@gmail.com', 'qwertyuiop', is_superuser=False)

    def test_role(self):
        self.assertEqual(self.resident.role, 'resident')
        self.assertEqual(self.scheduler.role, 'scheduler')
        self.assertEqual(self.account_manager.role, 'account_manager')
        self.assertEqual(self.superuser.role, 'user')
