from django.test import TestCase

from apps.accounts.models import SuperUser


class SuperUserTest(TestCase):
    def test_create(self):
        superuser = SuperUser.objects.create(
            first_name='first', last_name='last', email='test@gmail.com'
        )
        self.assertEqual(superuser.email, superuser.username)
        self.assertTrue(superuser.is_staff)
