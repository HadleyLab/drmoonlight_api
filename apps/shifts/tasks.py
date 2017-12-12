from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from apps.shifts.models import Application, ApplicationStateEnum


@shared_task
def daily_make_confirmed_applications_completed_for_ended_shifts():
    # Completes all confirmed applications for shifts, which were
    # ended day before
    yesterday = timezone.now() - timedelta(days=1)
    applications = Application.objects.filter(
        state=ApplicationStateEnum.CONFIRMED, shift__date_end__lte=yesterday)

    for application in applications:
        application.complete({
            'user': application.shift.owner.user_ptr,
            'text': '',
        })
        application.save()
