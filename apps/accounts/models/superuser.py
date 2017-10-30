from django.db.models.signals import pre_save
from django.dispatch import receiver

from .user import User, UserManager


class SuperUserManager(UserManager):
    def get_queryset(self):
        return super(SuperUserManager, self).get_queryset() \
            .filter(is_superuser=True)


class SuperUser(User):
    objects = SuperUserManager()

    class Meta:
        proxy = True
        verbose_name = 'Superuser'
        verbose_name_plural = 'Superusers'


@receiver(pre_save, sender=SuperUser)
def set_up(sender, instance, *args, **kwargs):
    instance.is_staff = True
    instance.is_superuser = True
