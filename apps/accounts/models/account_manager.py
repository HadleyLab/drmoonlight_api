from django.db.models.signals import pre_save
from django.dispatch import receiver

from .user import User, UserManager


class AccountManager(User):
    objects = UserManager()

    class Meta:
        verbose_name = 'Account manager'
        verbose_name_plural = 'Account manager'


@receiver(pre_save, sender=AccountManager)
def set_up(sender, instance, *args, **kwargs):
    instance.is_staff = True
