from django.db import models
from django.db.models import Count, Case, When
from django_fsm import FSMIntegerField, transition, RETURN_VALUE

from apps.main.models import TimestampModelMixin
from apps.shifts.services.application import (
    process_approving,
    process_cancelling,
    process_completing,
    process_confirming,
    process_postponing,
    process_renewing,
    process_rejecting
)


class ApplicationStateEnum(object):
    NEW = 1

    # First stage (when a resident approved or rejected)
    APPROVED = 2
    REJECTED = 3
    POSTPONED = 4

    # Second stage (when resident confirmed or cancelled)
    CONFIRMED = 5
    CANCELLED = 6

    # Third stage (when shift ended)
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

    # An application is active when the shift isn't ended and the applications
    # isn't cancelled/rejected/postponed
    ACTIVE_STATES = (NEW, APPROVED, CONFIRMED, )


def can_scheduler_change_application(instance, user):
    return user.is_scheduler and instance.shift.owner == user.scheduler


def can_resident_change_application(instance, user):
    return user.is_resident and instance.owner == user.resident


def can_resident_or_scheduler_change_application(instance, user):
    return can_scheduler_change_application(instance, user) or \
           can_resident_change_application(instance, user)


class ApplicationQuerySet(models.QuerySet):
    def filter_for_resident(self, resident):
        if resident.is_approved:
            return self.filter(owner=resident)

        return self.none()  # pragma: no cover

    def filter_for_scheduler(self, scheduler):
        return self.filter(shift__owner=scheduler)

    def filter_for_user(self, user):
        if user.is_scheduler:
            return self.filter_for_scheduler(user.scheduler)

        if user.is_resident:
            return self.filter_for_resident(user.resident)

        return self.none()  # pragma: no cover

    def filter_active(self):
        return self.filter(state__in=ApplicationStateEnum.ACTIVE_STATES)

    def aggregate_count_by_state(self):
        count_by_state = self.values('state') \
            .order_by('state') \
            .annotate(count=Count('state')) \
            .values_list('state', 'count')

        return dict(count_by_state)

    def annotate_messages_count(self):
        return self.annotate(
            annotated_messages_count=Count('messages', distinct=True)
        )

    def order_by_without_messages_first(self):
        return self.annotate_messages_count().annotate(
            without_messages=Case(
                When(annotated_messages_count=0, then=True),
                default=False,
                output_field=models.BooleanField()
            )
        ).order_by('-without_messages', '-date_created')


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
        'accounts.Resident',
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

    @property
    def messages_count(self):
        if hasattr(self, 'annotated_messages_count'):
            return self.annotated_messages_count
        return self.messages.count()

    @property
    def last_message(self):
        """
        Returns last message for the applications (sorted by date)

        TODO: optimize it. Now it creates N+1 queries
        """
        return self.messages.order_by('date_created').last()

    @transition(field=state,
                source=ApplicationStateEnum.NEW,
                target=ApplicationStateEnum.APPROVED,
                permission=can_scheduler_change_application)
    def approve(self, data):
        """
        Approves the application and postpone all other
        new applications
        """
        new_applications = self.shift.applications.exclude(
            pk=self.pk).filter(state=ApplicationStateEnum.NEW)

        for application in new_applications:
            application.postpone()
            application.save()

        process_approving(self, data['user'], data['text'])

    @transition(field=state,
                source=ApplicationStateEnum.NEW,
                target=ApplicationStateEnum.POSTPONED,
                custom={'viewset': False, 'admin': False})
    def postpone(self):
        """
        Postpones the application
        """
        process_postponing(self)

    @transition(field=state,
                source=ApplicationStateEnum.POSTPONED,
                target=ApplicationStateEnum.NEW,
                custom={'viewset': False, 'admin': False})
    def renew(self):
        """
        Renews the application
        """
        process_renewing(self)

    @transition(field=state,
                source=ApplicationStateEnum.NEW,
                target=ApplicationStateEnum.REJECTED,
                permission=can_scheduler_change_application)
    def reject(self, data):
        """
        Rejects  the application
        """
        process_rejecting(self, data['user'], data['text'])

    @transition(field=state,
                source=ApplicationStateEnum.APPROVED,
                target=ApplicationStateEnum.CONFIRMED,
                permission=can_resident_change_application)
    def confirm(self, data):
        """
        Confirms the application
        """
        process_confirming(self, data['user'], data['text'])

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
    def cancel(self, data):
        """
        Cancels the application and renew all postponed applications if
        the shift wasn't started
        """
        process_cancelling(self, data['user'], data['text'])

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
                permission=can_scheduler_change_application,
                conditions=[lambda application: application.shift.is_ended]
    )
    def complete(self, data):
        """
        Completes the application
        """
        process_completing(self, data['user'], data['text'])
