from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    @property
    def full_name(self):
        name = self.last_name + ' ' + self.first_name
        return name if name != ' ' else self.username

    @property
    def is_scheduler(self):
        return hasattr(self, 'scheduler')

    @property
    def is_resident(self):
        return hasattr(self, 'resident')

    @property
    def is_account_manager(self):
        return hasattr(self, 'accountmanager')
