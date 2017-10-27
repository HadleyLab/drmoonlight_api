from factory import DjangoModelFactory

from apps.accounts.models import Speciality


class SpecialityFactory(DjangoModelFactory):

    class Meta:
        model = Speciality
