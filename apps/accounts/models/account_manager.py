from django.db.models.signals import pre_save
from django.dispatch import receiver

from .user import User


class AccountManager(User):
    class Meta:
        verbose_name = 'Account manager'
        verbose_name_plural = 'Account manager'


@receiver(pre_save, sender=AccountManager)
def set_up(sender, instance, *args, **kwargs):
    instance.is_staff = True
    instance.username = instance.email
