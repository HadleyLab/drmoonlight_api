from datetime import timedelta

from django.db.models import Count, Avg
from django.db.models.functions import TruncMonth
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from apps.accounts.models import Resident, Speciality
from apps.shifts.models import Shift, ApplicationStateEnum


@api_view()
@permission_classes((AllowAny, ))
def statistics(request):
    now = timezone.now()
    current_month_date_start = now.replace(day=1).date()
    last_month_date_start = (
        (current_month_date_start - timedelta(days=1)).replace(day=1))

    available_shifts_count = Shift.objects.filter(
        date_start__gt=now).count()
    residents_count = Resident.objects.filter_approved().count()
    required_specialities_top = Speciality.objects.annotate(
        shifts_count=Count('shifts')
    ).order_by('-shifts_count').values('pk', 'name', 'shifts_count')

    # Calculate average for past months shifts
    average_shifts_per_months_count = Shift.objects \
        .filter(date_start__lt=current_month_date_start) \
        .annotate(month=TruncMonth('date_start')) \
        .values('month') \
        .annotate(count=Count('pk')) \
        .values('month', 'count') \
        .aggregate(average=Avg('count'))['average'] or 0
    all_completed_shifts = Shift.objects.filter(
        date_start__gte=now,
        applications__state=ApplicationStateEnum.COMPLETED)

    # TODO: Add denormalization or think about better solution
    total_earned_money_amount = sum([
        shift.total_payment_amount for shift in all_completed_shifts.all()])

    last_month_shifts = all_completed_shifts.filter(
        date_start__gte=last_month_date_start,
        date_start__lt=current_month_date_start
    )
    # TODO: Add denormalization or think about better solution
    last_month_earned_money_amount = sum([
        shift.total_payment_amount for shift in last_month_shifts.all()])
    last_month_worked_residents_count = last_month_shifts.values(
        'applications__owner').distinct().count()

    return Response({
        'available_shifts_count': available_shifts_count,
        'average_shifts_per_months_count': average_shifts_per_months_count,

        'residents_count': residents_count,
        'required_specialities_top': required_specialities_top,
        'total_earned_money_amount': total_earned_money_amount,

        'last_month_earned_money_amount': last_month_earned_money_amount,
        'last_month_worked_residents_count': last_month_worked_residents_count,
    })
