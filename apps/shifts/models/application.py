from django.db import models
from django.db.models import Count
from django_fsm import FSMIntegerField, transition, RETURN_VALUE

from apps.accounts.models import Resident
from apps.main.models import TimestampModelMixin


class ApplicationStateEnum(object):
    NEW = 1

    # First stage
    APPROVED = 2
    REJECTED = 3
    POSTPONED = 4

    # Second stage
    CONFIRMED = 5
    CANCELLED = 6

    # Third stage
    FAILED = 7
    COMPLETED = 8

    CHOICES = (
        (NEW, 'New'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (POSTPONED, 'Postponed'),
        (CONFIRMED, 'Confirmed'),
        (CANCELLED, 'Cancelled'),
        (FAILED, 'Failed'),
        (COMPLETED, 'Completed'),
    )


def can_scheduler_change_application(instance, user):
    return user.is_scheduler and instance.shift.owner == user.scheduler


def can_resident_change_application(instance, user):
    return user.is_resident and instance.owner == user


def can_resident_or_scheduler_change_application(instance, user):
    return can_scheduler_change_application(instance, user) or \
           can_resident_change_application(instance, user)


class ApplicationQuerySet(models.QuerySet):
    def filter_for_resident(self, resident):
        if resident.is_approved:
            return self.filter(owner=resident)

        return self.none()

    def filter_for_scheduler(self, scheduler):
        return self.filter(shift__owner=scheduler)

    def filter_for_user(self, user):
        if user.is_scheduler:
            return self.filter_for_scheduler(user.scheduler)

        if user.is_resident:
            return self.filter_for_resident(user.resident)

        return self.none()  # pragma: no cover

    def aggregate_count_by_state(self):
        count_by_state = self.values('state') \
            .order_by('state') \
            .annotate(count=Count('state')) \
            .values_list('state', 'count')

        return dict(count_by_state)


class Application(TimestampModelMixin, models.Model):
    """
    Application workflow:
    1. A resident creates an application with NEW state.

    2. A scheduler can:
        2.1. Approve the application
        The application will become APPROVED. The other new applications
        will become POSTPONED.
        2.2. Reject the application
        The state will be changed to REJECTED.

    3. The resident can:
        3.1. Confirm the application
        The application will become CONFIRMED.
        3.2. Cancel the application
        The application will become CANCELLED if shift was not started
        otherwise become FAILED

    4. The scheduler or the resident can cancel the confirmed application
    The application will become FAILED

    5. The scheduler can complete the application after the resident completes
    the shift in real life
    The application will become COMPLETED.

    When a resident/a scheduler cancels the application, all postponed
    applications become new.
    """
    owner = models.ForeignKey(
        Resident,
        related_name='applications',
        verbose_name='Owner'
    )
    shift = models.ForeignKey(
        'shifts.Shift',
        related_name='applications',
        verbose_name='Shift'
    )
    state = FSMIntegerField(
        verbose_name='State',
        default=ApplicationStateEnum.NEW,
        choices=ApplicationStateEnum.CHOICES
    )
    objects = ApplicationQuerySet.as_manager()

    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'

    def __str__(self):
        return "{0} by {1}".format(self.shift, self.owner)

    @transition(field=state,
                source=ApplicationStateEnum.NEW,
                target=ApplicationStateEnum.APPROVED,
                permission=can_scheduler_change_application)
    def approve(self):
        """
        Approves the application and postpone all other
        new applications
        """
        new_applications = self.shift.applications.exclude(
            pk=self.pk).filter(state=ApplicationStateEnum.NEW)

        for application in new_applications:
            application.postpone()
            application.save()

    @transition(field=state,
                source=ApplicationStateEnum.NEW,
                target=ApplicationStateEnum.POSTPONED,
                custom={'viewset': False, 'admin': False})
    def postpone(self):
        """
        Postpones the application
        """
        pass

    @transition(field=state,
                source=ApplicationStateEnum.POSTPONED,
                target=ApplicationStateEnum.NEW,
                custom={'viewset': False, 'admin': False})
    def renew(self):
        """
        Renews the application
        """
        # TODO: send notification to POSTPONED application's owners
        # TODO: about shift availability
        pass

    @transition(field=state,
                source=ApplicationStateEnum.NEW,
                target=ApplicationStateEnum.REJECTED,
                permission=can_scheduler_change_application)
    def reject(self):
        """
        Rejects  the application
        """

    @transition(field=state,
                source=ApplicationStateEnum.APPROVED,
                target=ApplicationStateEnum.CONFIRMED,
                permission=can_resident_change_application)
    def confirm(self):
        """
        Confirms the application
        """
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
        Cancels the application and renew all postponed applications if
        the shift wasn't started
        """
        if not self.shift.is_started:
            postponed_applications = self.shift.applications.filter(
                state=ApplicationStateEnum.POSTPONED)

            for application in postponed_applications:
                application.renew()
                application.save()

            if self.state == ApplicationStateEnum.APPROVED:
                return ApplicationStateEnum.CANCELLED

        return ApplicationStateEnum.FAILED

    @transition(field=state,
                source=ApplicationStateEnum.CONFIRMED,
                target=ApplicationStateEnum.COMPLETED,
                permission=can_scheduler_change_application)
    def complete(self):
        """
        Completes the application
        """
        # TODO: check that now() >= shift.date_end
        pass
