from django.test import TestCase

from apps.accounts.models import Scheduler


class SchedulerTest(TestCase):
    def test_create(self):
        scheduler = Scheduler.objects.create(
            first_name='first', last_name='last', email='test@gmail.com')
        self.assertFalse(scheduler.is_staff)
