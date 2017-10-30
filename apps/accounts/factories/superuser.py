from apps.accounts.models import SuperUser
from .user import UserFactory


class SuperUserFactory(UserFactory):

    class Meta:
        model = SuperUser
