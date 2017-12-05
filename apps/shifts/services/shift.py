from django.utils.timezone import localtime

from apps.accounts.models import Resident
from apps.accounts.services.user import get_user_context, localize_for_user
from apps.main.utils import async_send_mail


def get_shift_context(shift):
    return {
        'pk': shift.pk,
        'date_start': localtime(shift.date_start).strftime('%Y-%m-%d %H:%M'),
        'date_end': localtime(shift.date_end).strftime('%Y-%m-%d %H:%M'),
        'facility_name': shift.owner.facility_name,
        'department_name': shift.owner.department_name,
        'speciality_name': shift.speciality.name,
        'residency_years_required': shift.residency_years_required,
        'residency_program_name':
            shift.residency_program.name
            if shift.residency_program else None,
        'payment_amount': shift.payment_amount,
        'payment_per_hour': shift.payment_per_hour,
        'description': shift.description,
    }


def get_context(shift, resident, **kwargs):
    context = {
        'resident': get_user_context(resident),
        'shift': get_shift_context(shift),
    }

    context.update(kwargs)

    return context


def process_shift_creation(shift):
    suitable_residents = Resident.objects.filter_for_shift(shift) \
        .filter(notification_new_shifts=True)

    for resident in suitable_residents:
        with localize_for_user(resident):
            async_send_mail(
                'shift_created',
                resident.email,
                get_context(shift, resident)
            )


def process_shift_updating(shift):
    active_applications = shift.applications.filter_active()

    if active_applications.exists():
        suitable_residents = active_applications.all()
        is_applicant = True
    else:
        suitable_residents = Resident.objects.filter_for_shift(shift) \
            .filter(notification_new_shifts=True)
        is_applicant = False

    for resident in suitable_residents:
        with localize_for_user(resident):
            async_send_mail(
                'shift_updated',
                resident.email,
                get_context(shift, resident, is_applicant=is_applicant)
            )


def process_shift_deletion(shift):
    active_applications = shift.applications.filter_active()

    if active_applications.exists():
        for resident in active_applications.all():
            with localize_for_user(resident):
                async_send_mail(
                    'shift_deleted',
                    resident.email,
                    get_context(shift, resident)
                )
