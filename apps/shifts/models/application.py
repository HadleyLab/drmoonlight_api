from django.db import models

from apps.accounts.models import Resident
from .shift import Shift


class Application(models.Model):
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date created'
    )
    date_modified = models.DateTimeField(
        auto_now=True,
        verbose_name='Date modified'
    )
    owner = models.ForeignKey(
        Resident,
        verbose_name='Owner'
    )
    shift = models.ForeignKey(
        Shift,
        verbose_name='Shift'
    )

    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
