from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .user import User


class Scheduler(User):
    facility_name = models.CharField(
        verbose_name='Facility name',
        max_length=255
    )
    department_name = models.CharField(
        verbose_name='Department name',
        max_length=255
    )

    class Meta:
        verbose_name = 'Scheduler'
        verbose_name_plural = 'Schedulers'


@receiver(pre_save, sender=Scheduler)
def set_up(sender, instance, *args, **kwargs):
    instance.is_staff = True
    instance.username = instance.email
