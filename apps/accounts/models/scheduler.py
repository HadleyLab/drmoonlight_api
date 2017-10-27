from django.db import models
from django_fsm import FSMIntegerField, transition

from .user import User


class SchedulerStateEnum(object):
    NEW = 1
    EMAIL_CONFIRMED = 2
    APPROVED = 3


class Scheduler(User):
    facility_name = models.CharField(
        verbose_name='Facility name',
        max_length=255
    )
    department_name = models.CharField(
        verbose_name='Department name',
        max_length=255
    )
    state = FSMIntegerField(
        verbose_name='State',
        default=SchedulerStateEnum.NEW
    )

    class Meta:
        verbose_name = 'Scheduler'
        verbose_name_plural = 'Schedulers'

    @transition(
        field=state,
        source=SchedulerStateEnum.NEW,
        target=SchedulerStateEnum.EMAIL_CONFIRMED
    )
    def confirm_email(self):
        # TODO: send email to the managing editor
        pass

    @transition(
        field=state,
        source=SchedulerStateEnum.EMAIL_CONFIRMED,
        target=SchedulerStateEnum.APPROVED
    )
    def approve(self):
        # TODO: send email to the scheduler
        pass
