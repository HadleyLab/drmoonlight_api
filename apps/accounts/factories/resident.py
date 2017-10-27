from apps.accounts.models import Resident
from .user import UserFactory


class ResidentFactory(UserFactory):

    class Meta:
        model = Resident
