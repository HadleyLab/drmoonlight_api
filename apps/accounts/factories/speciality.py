from factory import DjangoModelFactory, fuzzy

from apps.accounts.models import Speciality


class SpecialityFactory(DjangoModelFactory):
    name = fuzzy.FuzzyText()

    class Meta:
        model = Speciality
