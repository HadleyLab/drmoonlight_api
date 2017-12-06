from factory import post_generation

from apps.accounts.models import Resident
from .user import UserFactory


class ResidentFactory(UserFactory):

    class Meta:
        model = Resident

    @post_generation
    def specialities(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for speciality in extracted:
                self.specialities.add(speciality)
