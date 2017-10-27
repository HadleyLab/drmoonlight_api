from factory import DjangoModelFactory, SubFactory, Faker

from apps.accounts.factories import (
    ResidencyProgramFactory, SpecialityFactory, SchedulerFactory)
from apps.shifts.models import Shift


class ShiftFactory(DjangoModelFactory):
    # TODO: Use more complex logic for date_start/date_end
    date_start = Faker('date_time')
    date_end = Faker('date_time')
    owner = SubFactory(SchedulerFactory)
    residency_program = SubFactory(ResidencyProgramFactory)
    speciality = SubFactory(SpecialityFactory)
    payment_amount = 20
    payment_per_hour = True

    class Meta:
        model = Shift
