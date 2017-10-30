from django.test import TestCase

from apps.accounts.models import AccountManager


class AccountManagerTest(TestCase):
    def test_create(self):
        account_manager = AccountManager.objects.create(
            first_name='first', last_name='last', email='test@gmail.com'
        )
        self.assertEqual(account_manager.email, account_manager.username)
        self.assertTrue(account_manager.is_staff)
