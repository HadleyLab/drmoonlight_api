from django.db import models
from django_fsm import FSMIntegerField

from apps.accounts.models import Resident
from apps.main.models import TimestampModelMixin
from .shift import Shift


class ApplicationStateEnum(object):
    NEW = 1

    # First stage
    APPROVED = 2
    REJECTED = 3

    # Second stage
    CONFIRMED = 4
    CANCELLED = 5

    # Third stage
    FAILED = 6
    COMPLETED = 7


class Application(TimestampModelMixin, models.Model):
    owner = models.ForeignKey(
        Resident,
        verbose_name='Owner'
    )
    shift = models.ForeignKey(
        Shift,
        verbose_name='Shift'
    )
    state = FSMIntegerField(default=ApplicationStateEnum.NEW)

    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
