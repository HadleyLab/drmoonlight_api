from datetime import timedelta
from django.utils import timezone
from factory import DjangoModelFactory, SubFactory, lazy_attribute

from apps.accounts.factories import (
    ResidencyProgramFactory, SpecialityFactory, SchedulerFactory)
from apps.shifts.models import Shift


class ShiftFactory(DjangoModelFactory):
    owner = SubFactory(SchedulerFactory)
    residency_program = SubFactory(ResidencyProgramFactory)
    speciality = SubFactory(SpecialityFactory)
    payment_amount = 20
    payment_per_hour = True

    class Meta:
        model = Shift

    @lazy_attribute
    def date_start(self):
        return timezone.now() + timedelta(hours=1)

    @lazy_attribute
    def date_end(self):
        return timezone.now() + timedelta(hours=2)
