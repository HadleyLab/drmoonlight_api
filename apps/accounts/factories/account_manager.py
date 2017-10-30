from apps.accounts.models import AccountManager
from .user import UserFactory


class AccountManagerFactory(UserFactory):

    class Meta:
        model = AccountManager
