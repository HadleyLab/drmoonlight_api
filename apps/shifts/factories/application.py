from factory import DjangoModelFactory, SubFactory

from apps.accounts.factories import ResidentFactory
from apps.shifts.factories import ShiftFactory
from apps.shifts.models import Application


class ApplicationFactory(DjangoModelFactory):
    owner = SubFactory(ResidentFactory)
    shift = SubFactory(ShiftFactory)

    class Meta:
        model = Application
