from django.db import models

from apps.accounts.models import Scheduler, Speciality, ResidencyProgram
from apps.main.models import TimestampModelMixin


class Shift(TimestampModelMixin, models.Model):
    date_start = models.DateTimeField(
        verbose_name='Date start'
    )
    date_end = models.DateTimeField(
        verbose_name='Date end'
    )
    owner = models.ForeignKey(
        Scheduler,
        verbose_name='Owner'
    )
    speciality = models.ForeignKey(
        Speciality,
        verbose_name='Speciality'
    )
    residency_program = models.ForeignKey(
        ResidencyProgram,
        verbose_name='Residency program'
    )
    residency_years_required = models.PositiveIntegerField(
        verbose_name='Residency years required',
        null=True
    )
    payment_amount = models.PositiveIntegerField(
        verbose_name='Payment amount'
    )
    payment_per_hour = models.BooleanField(
        verbose_name='Payment per hour'
    )
    description = models.TextField(
        verbose_name='Description',
        blank=True
    )

    class Meta:
        verbose_name = 'Shift'
        verbose_name_plural = 'Shifts'
