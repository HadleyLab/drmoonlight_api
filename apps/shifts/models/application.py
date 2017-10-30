from django.db import models
from django_fsm import FSMIntegerField, transition, RETURN_VALUE

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


def can_scheduler_change_application(instance, user):
    return user.is_scheduler and instance.shift.owner == user.scheduler


def can_resident_change_application(instance, user):
    return user.is_resident and instance.owner == user


def can_resident_or_scheduler_change_application(instance, user):
    return can_scheduler_change_application(instance, user) or \
           can_resident_change_application(instance, user)


class Application(TimestampModelMixin, models.Model):
    """
    Application workflow:
    1. A resident creates an application with NEW state.

    2. A scheduler can:
        2.1. Approve the application
        The application will become APPROVED. The other new applications
        will become REJECTED.
        2.2. Reject the application
        The state will be changed to REJECTED.

    3. The resident can:
        3.1. Confirm the application
        The application will become CONFIRMED.
        3.2. Cancel the application
        The application will become CANCELLED if shift was not started
        otherwise become FAILED

    4. The scheduler or the resident can cancel the confirmed application
    The application will become FAILED (TODO: discuss and update comment).

    5. The scheduler can complete the application after the resident completes
    the shift in real life
    The application will become COMPLETED.
    """
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
    state = FSMIntegerField(
        verbose_name='State',
        default=ApplicationStateEnum.NEW
    )

    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'

    def __str__(self):
        return "{0} for {1}".format(self.owner, self.shift)

    @transition(field=state,
                source=ApplicationStateEnum.NEW,
                target=ApplicationStateEnum.APPROVED,
                permission=can_scheduler_change_application)
    def approve(self):
        """
        Approves the application and makes rejected all other
        new applications
        """
        new_applications = self.shift.applications.exclude(
            pk=self.pk).filter(state=ApplicationStateEnum.NEW)

        for application in new_applications:
            application.reject()
            application.save()

    @transition(field=state,
                source=ApplicationStateEnum.NEW,
                target=ApplicationStateEnum.REJECTED,
                permission=can_scheduler_change_application)
    def reject(self):
        pass

    @transition(field=state,
                source=ApplicationStateEnum.APPROVED,
                target=ApplicationStateEnum.CONFIRMED,
                permission=can_resident_change_application)
    def confirm(self):
        pass

    @transition(field=state,
                source=[
                    ApplicationStateEnum.APPROVED,
                    ApplicationStateEnum.CONFIRMED,
                ],
                target=RETURN_VALUE(
                    ApplicationStateEnum.CANCELLED,
                    ApplicationStateEnum.FAILED,
                ),
                permission=can_resident_or_scheduler_change_application)
    def cancel(self):
        """
        Cancels the application if a confirmed shift is not started
        """
        if not self.shift.is_started:
            # TODO: send notification to REJECTED application's owners
            # TODO: about shift availability
            pass

            if self.state == ApplicationStateEnum.APPROVED:
                # TODO: discuss it. May be if the resident cancels
                # TODO: the CONFIRMED application for the not started shift
                # TODO: we should always transit the application to cancelled
                return ApplicationStateEnum.CANCELLED

        return ApplicationStateEnum.FAILED

    @transition(field=state,
                source=ApplicationStateEnum.CONFIRMED,
                target=ApplicationStateEnum.COMPLETED,
                permission=can_scheduler_change_application)
    def complete(self):
        pass
