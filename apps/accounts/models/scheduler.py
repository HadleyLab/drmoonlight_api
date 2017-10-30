from django.db import models

from .user import User, UserManager


class Scheduler(User):
    facility_name = models.CharField(
        verbose_name='Facility name',
        max_length=255
    )
    department_name = models.CharField(
        verbose_name='Department name',
        max_length=255
    )

    objects = UserManager()

    class Meta:
        verbose_name = 'Scheduler'
        verbose_name_plural = 'Schedulers'
