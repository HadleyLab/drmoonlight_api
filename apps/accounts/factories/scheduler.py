from apps.accounts.models import Scheduler
from .user import UserFactory


class SchedulerFactory(UserFactory):

    class Meta:
        model = Scheduler
