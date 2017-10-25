from .user import User


class AccountManager(User):
    class Meta:
        verbose_name = 'Account manager'
        verbose_name_plural = 'Account manager'
