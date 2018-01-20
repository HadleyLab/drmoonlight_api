from django.test import TestCase

from apps.accounts.factories import (
    SpecialityFactory, ResidentFactory)
from apps.accounts.models import ResidentStateEnum
from apps.shifts.factories import ShiftFactory


class ShiftsTestCaseMixin(TestCase):
    """
    Provides initial data for shifts application
    """
    def setUp(self):
        super(ShiftsTestCaseMixin, self).setUp()

        self.first_speciality = SpecialityFactory.create()
        self.second_speciality = SpecialityFactory.create()
        self.first_shift = ShiftFactory.create(
            residency_years_required=0,
            speciality=self.first_speciality
        )
        self.second_shift = ShiftFactory.create(
            residency_years_required=5,
            speciality=self.second_speciality
        )

        self.approved_resident = ResidentFactory.create(
            state=ResidentStateEnum.APPROVED,
            residency_years=5,
        )
        self.approved_resident.specialities.add(
            self.first_speciality, self.second_speciality)
