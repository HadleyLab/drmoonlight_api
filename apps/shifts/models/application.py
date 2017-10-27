from django.db import models
from django_fsm import FSMIntegerField, transition

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
        related_name='applications',
        verbose_name='Owner'
    )
    shift = models.ForeignKey(
        Shift,
        related_name='applications',
        verbose_name='Shift'
    )
    state = FSMIntegerField(default=ApplicationStateEnum.NEW)

    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'

    def __str__(self):
        return "{0} for {1}".format(self.owner, self.shift)

    @transition(field=state,
                source=ApplicationStateEnum.NEW,
                target=ApplicationStateEnum.APPROVED)
    def approve(self):
        """
        Approves current application and makes rejected all other
        new applications
        """
        new_applications = self.shift.applications.exclude(
            pk=self.pk).filter(state=ApplicationStateEnum.NEW)

        for application in new_applications:
            application.reject()
            application.save()

    @transition(field=state,
                source=ApplicationStateEnum.NEW,
                target=ApplicationStateEnum.REJECTED)
    def reject(self):
        pass

    @transition(field=state,
                source=ApplicationStateEnum.APPROVED,
                target=ApplicationStateEnum.CONFIRMED)
    def confirm(self):
        pass

    @transition(field=state,
                source=ApplicationStateEnum.APPROVED,
                target=ApplicationStateEnum.CANCELLED)
    @transition(field=state,
                source=ApplicationStateEnum.CONFIRMED,
                target=ApplicationStateEnum.FAILED)
    def cancel(self):
        pass

    @transition(field=state,
                source=ApplicationStateEnum.CONFIRMED,
                target=ApplicationStateEnum.COMPLETED)
    def complete(self):
        pass
